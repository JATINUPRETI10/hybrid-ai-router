
# Hybrid AI Router

> An intelligent AI routing system that automatically selects the most suitable AI backend based on the nature of the user query.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4)
![AI Routing](https://img.shields.io/badge/AI-Intelligent%20Routing-purple)

---

## Project Overview

Hybrid AI Router is a hybrid AI system designed to intelligently route user queries between different AI backends.

Instead of sending every query to the same model, the system first analyzes the nature of the query and determines which backend is more appropriate.

The current architecture supports:

- **JEV** — structured decision-oriented tasks
- **Google Gemini** — general-purpose reasoning and conversational tasks

The goal is to build a performance-aware AI routing layer that can select the appropriate model based on the characteristics of the incoming query.

---

## Features

- LLM-based query routing
- Automatic backend selection
- Google Gemini integration
- JEV backend integration
- Backend comparison
- Confidence-aware routing
- FastAPI backend
- React frontend
- Production deployment support
- Environment-based API key configuration
- CORS configuration for frontend-backend communication

---

## Architecture

```text
                    +---------------------+
                    |      User Query     |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |   React Frontend    |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |     FastAPI API     |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |   Routing Engine    |
                    |                     |
                    | Query Classification|
                    | + Route Selection   |
                    +----------+----------+
                               |
                  +------------+------------+
                  |                         |
                  v                         v
          +---------------+         +---------------+
          |      JEV      |         |    Gemini     |
          |               |         |               |
          | Decision /    |         | General AI /  |
          | Structured    |         | Reasoning     |
          | Tasks         |         | Tasks         |
          +-------+-------+         +-------+-------+
                  |                         |
                  +------------+------------+
                               |
                               v
                    +---------------------+
                    |  Normalized Result  |
                    +---------------------+
```

## Core Features

- Intelligent query routing between JEV and Gemini
- LLM-based query classification
- Structured decision-task handling through JEV
- General reasoning and knowledge tasks through Gemini
- Backend comparison for supported queries
- FastAPI REST API
- React-based frontend
- CORS-enabled production API
- Environment-based API key configuration
- Normalized API responses
- Production deployment support

## Routing Logic

The system analyzes the incoming query before selecting the appropriate backend.

### JEV

JEV is selected for structured decision-oriented tasks such as:

- Fraud detection
- Transaction classification
- Risk assessment
- Binary or categorical decisions
- Structured prediction tasks

### Gemini

Gemini is selected for general-purpose tasks such as:

- General questions
- Explanations
- Reasoning
- Summarization
- Knowledge-based queries
- Open-ended generation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/test` | Test Gemini integration |
| GET | `/test-jev` | Test JEV integration |
| POST | `/route` | Classify and route a query |
| POST | `/chat` | Route and execute a query |
| POST | `/compare` | Compare available backend responses |

## Example Request

```json
{
  "query": "Determine whether this transaction is fraudulent or legitimate."
}

```
## Example Routing Response
```json
{
  "query": "Determine whether this transaction is fraudulent or legitimate.",
  "route": "jev"
}
```
## Example Chat Response
```json
{
  "query": "What is machine learning?",
  "route": "gemini",
  "execution": {
    "provider": "gemini"
  }
}
```
# Technology Stack
## Frontend
-React
-JavaScript
-Vite
-CSS
## Backend
-Python
-FastAPI
-Pydantic
-Uvicorn
## AI
Gemini
-JEV
-LLM-based routing
