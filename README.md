# 🚦 Hybrid AI Router

> An intelligent AI routing system that automatically selects the most suitable AI backend based on the nature of the user query.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4)
![AI Routing](https://img.shields.io/badge/AI-Intelligent%20Routing-purple)

---

## 🔗 Project Overview

**Hybrid AI Router** is a hybrid AI system designed to intelligently route user queries between different AI backends.

Instead of sending every query to the same model, the system first analyzes the nature of the query and determines which backend is more appropriate.

The current architecture supports:

- **JEV** — structured decision-oriented tasks
- **Google Gemini** — general-purpose reasoning and conversational tasks

The goal is to build a **performance-aware AI routing layer** that can select the appropriate model based on the characteristics of the incoming query.

---

## ✨ Features

- 🧠 **LLM-based query routing**
- 🔀 Automatic backend selection
- 🤖 Google Gemini integration
- ⚡ JEV backend integration
- 📊 Backend comparison
- 🎯 Confidence-aware routing
- 🚀 FastAPI backend
- ⚛️ React frontend
- 🌐 Production deployment support
- 🔐 Environment-based API key configuration
- 🛡️ CORS configuration for frontend-backend communication

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      User Query     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Frontend    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Routing Engine    │
                    │                     │
                    │ Query Classification│
                    │ + Route Selection   │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
          ┌───────────────┐         ┌───────────────┐
          │      JEV      │         │    Gemini     │
          │               │         │               │
          │ Decision /    │         │ General AI /  │
          │ Structured    │         │ Reasoning      │
          │ Tasks         │         │ Tasks          │
          └───────┬───────┘         └───────┬───────┘
                  │                         │
                  └────────────┬────────────┘
                               ▼
                    ┌─────────────────────┐
                    │  Normalized Result  │
                    └─────────────────────┘
