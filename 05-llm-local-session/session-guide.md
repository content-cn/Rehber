# Run LLMs Locally — Consolidated Session Guide

> **Duration:** 60–90 minutes | **Audience:** University students / early-career devs
> **Tone:** Informative, irreverent, meme-aware, critical of subscription costs

---

## PRE-SESSION CHECKLIST

- [ ] Ollama installed and running (`ollama serve`)
- [ ] Models pre-pulled: `llama3.1:8b`, `qwen2.5-coder:7b`, `phi3:mini`
- [ ] Python 3.8+ with `ollama` SDK installed (`pip install ollama`)
- [ ] Demo scripts in `demo-scripts/` tested and working
- [ ] Terminal font size ≥16pt for visibility
- [ ] Backup screenshots of expected outputs (in case of hardware issues)
- [ ] Slides loaded in presentation mode

---

## SESSION TIMELINE

| Time | Block | Key Activity |
|------|-------|-------------|
| 0:00–0:08 | **The Subscription Trap** | Hook: cost of AI subscriptions, data privacy |
| 0:08–0:18 | **Ollama Setup** | Live install + first model pull |
| 0:18–0:30 | **Model Zoo** | Pulling models, comparing sizes, choosing for tasks |
| 0:30–0:42 | **Agents Demystified** | What agents really are, live agent demo |
| 0:42–0:55 | **Tooling Ecosystem** | Python SDK, Open WebUI, building your own tools |
| 0:55–1:10 | **Harness Engineering** | Structured output, chaining, guardrails |
| 1:10–1:20 | **Wrap-Up & Resources** | Recap, Q&A, resource links |

---

## BLOCK 1 — THE SUBSCRIPTION TRAP (0:00–0:08)

### 📊 Slide: "The Real Cost of 'AI-Powered'"

**Narration:**

🗣️ *"Let's do some math. ChatGPT Plus: $20/month. Claude Pro: $20/month. Copilot: $19/month. That's $59/month — $708 a year — for the privilege of sending your code, your data, your half-baked ideas to someone else's server. And they can change the price, throttle you, or shut down your favorite model tomorrow."*

🗣️ *"Here's the alternative: you download a model, run it on your laptop, and it works offline, forever, for free. No API key. No credit card. No 'you've hit your daily limit' popup at 2am when you're debugging."*

**Key points:**
- $708/year across major subscriptions
- Data leaves your machine with every prompt
- Vendor lock-in: models deprecated, prices raised, features removed
- Local alternative: free, private, offline, permanent

---

## BLOCK 2 — OLLAMA SETUP (0:08–0:18)

### 📊 Slide: "Ollama — Your Local AI Runtime"

### Demo 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

**Expected output:**
```
==> Installing ollama...
✓ Ollama installed successfully
```

Start the server:
```bash
ollama serve
```

🗣️ *"That's it. One command. Ollama is now running on localhost:11434. No account, no API key, no terms of service to accept."*

### Demo 2: Pull Your First Model

```bash
ollama pull llama3.1:8b
```

**Expected output:**
```
pulling manifest...
pulling 8eeb52dfb3bb... 100% ▕████████████████▏ 4.7 GB
success
```

⚠️ **Fallback:** If download is slow on venue WiFi, have the model pre-pulled. Show `ollama list` instead.

### Demo 3: First Chat

```bash
ollama run llama3.1:8b "Explain recursion like I'm five"
```

🗣️ *"We just ran an 8-billion parameter language model. On this laptop. No internet required. Try doing that with ChatGPT."*

---

## BLOCK 3 — MODEL ZOO (0:18–0:30)

### 📊 Slide: "Model Selection Matrix"

| Size | RAM | Good For | Example |
|------|-----|----------|---------|
| 1–3B | 4 GB | Quick tasks, autocomplete | `phi3:mini` |
| 7–8B | 8 GB | Coding, summarization, chat | `llama3.1:8b`, `qwen2.5-coder:7b` |
| 13–14B | 16 GB | Complex reasoning | `llama3.1:13b` |
| 32–70B | 32–64 GB | Research, heavy analysis | `qwen2.5:32b` |

### Demo 4: Model Comparison — Same Prompt, Different Models

```bash
ollama run phi3:mini "Write a Python function to reverse a linked list"
```
Then:
```bash
ollama run qwen2.5-coder:7b "Write a Python function to reverse a linked list"
```

🗣️ *"See the difference? The 3B model gives you something that kind of works. The 7B coding model gives you production-ready code with edge case handling. Bigger isn't always better — but for code, a code-specialized model at 7B beats a general model at 13B."*

### Demo 5: Model Library Tour

```bash
ollama list
```

🗣️ *"Browse the full library at ollama.com/library. There are hundreds of models. Coding models, math models, uncensored models, vision models. All free. All local."*

⚠️ **Fallback:** If pulling a new model is slow, stick with pre-pulled models and show the web library on screen.

---

## BLOCK 4 — AGENTS DEMYSTIFIED (0:30–0:42)

### 📊 Slide: "Agents: What They Actually Are"

🗣️ *"Everyone says 'agents' like it's magic. It's not. An agent is an LLM that can call external tools. That's it. The loop is: Think → Act → Observe → Repeat."*

**The Agent Loop:**
1. **Think** — LLM decides what to do
2. **Act** — LLM calls a tool (function) via structured JSON
3. **Observe** — LLM reads the tool's output
4. **Repeat** — until the task is done

### Demo 6: Live Agent Demo

Run `demo-scripts/agent_demo.py`:

```bash
python demo-scripts/agent_demo.py
```

**Expected output:**
```
🤖 Agent: I need to check the weather. Let me call the weather tool.

📞 Tool Call: get_weather({"city": "London"})
📋 Tool Result: {"temp": 12, "condition": "cloudy", "humidity": 78}

🤖 Agent: The weather in London is 12°C and cloudy with 78% humidity.
```

🗣️ *"The LLM didn't actually check the weather — it told our code WHICH function to call and with WHAT arguments, as JSON. Our code ran the function and fed the result back. That's all an agent is. Think, Act, Observe, Repeat."*

---

## BLOCK 5 — TOOLING ECOSYSTEM (0:42–0:55)

### 📊 Slide: "Building on Top of Ollama"

**Three levels:**
1. **CLI** — `ollama run` for quick tasks
2. **SDK** — Python/JS libraries for programmatic access
3. **UI** — Open WebUI for a ChatGPT-like interface

### Demo 7: Python SDK — 5-Line Chat

Run `demo-scripts/quick_chat.py`:

```bash
python demo-scripts/quick_chat.py
```

```python
import ollama
response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
print(response["message"]["content"])
```

### Demo 8: Build Your Own CLI Tool

Run `demo-scripts/eli5.py`:

```bash
python demo-scripts/eli5.py "quantum computing"
```

**Expected output:**
```
🧒 ELI5: Quantum computing is like having a coin that can be
heads AND tails at the same time...
```

🗣️ *"In 25 lines of Python, we built a CLI tool that explains anything simply. No API key. No subscription. Works offline."*

### 📊 Slide: "Open WebUI — ChatGPT UI for Free"

```bash
# One-liner to run Open WebUI
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway ghcr.io/open-webui/open-webui:main
```

🗣️ *"If you want a ChatGPT-like interface, Open WebUI gives you exactly that — connected to your local Ollama. Multi-model chat, conversation history, image generation, all running locally."*

---

## BLOCK 6 — HARNESS ENGINEERING (0:55–1:10)

### 📊 Slide: "Harness Engineering — Making LLMs Reliable"

🗣️ *"Prompt engineering is step one. Harness engineering is everything else: structured output, chaining, guardrails, retry logic. It's the difference between a toy demo and something you'd actually ship."*

**Four pillars:**
1. **Structured Output** — Force JSON, not prose
2. **Chaining** — Multi-step pipelines
3. **Guardrails** — Validate outputs, retry on failure
4. **System Prompts** — Lock behavior and persona

### Demo 9: Structured JSON Output

Run `demo-scripts/json_demo.py`:

```bash
python demo-scripts/json_demo.py
```

**Expected output:**
```json
{
  "language": "Python",
  "paradigm": "multi-paradigm",
  "typing": "dynamic",
  "year_created": 1991,
  "creator": "Guido van Rossum"
}
```

🗣️ *"We told the model to output JSON and set the format to 'json'. This isn't the model being helpful — it's a hard constraint. The output is machine-parseable every time."*

### Demo 10: Multi-Step Chain

Run `demo-scripts/chain_demo.py`:

```bash
python demo-scripts/chain_demo.py
```

**Expected output:**
```
📝 Step 1 — Code Review:
Issues found: missing error handling, no input validation...

🔧 Step 2 — Auto-Fix:
Fixed code with added try/except and type checks...

✅ Step 3 — Test Generation:
Generated 3 test cases covering edge cases...
```

🗣️ *"Three LLM calls, chained. The output of the review feeds into the fix, and the fix feeds into the test generator. This is harness engineering — orchestrating multiple LLM calls into a reliable pipeline."*

---

## BLOCK 7 — WRAP-UP & Q&A (1:10–1:20)

### 📊 Slide: "What You Learned Today"

| Topic | Key Takeaway |
|-------|-------------|
| **Ollama** | One command to run LLMs locally. No cloud, no API key. |
| **Models** | Match model size to task. 7B for coding, 13B+ for reasoning. |
| **Agents** | LLM + tool calling. Think → Act → Observe → Repeat. |
| **Tooling** | Python SDK, CLI tools, Open WebUI — build whatever you want. |
| **Harness Engineering** | Structured output + chaining + guardrails = production-ready. |

### 📊 Slide: "Resources"

- **Ollama:** https://ollama.com
- **Model Library:** https://ollama.com/library
- **Python SDK:** https://github.com/ollama/ollama-python
- **Open WebUI:** https://github.com/open-webui/open-webui
- **Hugging Face:** https://huggingface.co

🗣️ *"You now have everything you need to run AI locally, build tools on top of it, and never pay $20/month again. The models are free. The tools are free. The only cost is the electricity to run your laptop. Go build something."*

---

## CONTINGENCY TABLE

| Problem | Solution |
|---------|----------|
| WiFi down during model pull | Use pre-pulled models. Show `ollama list`. |
| Model generates garbage | Switch to a different model or re-run. "Even GPT-4 has bad days." |
| Ollama crashes | Restart with `ollama serve`. Have backup terminal ready. |
| Demo script errors | Show the code and expected output from backup screenshots. |
| Runs over time | Cut the Open WebUI demo (Block 5) and go straight to Harness Engineering. |
| Student asks about GPU | "Ollama auto-detects NVIDIA/Apple Silicon GPUs. No config needed." |

---

## POST-SESSION SHARING

Share with attendees:
1. This guide (PDF or link)
2. All demo scripts from `demo-scripts/`
3. The slides
4. Links from the Resources slide
