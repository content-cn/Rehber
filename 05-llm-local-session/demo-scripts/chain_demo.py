"""Demo 10: Multi-step LLM chain — Review → Fix → Test.
Requires: pip install ollama
"""

import ollama

SAMPLE_CODE = '''
def process_order(order):
    total = order["items"][0]["price"] * order["quantity"]
    db.save(order)
    send_email(order["email"], "Order confirmed", f"Total: ${total}")
    return total
'''


def chain_step(model: str, system_prompt: str, user_prompt: str, label: str) -> str:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    result = response["message"]["content"]
    print(result)
    return result


def run_chain():
    model = "qwen2.5-coder:7b"

    # Step 1: Code Review
    review = chain_step(
        model=model,
        system_prompt=(
            "You are a senior code reviewer. List every bug, edge case, "
            "and improvement. Be specific about line numbers and issues."
        ),
        user_prompt=f"Review this code:\n```python\n{SAMPLE_CODE}\n```",
        label="📝 Step 1 — Code Review",
    )

    # Step 2: Auto-Fix (uses review output)
    fixed = chain_step(
        model=model,
        system_prompt=(
            "You are a senior Python developer. Given a code review, "
            "rewrite the function to fix ALL issues mentioned. "
            "Output only the corrected Python code."
        ),
        user_prompt=f"Original code:\n```python\n{SAMPLE_CODE}\n```\n\nReview findings:\n{review}\n\nFix all issues.",
        label="🔧 Step 2 — Auto-Fix",
    )

    # Step 3: Test Generation (uses fixed code)
    chain_step(
        model=model,
        system_prompt=(
            "You are a test engineer. Write pytest tests for the given function. "
            "Cover happy path, edge cases, and error scenarios. "
            "Output only the test code."
        ),
        user_prompt=f"Write tests for this function:\n```python\n{fixed}\n```",
        label="✅ Step 3 — Test Generation",
    )


if __name__ == "__main__":
    run_chain()
