# AI Use Cases — Complete Repository

Scripts, sample apps, prompts, and references for 5 fully implemented AI use cases — plus a master CSV covering 14 total.

---

## Repository Structure

```
.
├── ai_use_cases.csv                          # Master CSV: 14 use cases
│
├── 01-ai-pr-review/                          # AI-Powered PR Code Review (Ollama — Free, Local)
│   ├── scripts/
│   │   ├── part-a-hook.md                    # 1-min hook script
│   │   ├── part-b-implementation.md          # Full step-by-step walkthrough
│   │   └── screen-recording-guide.md         # Video splits, cue sheet, checklists
│   └── sample-app/
│       ├── ai-review.sh                      # Reusable AI review script (any repo, any language)
│       └── utils/
│           ├── http_client_buggy.py          # Buggy HTTP retry handler (3 edge cases)
│           └── http_client_fixed.py          # Fixed version after AI review
│
├── 02-ai-unit-tests/                         # AI-Generated Unit Tests & Coverage Boost
│   ├── scripts/
│   │   ├── paid-version-scripts.md           # Using OpenAI / Anthropic API keys
│   │   └── free-version-scripts.md           # Using Ollama (free, local)
│   ├── sample-app/
│   │   ├── app/calculator.py                 # Module with 2 planted bugs
│   │   ├── tests/test_calculator.py          # Minimal starter tests (~23% coverage)
│   │   └── bug_surfacing_prompt.txt          # Reusable bug-surfacing prompt
│   └── qodo-cover/ → (symlink)              # Full Qodo Cover repo
│
├── 03-ai-exploratory-testing/                # AI E2E Flow Testing with LLMs
│   ├── scripts/
│   │   ├── part-a-hook.md                    # 1-min hook script
│   │   ├── part-b-implementation.md          # Full step-by-step walkthrough (671 lines)
│   │   ├── screen-recording-guide.md         # Video splits, cue sheet, flow diagram
│   │   └── csv-row.csv                       # Use case CSV row
│   └── sample-app/                           # Django app with 7 planted middleware bugs
│       ├── manage.py
│       ├── requirements.txt
│       ├── config/settings.py                # Middleware stack, auth config, RBAC rules
│       ├── middleware/
│       │   ├── rate_limiter.py               # 3 bugs: wrong status, GET-only, IP spoofing
│       │   ├── auth.py                       # 4 bugs: key bypass, OR logic, path bypass, no expiry
│       │   └── request_logger.py             # Clean
│       ├── api/
│       │   ├── urls.py                       # 9 endpoints across 4 tiers
│       │   └── views.py                      # Clean views (bugs are in middleware)
│       ├── prompts/
│       │   ├── 01-generate-scenarios.md      # Prompt 1: generate E2E test scenarios (LLM-agnostic)
│       │   └── 02-analyze-results.md         # Prompt 2: produce structured bug report (LLM-agnostic)
│       ├── scenarios.txt                     # Actual AI-generated scenarios
│       ├── test_results.txt                  # Actual curl test results
│       └── output.txt                        # Actual AI bug report (7 bugs, 3 critical)
│
├── 04-voice-to-ticket/                       # Voice-to-Ticket: Meeting Action Item Extraction
│   └── scripts.md                            # Fireflies + n8n + Gemini + Slack + Jira
│
├── 05-llm-local-session/                     # University Session: Run LLMs Locally (60–90 min)
│   ├── session-guide.md                      # Consolidated presenter guide + demos
│   ├── slide-contents.md                     # 26 slides
│   └── demo-scripts/
│       ├── agent_demo.py                     # Agent with tool calling
│       ├── quick_chat.py                     # 5-line SDK chat
│       ├── eli5.py                           # CLI: explain anything simply
│       ├── json_demo.py                      # Structured JSON output
│       └── chain_demo.py                     # Multi-step chain: Review → Fix → Test
│
└── references/
    └── external-tools-and-links.md           # All tools, URLs, models, libraries
```

---

## Quick Start

### AI PR Review
```bash
cd 01-ai-pr-review/sample-app
chmod +x ai-review.sh
# Set up a git repo with buggy code on a feature branch, then:
./ai-review.sh main
```

### AI Unit Tests (Free)
```bash
cd 02-ai-unit-tests/sample-app
pip install pytest pytest-cov
pytest tests/ --cov=app --cov-report=term   # ~23% baseline
# Follow scripts/free-version-scripts.md to run Qodo Cover with Ollama
```

### AI Exploratory Testing
```bash
cd 03-ai-exploratory-testing/sample-app
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver 8000
curl http://localhost:8000/api/health
# Copy prompts/ into any LLM to generate and run E2E test scenarios
```

### LLM Local Session Demos
```bash
pip install ollama
ollama pull llama3.1:8b && ollama pull qwen2.5-coder:7b
python 05-llm-local-session/demo-scripts/quick_chat.py
python 05-llm-local-session/demo-scripts/eli5.py "quantum computing"
python 05-llm-local-session/demo-scripts/json_demo.py
python 05-llm-local-session/demo-scripts/agent_demo.py
python 05-llm-local-session/demo-scripts/chain_demo.py
```

---

## External References

| Tool | URL |
|------|-----|
| Ollama | https://ollama.com |
| Qodo Cover | https://github.com/qodo-ai/qodo-cover |
| Fireflies.ai | https://fireflies.ai |
| n8n | https://n8n.io |
| Open WebUI | https://github.com/open-webui/open-webui |
| Ollama Python SDK | https://github.com/ollama/ollama-python |
| OWASP Testing Guide | https://owasp.org/www-project-web-security-testing-guide/ |

Full list: [`references/external-tools-and-links.md`](references/external-tools-and-links.md)

---

## Additional Use Cases (in CSV, no scripts yet)

See `ai_use_cases.csv` for: Chat with DB, PRD to User Stories, Onboarding + Jira, Code Migration, Incident Root Cause, Figma to Code, Auto Release Notes, Architecture Diagrams, Dependency Upgrade & Auto-Patch.

---

## License

Internal use only.
