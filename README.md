KAYA AI

Multilingual AI-Powered Medication Assistance System

Healthcare technology that speaks your language.

KAYA AI is an AI-powered medication assistance system designed to make medication-related support simpler, more accessible, and more natural through conversational AI, voice interaction, multilingual communication, medication assistance, and reminders.

🌐 Live Prototype

KAYA AI 1.0:
https://kaya-ai.streamlit.app/

💡 The Problem

Managing medications can become difficult for many users.

Common challenges include:

Forgetting medication schedules

Managing multiple medicines

Understanding medication-related information

Language barriers

Difficulty using complicated digital interfaces

Need for simple and natural assistance

KAYA was designed to address these challenges through an AI-based conversational interface.

🚀 Our Solution

KAYA AI provides a simple way for users to interact with a medication-focused AI assistant using text and voice.

The core concept combines:

Conversational AI + Voice Interaction + Multilingual Support + Medication Assistance + Reminders

✨ Key Features

🤖 AI Conversational Assistant — understands natural-language requests and generates conversational responses.

🗣️ Voice Interaction — enables natural voice-based interaction.

🌐 Multilingual Interaction — supports interaction across supported languages.

💊 Medication Assistance — provides medication-focused assistance and information.

⏰ Medication Reminders — supports medication schedules and reminders.

🖥️ Simple Interface — built around a straightforward Streamlit experience.

⚙️ How KAYA Works

             USER
               │
               ▼
        Voice / Text Input
               │
               ▼
        KAYA 1.0 Application
               │
               ▼
        AI / Application Logic
          ┌────┼────┐
          │    │    │
          ▼    ▼    ▼
         AI  Medication  Reminders
          │    │    │
          └────┼────┘
               ▼
        Response Generation
               │
          ┌────┴────┐
          ▼         ▼
        Text      Voice
          │         │
          └────┬────┘
               ▼
              USER

Step-by-step

The user provides a request through text or voice.

Voice input is processed when voice interaction is used.

KAYA processes the request through its application and AI layer.

Relevant medication or reminder functionality can be used when applicable.

The AI generates a response.

The response is displayed and/or delivered through voice output.

🧠 AI Architecture

KAYA is an application that uses generative AI, rather than a newly trained large language model.

User
  ↓
KAYA Interface
  ↓
Input Processing
  ↓
Generative AI
  ↓
KAYA Application Logic
  ↓
Response
  ↓
User

The AI layer allows KAYA to understand natural-language requests and generate conversational responses.

🎙️ Voice System

Microphone
    ↓
Speech Processing
    ↓
Text / User Request
    ↓
KAYA AI
    ↓
AI Response
    ↓
Text-to-Speech
    ↓
Speaker

Voice technologies used in the project include voice processing and Edge TTS for text-to-speech output.

🌍 Multilingual Interaction

KAYA is designed to make medication assistance more accessible beyond English.

The AI-based conversational approach allows KAYA to process supported multilingual requests and respond conversationally.

💊 Medication Assistance

KAYA includes medication-focused functionality intended to help users interact with medication-related information and routines.

Important: KAYA is an assistance tool and is not intended to replace qualified doctors, pharmacists, or other healthcare professionals.

⏰ Reminder System

KAYA includes functionality related to medication reminders, intended to help users organize medication schedules and maintain their routine.

🛠️ Technology Stack

Technology

Purpose

Python

Core programming language

Streamlit

KAYA 1.0 user interface

Google GenAI

Generative AI integration

Edge TTS

Text-to-speech

Voice Processing

Voice interaction

JSON / Application Storage

Application data handling

📁 Project Structure

KAYA_AI/
│
├── app.py
├── ai.py
├── api_server.py
├── local_ai.py
├── voice.py
├── tts.py
├── medication.py
├── medicines.py
├── reminders.py
├── documents.py
├── documents.json
├── medications.json
├── requirements.txt
├── .gitignore
│
├── .streamlit/
├── documents/
├── medical_reports/
│
└── kaya-2.0/

Important files

app.py — Main Streamlit application and user interface.

ai.py — AI integration.

voice.py — Voice-related functionality.

tts.py — Text-to-speech functionality.

medication.py / medicines.py — Medication functionality.

reminders.py — Reminder functionality.

documents.py — Document-related functionality.

api_server.py — API/backend-related functionality where applicable.

local_ai.py — Local AI experimentation/integration component.

requirements.txt — Python dependencies.

▶️ Running KAYA Locally

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd KAYA_AI

2. Create a virtual environment

python -m venv venv

Windows

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file and add the required API configuration.

Example:

GOOGLE_API_KEY=your_api_key_here

Never publish real API keys or secrets to GitHub.

5. Start KAYA

streamlit run app.py

🔐 Security

API keys and other secrets should be stored in environment variables rather than directly inside source code.

The .env file should remain excluded from the public repository through .gitignore.

Never commit a real API key to GitHub.

🧪 Current Prototype

KAYA 1.0

KAYA 1.0 is the current working Streamlit prototype.

The prototype demonstrates the core software and AI concept, including:

Conversational AI

Voice interaction

Multilingual interaction

Medication assistance

Reminder functionality

Streamlit-based user interface

Only functionality implemented and working in the current prototype should be considered part of KAYA 1.0.

💡 What Makes KAYA Different?

KAYA combines:

Conversational AI
       +
Voice Interaction
       +
Multilingual Access
       +
Medication Assistance
       +
Reminders
       ↓
     KAYA

Rather than being only a reminder application or only a chatbot, KAYA is designed around a conversational medication-assistance experience.

🚧 Future Development

KAYA 2.0

KAYA 2.0 is a separate future development phase.

Potential areas include:

Modern Next.js web interface

Improved AI capabilities

Greater personalization

Caregiver integration

Potential IoT / smart-device integration

These are future development and are not presented as completed KAYA 1.0 features.

⚠️ Disclaimer

KAYA AI is a technology prototype intended to demonstrate AI-powered medication assistance.

It does not replace professional medical advice, diagnosis, or treatment.

Users should consult qualified healthcare professionals for medical decisions.

🎯 Project Vision

KAYA aims to make healthcare technology more accessible by allowing people to communicate naturally with an intelligent medication assistant.

The long-term vision is:

AI + Voice + Language + Medication Assistance + Personalization

👥 Team

Team Name: <YOUR TEAM NAME>

College / Institution: <YOUR COLLEGE NAME>

Team Members:

<Prasad Patankar>

<Chittaranjan Bhalero>

< Aryan Hatagle>


🔗 Links

Live Prototype:
https://kaya-ai.streamlit.app/

GitHub Repository:
<https://github.com/prasad-patankar-ship-it/KAYA_AI>

Demo Video:
<YOUR VIDEO URL>

KAYA AI

Healthcare technology that speaks your language.
