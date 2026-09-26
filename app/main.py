from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm import ask_llm
from app.jev import ask_jev
from app.router import route_query
from app.executor import (
    execute_llm,
    execute_jev,
    compare_backends
)

app = FastAPI(
    title="Hybrid AI Router",
    description="Intelligent routing between JEV and Gemini",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://hybrid-ai-router-pink.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class QueryRequest(BaseModel):
    query: str


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Hybrid AI Router is running"
    }


# --------------------------------------------------
# Test Gemini
# --------------------------------------------------

@app.get("/test")
def test_llm():

    result = ask_llm(
        "Explain what an LLM is in one simple sentence."
    )

    return result


# --------------------------------------------------
# Route Query
# --------------------------------------------------

@app.post("/route")
def route(request: QueryRequest):

    selected_route = route_query(
        request.query
    )

    return {
        "query": request.query,
        "route": selected_route
    }


# --------------------------------------------------
# Test JEV
# --------------------------------------------------

@app.get("/test-jev")
def test_jev():

    result = ask_jev(
        "A customer says they were charged twice for the same order. "
        "What type of task is this?"
    )

    return result


# --------------------------------------------------
# Chat
# --------------------------------------------------

@app.post("/chat")
def chat(request: QueryRequest):

    # 1. Ask routing LLM
    routing = route_query(
        request.query
    )

    selected_route = routing["route"]


    # 2. Execute selected backend
    if selected_route == "jev":

        result = execute_jev(
            request.query,
            routing["question"]
        )

    else:

        result = execute_llm(
            request.query
        )


    # 3. Return normalized response
    return {
        "query": request.query,
        "route": selected_route,
        "execution": result
    }


@app.post("/compare")
def compare(request: QueryRequest):

    # Route the query
    routing = route_query(request.query)

    selected_route = routing["route"]

    # JEV query
    if selected_route == "jev":

        jev_question = routing["question"]

        result = compare_backends(
    request.query,
    jev_question,
    routing["route"]
)
        result["routing"] = {
            "selected_provider": "jev",
            "confidence": routing.get("confidence")
        }

        return result

    # Gemini query
    else:

        gemini_result = execute_llm(
            request.query
        )

        return {
            "query": request.query,

            "routing": {
                "selected_provider": "gemini",
                "confidence": routing.get("confidence")
            },

            "gemini": gemini_result,

            "jev": None,

            "comparison": {
                "status": "not_available",
                "reason": "JEV requires a structured decision task."
            }
        }