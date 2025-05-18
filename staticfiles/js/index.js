/**
 * Index JavaScript for AI Appointment Assistant Landing Page
 * Handles landing page specific functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize smooth scrolling for anchor links
    initSmoothScroll();
    
    // Add animation to features on scroll
    initFeatureAnimations();
    
    // Add animation to testimonials on scroll
    initTestimonialAnimations();
    
    // Add animation to industry cards on scroll
    initIndustryCardAnimations();
});

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (!targetElement) return;
            
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        });
    });
}

/**
 * Initialize animations for feature cards on scroll
 */
function initFeatureAnimations() {
    const featureCards = document.querySelectorAll('.features-section .card');
    
    if (featureCards.length === 0 || !window.IntersectionObserver) return;
    
    const featureObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a slight delay for each card to create a cascade effect
                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, index * 100);
                
                // Unobserve after animation is applied
                featureObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    featureCards.forEach(card => {
        card.classList.add('feature-card-hidden');
        featureObserver.observe(card);
    });
}

/**
 * Initialize animations for testimonial cards on scroll
 */
function initTestimonialAnimations() {
    const testimonialCards = document.querySelectorAll('.testimonials-section .card');
    
    if (testimonialCards.length === 0 || !window.IntersectionObserver) return;
    
    const testimonialObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a slight delay for each card to create a cascade effect
                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, index * 150);
                
                // Unobserve after animation is applied
                testimonialObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    testimonialCards.forEach(card => {
        card.classList.add('testimonial-card-hidden');
        testimonialObserver.observe(card);
    });
}

/**
 * Initialize animations for industry cards on scroll
 */
function initIndustryCardAnimations() {
    const industryCards = document.querySelectorAll('.industry-card');
    
    if (industryCards.length === 0 || !window.IntersectionObserver) return;
    
    const industryObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a slight delay for each card to create a cascade effect
                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, index * 100);
                
                // Unobserve after animation is applied
                industryObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    industryCards.forEach(card => {
        card.classList.add('industry-card-hidden');
        industryObserver.observe(card);
    });
}

/**
 * Add CSS animations to index.css dynamically
 * This adds the necessary CSS for the animations initialized above
 */
(function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        /* Feature card animations */
        .feature-card-hidden {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .feature-card-hidden.animated {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Testimonial card animations */
        .testimonial-card-hidden {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .testimonial-card-hidden.animated {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Industry card animations */
        .industry-card-hidden {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .industry-card-hidden.animated {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
})();
