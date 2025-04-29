🧠 Project Summary – AI-Powered Appointment Assistant for Industry-Specific Businesses
Overview
This is a SaaS web application designed to help businesses in specific industries (like cleaning services, real estate, etc.) capture, engage, and convert leads using AI voice/SMS agents. Leads are received via webhooks, stored in a PostgreSQL database, and followed up by AI agents using Twilio for communication and OpenAI for smart response generation.

✅ Key Features
Webhook Integration: Accept leads from external platforms via custom webhook endpoints.

Industry Customization: Each business type (industry) has its own unique form fields and logic.

Dynamic Forms: Based on the industry, show different HTML form fields for data input (e.g., square footage for cleaning, location for real estate).

AI Assistants:

SMS Agent: Sends personalized messages to leads using Twilio.

Voice Agent: Makes automated calls to gather lead info or confirm appointments.

Task Scheduling: Use Django Q2 (no Celery/Redis) to schedule follow-ups or delayed messages.

Plugin-Based Architecture: Flexible system where industries, fields, and lead handlers are modular and pluggable.

Admin Dashboard: Manage businesses, leads, industry fields, and message templates.

🛠️ Tech Stack
Backend
Django (core framework)

Python

PostgreSQL

Django Q2 (task scheduling)

OpenAI (AI text generation)

Twilio (SMS & Voice integration)

Frontend
HTML5

Bootstrap

Vanilla JavaScript

Custom CSS

📦 Architecture Highlights
Modular Plugin-Based Design: Easily extend to new industries without touching core code.

Dynamic Form Generation: Render industry-specific forms using DB-configured fields.

AI Response Rules: Use OpenAI prompts tailored per industry to collect relevant data.

Queue System: Background task execution (e.g., send SMS after lead added) via Django Q2.

No login or user roles in current phase.