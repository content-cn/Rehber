# Run LLMs Locally — Slide Deck Contents

---

## Slide 1: Title
**Run LLMs Locally**
*Stop Paying. Start Owning.*
[Your Name] | [Date] | [University/Event Name]

---

## Slide 2: The Subscription Trap
- ChatGPT Plus: $20/mo
- Claude Pro: $20/mo
- GitHub Copilot: $19/mo
- **Total: $708/year**
- Your data leaves your machine with every prompt
- Prices go up. Models get deprecated. Features get paywalled.

---

## Slide 3: The Alternative
- **Ollama** — run LLMs locally
- One command install
- No account. No API key. No internet required.
- Your data never leaves your laptop
- Models are free. Forever.

---

## Slide 4: What is Ollama?
- Local LLM runtime
- Supports 100+ open-source models
- macOS, Linux, Windows
- REST API on `localhost:11434`
- GPU auto-detection (NVIDIA, Apple Silicon)

---

## Slide 5: Demo — Install Ollama
```bash
brew install ollama   # macOS
ollama serve          # Start server
ollama pull llama3.1:8b
```
*[LIVE DEMO]*

---

## Slide 6: Demo — First Chat
```bash
ollama run llama3.1:8b "Explain recursion like I'm five"
```
*[LIVE DEMO]*

---

## Slide 7: Model Selection Matrix
| Size | RAM | Best For | Example |
|------|-----|----------|---------|
| 1–3B | 4 GB | Quick tasks | `phi3:mini` |
| 7–8B | 8 GB | Coding, chat | `llama3.1:8b` |
| 13–14B | 16 GB | Complex reasoning | `llama3.1:13b` |
| 32–70B | 32+ GB | Research | `qwen2.5:32b` |

---

## Slide 8: Choosing the Right Model
- **Coding?** → `qwen2.5-coder:7b`
- **General chat?** → `llama3.1:8b`
- **Tiny & fast?** → `phi3:mini`
- **Maximum quality?** → `qwen2.5:32b` (if you have the RAM)
- Browse: https://ollama.com/library

---

## Slide 9: Demo — Model Comparison
Same prompt, two models:
```bash
ollama run phi3:mini "Reverse a linked list in Python"
ollama run qwen2.5-coder:7b "Reverse a linked list in Python"
```
*[LIVE DEMO]*

---

## Slide 10: Agents — The Buzzword
"AI Agents" = an LLM that can call tools.
That's it. No magic.

---

## Slide 11: The Agent Loop
```
Think → Act → Observe → Repeat
```
1. LLM decides what to do
2. LLM calls a function (via JSON)
3. Your code runs the function
4. Result fed back to LLM
5. Repeat until done

---

## Slide 12: Demo — Agent in Action
```bash
python demo-scripts/agent_demo.py
```
*[LIVE DEMO — watch the Think→Act→Observe loop]*

---

## Slide 13: Tooling — Three Levels
1. **CLI** — `ollama run` (quick tasks)
2. **SDK** — Python/JS (build apps)
3. **UI** — Open WebUI (ChatGPT clone)

---

## Slide 14: Python SDK — 5 Lines
```python
import ollama
response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response["message"]["content"])
```

---

## Slide 15: Demo — Build a CLI Tool
```bash
python demo-scripts/eli5.py "quantum computing"
```
*[LIVE DEMO]*

---

## Slide 16: Open WebUI
- ChatGPT-like interface for your local models
- Multi-model support, conversation history
- One Docker command to run:
```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/open-webui/open-webui:main
```

---

## Slide 17: Harness Engineering
**Beyond prompt engineering:**
1. Structured Output — force JSON
2. Chaining — multi-step pipelines
3. Guardrails — validate + retry
4. System Prompts — lock behavior

---

## Slide 18: Demo — JSON Output
```bash
python demo-scripts/json_demo.py
```
*[LIVE DEMO — machine-parseable output every time]*

---

## Slide 19: Demo — Multi-Step Chain
```bash
python demo-scripts/chain_demo.py
```
Review → Fix → Test — three LLM calls, chained.
*[LIVE DEMO]*

---

## Slide 20: Prompt Engineering Tips
- Be specific: "Output only valid JSON" beats "give me JSON"
- Use system prompts to set persona
- Provide examples (few-shot)
- Set temperature: 0 for deterministic, 0.7 for creative

---

## Slide 21: When Local Beats Cloud
| Local (Ollama) | Cloud (ChatGPT/Claude) |
|---------------|----------------------|
| Free forever | $20+/month |
| Data stays private | Data sent to cloud |
| Works offline | Requires internet |
| You control the model | They control the model |
| Slightly slower (CPU) | Fast (GPU clusters) |

---

## Slide 22: When Cloud Still Wins
- Cutting-edge reasoning (GPT-4o, Claude 3.5 Sonnet)
- Very large context windows (100K+ tokens)
- Multimodal (vision, audio, video)
- Team features (shared workspaces)
- But the gap is closing fast.

---

## Slide 23: The Stack
```
Your App
    ↓
Python SDK / REST API
    ↓
Ollama (localhost:11434)
    ↓
Open-source Model (llama3, qwen, deepseek...)
    ↓
Your Hardware (CPU / GPU)
```

---

## Slide 24: What You Learned
- ✅ Install and run Ollama
- ✅ Choose models for different tasks
- ✅ Build agents with tool calling
- ✅ Use the Python SDK
- ✅ Force structured output (JSON)
- ✅ Chain multiple LLM calls
- ✅ Never pay $20/month again

---

## Slide 25: Resources
- **Ollama:** https://ollama.com
- **Model Library:** https://ollama.com/library
- **Python SDK:** https://github.com/ollama/ollama-python
- **Open WebUI:** https://github.com/open-webui/open-webui
- **Hugging Face:** https://huggingface.co

---

## Slide 26: Thank You / Q&A
*"Go build something. The models are free. The tools are free. The only cost is electricity."*

[Your contact / socials]
