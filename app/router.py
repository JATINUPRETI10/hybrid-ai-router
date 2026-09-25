import json
from app.llm import ask_llm


def route_query(query: str) -> dict:

    prompt = f"""
You are an intelligent routing system.

Your job is to decide whether a user query should be handled by
JEV or a general LLM.

Use JEV when the query is primarily:
- classification
- binary decision
- structured decision
- scoring
- risk assessment
- categorization
- selecting between predefined options

Use LLM when the query requires:
- explanation
- creative writing
- coding
- summarization
- open-ended reasoning
- general conversation
- detailed educational answers

Return ONLY valid JSON.
Do not use markdown.
Do not add any explanation outside the JSON.

If the route is "llm", return:

{{
  "route": "llm"
}}

If the route is "jev", return:

{{
  "route": "jev",
  "question": {{
    "type": "choice",
    "instructions": "Short and precise instruction describing the decision",
    "criteria": {{
      "option_1": "short label",
      "option_2": "short label"
    }}
  }}
}}

IMPORTANT RULES FOR CRITERIA:

1. Criteria values MUST be short, user-friendly labels.
2. Do NOT put explanations or full sentences inside criteria.
3. Prefer labels such as:
   - "high-risk"
   - "low-risk"
   - "fraudulent"
   - "legitimate"
   - "approved"
   - "rejected"
   - "relevant"
   - "not-relevant"
   - "positive"
   - "negative"

BAD:

"criteria": {{
  "option_1": "The transaction shows anomaly indicators such as an unusually large amount and unfamiliar location."
}}

GOOD:

"criteria": {{
  "option_1": "high-risk",
  "option_2": "low-risk"
}}

The "instructions" field can contain the actual explanation
of what JEV needs to determine.

For example, for:

"A customer suddenly makes a large transaction from an unfamiliar
location. Determine whether this transaction should be considered high-risk."

A good response is:

{{
  "route": "jev",
  "question": {{
    "type": "choice",
    "instructions": "Determine whether the transaction is high-risk based on the unusual amount and unfamiliar location.",
    "criteria": {{
      "option_1": "high-risk",
      "option_2": "low-risk"
    }}
  }}
}}

User query:
{query}
"""

    result = ask_llm(prompt)
    result = result["answer"]

    result = result.strip()

    # Remove markdown code fences if Gemini adds them
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    try:
        routing = json.loads(result)

        # Validate JEV response
        if routing.get("route") == "jev":

            question = routing.get(
                "question",
                {}
            )

            criteria = question.get(
                "criteria",
                {}
            )

            # Make sure JEV has usable criteria
            if (
                question.get("type") == "choice"
                and len(criteria) >= 2
            ):
                return routing

            # Invalid JEV structure -> fallback
            return {
                "route": "llm"
            }

        # Default route
        return {
            "route": "llm"
        }

    except json.JSONDecodeError:

        # Safe fallback
        return {
            "route": "llm"
        }