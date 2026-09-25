from app.llm import ask_llm
from app.jev import ask_jev

from app.pricing import (
    calculate_gemini_cost,
    calculate_jev_cost
)


# =========================================================
# GEMINI EXECUTION
# =========================================================

def execute_llm(query: str):

    result = ask_llm(query)

    input_tokens = result.get(
        "input_tokens",
        0
    )

    output_tokens = result.get(
        "output_tokens",
        0
    )

    cost = calculate_gemini_cost(
        input_tokens,
        output_tokens
    )

    return {

        "provider": "gemini",

        "answer": result.get(
            "answer",
            ""
        ),

        "latency_ms": result.get(
            "latency_ms",
            0
        ),

        "input_tokens": input_tokens,

        "output_tokens": output_tokens,

        "total_tokens": (
            input_tokens +
            output_tokens
        ),

        "cost": round(
            cost,
            8
        )

    }


# =========================================================
# JEV EXECUTION
# =========================================================

def execute_jev(
    query: str,
    question: dict
):

    result = ask_jev(
        query,
        question
    )

    # -----------------------------------------------------
    # Extract JEV response
    # -----------------------------------------------------

    response = result.get(
        "response",
        {}
    )

    data = response.get(
        "data",
        {}
    )

    jev_result = data.get(
        "result",
        {}
    )

    # -----------------------------------------------------
    # Usage
    # -----------------------------------------------------

    usage = jev_result.get(
        "usage",
        {}
    )

    # Support multiple possible naming formats
    input_tokens = (
        usage.get("input_tokens")
        or usage.get("inputTokens")
        or usage.get("prompt_tokens")
        or 0
    )

    output_tokens = (
        usage.get("output_tokens")
        or usage.get("outputTokens")
        or usage.get("completion_tokens")
        or 0
    )

    # -----------------------------------------------------
    # Decision
    # -----------------------------------------------------

    answers = jev_result.get(
        "answers",
        {}
    )

    decision = answers.get(
        "decision",
        {}
    )

    if not isinstance(decision, dict):
        decision = {}

    choice = decision.get(
        "choice"
    )

    # -----------------------------------------------------
    # Convert option_1 / option_2
    # into meaningful labels
    # -----------------------------------------------------

    criteria = question.get(
        "criteria",
        {}
    )

    if not isinstance(criteria, dict):
        criteria = {}

    if choice in criteria:

        decision_label = criteria[
            choice
        ]

    else:

        decision_label = choice or "Unknown"


    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    confidence = decision.get(
        "confidence"
    )

    if confidence is not None:

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = None


    # -----------------------------------------------------
    # Probabilities
    # -----------------------------------------------------

    probabilities = decision.get(
        "probabilities",
        {}
    )

    if not isinstance(
        probabilities,
        dict
    ):

        probabilities = {}


    # -----------------------------------------------------
    # Credits
    # -----------------------------------------------------

    credits_used = data.get(
        "creditsUsed",
        0
    )

    try:

        credits_used = float(
            credits_used
        )

    except (
        TypeError,
        ValueError
    ):

        credits_used = 0


    # -----------------------------------------------------
    # Cost
    # -----------------------------------------------------

    cost = calculate_jev_cost(
        credits_used
    )


    # -----------------------------------------------------
    # Server latency
    # -----------------------------------------------------

    server_latency = jev_result.get(
        "elapsedMs"
    )


    # -----------------------------------------------------
    # Final normalized JEV response
    # -----------------------------------------------------

    return {

        "provider": "jev",

        "answer": {

            "decision": decision_label,

            "confidence": confidence,

            "probabilities": probabilities

        },

        "latency_ms": result.get(
            "latency_ms",
            0
        ),

        "server_latency_ms": server_latency,

        "input_tokens": input_tokens,

        "output_tokens": output_tokens,

        "total_tokens": (
            input_tokens +
            output_tokens
        ),

        "credits_used": credits_used,

        "cost": round(
            cost,
            8
        )

    }


# =========================================================
# COMPARE JEV VS GEMINI
# =========================================================

def compare_backends(
    query: str,
    jev_question: dict,
    selected_provider: str
):

    # -------------------------
    # Execute both providers
    # -------------------------

    if selected_provider == "gemini":

        # Gemini is the selected/executed provider
        llm_result = execute_llm(query)

        # JEV is alternative
        try:
            jev_result = execute_jev(
                query,
                jev_question
            )
        except Exception as e:
            jev_result = {
                "provider": "jev",
                "answer": None,
                "latency_ms": None,
                "server_latency_ms": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "credits_used": 0,
                "cost": 0,
                "error": str(e)
            }

    else:

        # JEV is the selected/executed provider
        try:
            jev_result = execute_jev(
                query,
                jev_question
            )
        except Exception as e:
            jev_result = {
                "provider": "jev",
                "answer": None,
                "latency_ms": None,
                "server_latency_ms": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "credits_used": 0,
                "cost": 0,
                "error": str(e)
            }

        # Gemini is alternative
        llm_result = execute_llm(query)

    # -------------------------
    # Select executed provider
    # -------------------------

    if selected_provider == "gemini":

        executed = llm_result
        alternative = jev_result

    else:

        executed = jev_result
        alternative = llm_result

    # -------------------------
    # Comparison
    # -------------------------

    comparison = {
        "faster_provider": None,
        "time_difference_ms": None,
        "time_saved_percent": None,
        "cheaper_provider": None,
        "cost_difference": None,
        "jev_total_tokens": (
            jev_result["input_tokens"]
            + jev_result["output_tokens"]
        ),
        "gemini_total_tokens": (
            llm_result["input_tokens"]
            + llm_result["output_tokens"]
        )
    }

    # Latency comparison
    if (
        jev_result["latency_ms"] is not None
        and llm_result["latency_ms"] is not None
    ):

        jev_latency = jev_result["latency_ms"]
        gemini_latency = llm_result["latency_ms"]

        difference = abs(
            jev_latency - gemini_latency
        )

        if jev_latency < gemini_latency:
            faster = "jev"
            base = gemini_latency
        else:
            faster = "gemini"
            base = jev_latency

        comparison["faster_provider"] = faster
        comparison["time_difference_ms"] = round(
            difference,
            2
        )

        if base > 0:
            comparison["time_saved_percent"] = round(
                (difference / base) * 100,
                2
            )

    # Cost comparison
    jev_cost = jev_result["cost"]
    gemini_cost = llm_result["cost"]

    if jev_result.get("error") is None:

        comparison["cost_difference"] = round(
            abs(jev_cost - gemini_cost),
            8
        )

        if jev_cost < gemini_cost:
            comparison["cheaper_provider"] = "jev"

        elif gemini_cost < jev_cost:
            comparison["cheaper_provider"] = "gemini"

        else:
            comparison["cheaper_provider"] = "equal"

    return {
        "query": query,

        "selected_provider": selected_provider,

        "executed": executed,

        "alternative": alternative,

        "jev": jev_result,

        "gemini": llm_result,

        "comparison": comparison
    }