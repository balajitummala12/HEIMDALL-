<div align="center">

<img src="Version-5/Frontend/logo.png" width="220" height="220" alt="HEIMDALL Logo" style="border-radius: 50%; object-fit: cover;" />

# ⚡ HEIMDALL V5

### An Intelligent AI Assistant • Built to Think, Respond & Evolve

![Version](https://img.shields.io/badge/Version-V5-7c3aed?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)

<br/>

**HEIMDALL is an AI-powered assistant built with a dedicated frontend and backend architecture.**

</div>

---

# 🧠 About HEIMDALL

> **"The goal was never to build just another chatbot."**

HEIMDALL V5 is the fifth major evolution of my AI assistant project.

What started as a simple AI assistant gradually went through multiple versions, experiments, rewrites, failures, improvements, and architectural changes.

With Version 5, the focus shifted toward building a more structured application by separating the user interface from the backend AI system.

Instead of keeping everything inside one large script, HEIMDALL is organized into different components responsible for handling requests, processing conversations, managing context, connecting with AI models, and supporting additional functionality.

The goal is simple:

### **Build an AI assistant as a complete system — not just a chat box connected to an API.**

---

# ✨ What HEIMDALL Can Do

## 💬 AI Conversations

HEIMDALL allows users to interact with the assistant through a dedicated chat interface.

User messages are sent from the frontend to the backend, processed through the AI system, and returned as responses.

The application is designed around a complete frontend-to-backend communication flow rather than a standalone script.

---

## 🧠 Intent Detection

The backend analyzes user input to better understand what the user is asking for.

This helps HEIMDALL process different types of requests through the appropriate logic before generating a response.

---

## 🧩 Context-Aware Responses

HEIMDALL maintains conversation context so that responses can take the ongoing interaction into account instead of treating every message as completely unrelated.

This helps make conversations feel more connected and natural.

---

## 🔀 AI Model Integration

The assistant connects to an AI provider through the backend to generate intelligent responses.

The AI integration is separated from the main application flow, helping keep the backend organized and easier to work with.

---

## 🔎 Web Search Integration

For requests that require external or up-to-date information, HEIMDALL includes web search integration.

This allows the assistant to retrieve information beyond its normal conversational responses when needed.

---

## 🎙️ Voice Support

HEIMDALL V5 includes voice-related functionality as part of the assistant system.

The backend contains support for processing voice-based interaction alongside the text-based chat experience.

---

## 🎨 Dedicated User Interface

HEIMDALL includes a custom-built frontend instead of relying on a basic terminal interface.

The current interface includes dedicated pages for:

- 🏠 **Home**
- 💬 **Chat**
- 🕘 **Conversation History**
- ⚙️ **Settings**
- 📱 **Mobile Interface**

The frontend and backend are maintained as separate parts of the Version 5 architecture.

---

# 🏗️ Project Structure

```text
HEIMDALL
│
└── Version-5
    │
    ├── 🎨 Frontend
    │   │
    │   ├── Home Interface
    │   ├── Chat Interface
    │   ├── Conversation History
    │   ├── Settings
    │   └── Mobile Interface
    │
    └── 🧠 Backend
        │
        ├── AI Processing
        ├── Intent Detection
        ├── Context Handling
        ├── AI Providers
        ├── Search Integration
        ├── Voice Functionality
        ├── Memory & Profile
        ├── System Services
        └── API
