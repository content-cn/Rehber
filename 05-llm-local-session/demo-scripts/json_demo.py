"""Demo 9: Forcing structured JSON output from LLM.
Requires: pip install ollama
"""

import json
import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {
            "role": "system",
            "content": "You are a technical encyclopedia. Always respond in valid JSON only.",
        },
        {
            "role": "user",
            "content": "Give me facts about Python: language, paradigm, typing, year_created, creator",
        },
    ],
    format="json",
)

data = json.loads(response["message"]["content"])
print(json.dumps(data, indent=2))
