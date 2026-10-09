"""Demo 8: ELI5 CLI tool powered by local LLM.
Usage: python eli5.py "quantum computing"
Requires: pip install ollama
"""

import sys
import ollama


def eli5(topic: str) -> str:
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": "You explain topics simply, as if to a 5-year-old. "
                "Use analogies, short sentences, and no jargon. "
                "Keep it under 100 words.",
            },
            {"role": "user", "content": f"Explain: {topic}"},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eli5.py \"topic\"")
        sys.exit(1)
    topic = " ".join(sys.argv[1:])
    print(f"\n🧒 ELI5: {eli5(topic)}")
