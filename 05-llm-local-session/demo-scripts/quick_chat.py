"""Demo 7: Minimal Python SDK usage — 5-line chat.
Requires: pip install ollama
"""

import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
print(response["message"]["content"])
