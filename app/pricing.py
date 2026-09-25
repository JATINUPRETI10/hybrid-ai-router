# Keep provider pricing centralized.
# Values should be updated according to the actual API pricing.

GEMINI_INPUT_COST_PER_1M = 0.0
GEMINI_OUTPUT_COST_PER_1M = 0.0

JEV_COST_PER_CREDIT = 0.0


def calculate_gemini_cost(input_tokens, output_tokens):
    input_cost = (
        input_tokens / 1_000_000
    ) * GEMINI_INPUT_COST_PER_1M

    output_cost = (
        output_tokens / 1_000_000
    ) * GEMINI_OUTPUT_COST_PER_1M

    return input_cost + output_cost


def calculate_jev_cost(credits_used):
    return credits_used * JEV_COST_PER_CREDIT