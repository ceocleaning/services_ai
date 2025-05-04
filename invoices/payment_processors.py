"""
Payment processor abstraction layer for the invoices app.
This module provides a common interface for different payment processors.
"""
import stripe
from abc import ABC, abstractmethod
from decimal import Decimal
from django.conf import settings
from django.utils import timezone

from .models import Payment, PaymentMethod, Invoice, InvoiceStatus


class PaymentProcessor(ABC):
    """
    Abstract base class for payment processors.
    All payment processors should implement this interface.
    """
    
    @abstractmethod
    def create_payment_intent(self, invoice, amount):
        """
        Create a payment intent for immediate payment.
        
        Args:
            invoice: The Invoice object
            amount: The amount to charge
            
        Returns:
            dict: Response containing client_secret and any other necessary data
        """
        pass
    
    @abstractmethod
    def create_setup_intent(self, invoice, amount):
        """
        Create a setup intent for future payment.
        
        Args:
            invoice: The Invoice object
            amount: The amount that will be charged later
            
        Returns:
            dict: Response containing client_secret and any other necessary data
        """
        pass
    
    @abstractmethod
    def process_payment_success(self, invoice, payment_data):
        """
        Process a successful payment.
        
        Args:
            invoice: The Invoice object
            payment_data: Data from the payment processor
            
        Returns:
            Payment: The created Payment object
        """
        pass
    
    @abstractmethod
    def process_setup_success(self, invoice, setup_data):
        """
        Process a successful setup intent.
        
        Args:
            invoice: The Invoice object
            setup_data: Data from the payment processor
            
        Returns:
            bool: True if successful
        """
        pass
    
    @abstractmethod
    def capture_authorized_payment(self, invoice, payment_method_id, amount):
        """
        Capture a previously authorized payment.
        
        Args:
            invoice: The Invoice object
            payment_method_id: The payment method ID to charge
            amount: The amount to charge
            
        Returns:
            Payment: The created Payment object
        """
        pass


class StripeProcessor(PaymentProcessor):
    """
    Stripe payment processor implementation.
    """
    
    def __init__(self):
        """Initialize the Stripe API with the secret key."""
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
    def create_payment_intent(self, invoice, amount):
        """Create a Stripe PaymentIntent for immediate payment."""
        amount_cents = int(amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            metadata={
                'invoice_id': str(invoice.id),
                'invoice_number': invoice.invoice_number,
                'customer_name': invoice.booking.name,
                'customer_email': invoice.booking.email,
                'payment_type': 'instant'
            }
        )
        
        return {
            'client_secret': intent.client_secret,
            'processor': 'stripe'
        }
    
    def create_setup_intent(self, invoice, amount):
        """
        Create a Stripe SetupIntent for future payment authorization.
        This allows saving a payment method without charging it immediately.
        """
        # Create a customer or use existing one
        customer_email = invoice.booking.email
        customer_name = invoice.booking.name
        
        # Check if customer already exists
        existing_customers = stripe.Customer.list(email=customer_email, limit=1)
        
        if existing_customers and existing_customers.data:
            customer = existing_customers.data[0]
        else:
            # Create a new customer
            customer = stripe.Customer.create(
                email=customer_email,
                name=customer_name,
                metadata={
                    'invoice_id': str(invoice.id),
                    'invoice_number': invoice.invoice_number
                }
            )
        
        # Create setup intent with the customer
        setup_intent = stripe.SetupIntent.create(
            customer=customer.id,
            payment_method_types=['card'],
            usage='off_session',  # This indicates the payment method will be used when the customer is not present
            metadata={
                'invoice_id': str(invoice.id),
                'invoice_number': invoice.invoice_number,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'payment_type': 'authorize',
                'amount': str(amount)
            }
        )
        
        return {
            'client_secret': setup_intent.client_secret,
            'customer_id': customer.id,
            'processor': 'stripe'
        }
    
    def process_payment_success(self, invoice, payment_data):
        """Process a successful Stripe payment."""
        payment_intent_id = payment_data.get('payment_intent_id')
        amount = payment_data.get('amount')
        
        # Create payment record
        payment = Payment.objects.create(
            invoice=invoice,
            amount=Decimal(amount),
            payment_method=PaymentMethod.STRIPE,
            transaction_id=payment_intent_id,
            payment_date=timezone.now()
        )
        
        return payment
    
    def process_setup_success(self, invoice, setup_data):
        """
        Process a successful Stripe setup intent.
        This saves the payment method for future use without charging it.
        """
        try:
            setup_intent_id = setup_data.get('setup_intent_id')
            payment_method_id = setup_data.get('payment_method_id')
            
            if not setup_intent_id or not payment_method_id:
                raise ValueError("Setup intent ID and payment method ID are required")
            
            # Retrieve the setup intent to get customer ID
            setup_intent = stripe.SetupIntent.retrieve(setup_intent_id)
            customer_id = setup_intent.customer
            
            if not customer_id:
                raise ValueError("No customer ID found in setup intent")
            
            # Attach the payment method to the customer for future use
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id
            )
            
            # Set this payment method as the default for the customer
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
            
            # Update invoice to show payment method is authorized
            current_notes = invoice.notes or ''
            new_note = f"\nPayment method authorized via Stripe on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}."
            new_note += f"\nSetup Intent ID: {setup_intent_id}"
            new_note += f"\nPayment Method ID: {payment_method_id}"
            new_note += f"\nStripe Customer ID: {customer_id}"
            
            invoice.notes = current_notes + new_note
            invoice.save()
            
            return True
        except Exception as e:
            import traceback
            print(f"Error in process_setup_success: {str(e)}")
            print(traceback.format_exc())
            return False
    
    def capture_authorized_payment(self, invoice, payment_method_id, amount):
        """
        Capture a previously authorized Stripe payment.
        This creates a payment intent using the saved payment method and captures it immediately.
        """
        amount_cents = int(amount * 100)
        
        # Get the customer ID from the invoice notes
        customer_id = None
        if invoice.notes:
            import re
            customer_match = re.search(r'Stripe Customer ID: (cus_[a-zA-Z0-9]+)', invoice.notes)
            if customer_match:
                customer_id = customer_match.group(1)
        
        if not customer_id:
            # Try to find customer by email
            customer_email = invoice.booking.email
            existing_customers = stripe.Customer.list(email=customer_email, limit=1)
            if existing_customers and existing_customers.data:
                customer_id = existing_customers.data[0].id
        
        if not customer_id:
            raise ValueError("No customer ID found for this invoice")
        
        # Create and capture payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            customer=customer_id,
            payment_method=payment_method_id,
            off_session=True,  # This is an off-session payment
            confirm=True,      # Confirm the payment immediately
            metadata={
                'invoice_id': str(invoice.id),
                'invoice_number': invoice.invoice_number,
                'customer_name': invoice.booking.name,
                'customer_email': invoice.booking.email,
                'payment_type': 'capture'
            }
        )
        
        # Create payment record
        payment = Payment.objects.create(
            invoice=invoice,
            amount=Decimal(amount),
            payment_method=PaymentMethod.STRIPE,
            transaction_id=intent.id,
            payment_date=timezone.now()
        )
        
        return payment


# Factory for creating payment processors
class PaymentProcessorFactory:
    """
    Factory class for creating payment processor instances.
    This allows for easy addition of new payment processors.
    """
    
    @staticmethod
    def get_processor(processor_type):
        """
        Get a payment processor instance based on the type.
        
        Args:
            processor_type: The type of processor to create
            
        Returns:
            PaymentProcessor: An instance of the requested processor
            
        Raises:
            ValueError: If the processor type is not supported
        """
        if processor_type == 'stripe':
            return StripeProcessor()
        # Add more processors here as needed
        # elif processor_type == 'square':
        #     return SquareProcessor()
        # elif processor_type == 'paypal':
        #     return PayPalProcessor()
        else:
            raise ValueError(f"Unsupported payment processor: {processor_type}")


# Helper functions for invoice operations
def get_invoice_balance(invoice):
    """
    Calculate the balance due for an invoice.
    
    Args:
        invoice: The Invoice object
        
    Returns:
        Decimal: The balance due
    """
    # Get service items from the booking
    service_items = invoice.booking.service_items.all()
    
    # Calculate total price from service items or use base price if no items
    if service_items.exists():
        total_price = sum(item.price_at_booking * item.quantity for item in service_items)
    else:
        total_price = invoice.booking.service_offering.price if invoice.booking.service_offering else 0
    
    # Calculate payment totals
    payments = Payment.objects.filter(invoice=invoice, is_refunded=False)
    total_paid = sum(payment.amount for payment in payments)
    balance_due = total_price - total_paid
    
    return balance_due

def get_invoice_total(invoice):
    """
    Get the total amount for an invoice.
    
    Args:
        invoice: The Invoice object
        
    Returns:
        Decimal: The total amount
    """
    # Get service items from the booking
    service_items = invoice.booking.service_items.all()
    
    # Calculate total price from service items or use base price if no items
    if service_items.exists():
        total_price = sum(item.price_at_booking * item.quantity for item in service_items)
    else:
        total_price = invoice.booking.service_offering.price if invoice.booking.service_offering else 0
    
    return total_price

def update_invoice_status(invoice):
    """
    Update invoice status based on payments.
    
    Args:
        invoice: The Invoice object
    """
    balance_due = get_invoice_balance(invoice)
    
    if balance_due <= 0:
        invoice.status = InvoiceStatus.PAID
    elif balance_due < get_invoice_total(invoice):
        invoice.status = InvoiceStatus.PARTIALLY_PAID
    
    invoice.save()
