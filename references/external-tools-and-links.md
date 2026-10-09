# External Tools & Reference Links

All tools, repos, and references used across the AI use cases.

---

## LLM Runtimes & Models

| Tool | URL | Used In |
|------|-----|---------|
| **Ollama** — Local LLM Runtime | https://ollama.com | PR Review, Unit Tests (free), Exploratory Testing, LLM Session |
| Ollama Model Library | https://ollama.com/library | All local LLM use cases |
| Ollama Python SDK | https://github.com/ollama/ollama-python | LLM Session demos |
| Open WebUI (ChatGPT-like UI for Ollama) | https://github.com/open-webui/open-webui | LLM Session |
| Hugging Face (model hub) | https://huggingface.co | LLM Session |
| DeepSeek Coder V2 | https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Instruct | Exploratory Testing |

### Recommended Models by Use Case

| Use Case | Model | Size |
|----------|-------|------|
| PR Code Review | `qwen2.5-coder:7b` | ~8 GB RAM |
| Exploratory Testing | `deepseek-coder-v2:16b` | ~16 GB RAM |
| Unit Test Generation | `qwen2.5-coder:7b` or cloud LLM | ~8 GB RAM |
| General Chat / Demos | `llama3.1:8b` | ~8 GB RAM |
| Quick Tasks | `phi3:mini` | ~4 GB RAM |
| Best Local Quality | `qwen2.5-coder:32b` | ~32 GB RAM |

---

## AI Test Generation

| Tool | URL | Used In |
|------|-----|---------|
| **Qodo Cover** (fka Cover Agent) | https://github.com/qodo-ai/qodo-cover | AI Unit Tests |
| Qodo Cover — CI Integration | https://github.com/qodo-ai/qodo-ci | AI Unit Tests (CI mode) |
| Qodo AI (company) | https://www.qodo.ai | AI Unit Tests |

---

## Cloud LLM APIs (for paid versions)

| Provider | URL | Used In |
|----------|-----|---------|
| OpenAI (ChatGPT, GPT-4o) | https://chat.openai.com | Unit Tests (paid), general |
| Anthropic (Claude) | https://claude.ai | Unit Tests (paid), general |
| Google Gemini API | https://aistudio.google.com/apikey | Voice-to-Ticket |

---

## Automation & Integration

| Tool | URL | Used In |
|------|-----|---------|
| **n8n** (workflow automation) | https://n8n.io | Voice-to-Ticket |
| **Fireflies.ai** (meeting transcription) | https://fireflies.ai | Voice-to-Ticket |
| Jira API Tokens | https://id.atlassian.com/manage-profile/security/api-tokens | Voice-to-Ticket |
| Slack API (Bot Apps) | https://api.slack.com/apps | Voice-to-Ticket |

---

## Code Review (Cloud Alternatives)

| Tool | URL | Notes |
|------|-----|-------|
| CodeRabbit | https://coderabbit.ai | Cloud-based AI PR review (paid alternative to our local approach) |

---

## Security & Testing References

| Resource | URL | Used In |
|----------|-----|---------|
| OWASP Web Security Testing Guide | https://owasp.org/www-project-web-security-testing-guide/ | Exploratory Testing |

---

## Python Libraries Used

| Library | Install | Used In |
|---------|---------|---------|
| `requests` | `pip install requests` | PR Review sample app |
| `django` | `pip install django` | Exploratory Testing sample app |
| `djangorestframework` | `pip install djangorestframework` | Exploratory Testing sample app |
| `pytest` | `pip install pytest` | Unit Tests sample app |
| `pytest-cov` | `pip install pytest-cov` | Unit Tests sample app |
| `ollama` | `pip install ollama` | LLM Session demo scripts |
