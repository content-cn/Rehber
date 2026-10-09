"""Demo 6: Simple LLM Agent with Tool Calling
Shows the Think → Act → Observe → Repeat loop.
Requires: pip install ollama
"""

import json
import ollama

# --- Define tools the agent can call ---

TOOLS = {
    "get_weather": {
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
            },
            "required": ["city"],
        },
    },
    "get_time": {
        "description": "Get the current time in a timezone",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {"type": "string", "description": "Timezone (e.g. UTC, EST)"},
            },
            "required": ["timezone"],
        },
    },
}


def get_weather(city: str) -> dict:
    """Simulated weather API."""
    weather_data = {
        "London": {"temp": 12, "condition": "cloudy", "humidity": 78},
        "Tokyo": {"temp": 26, "condition": "sunny", "humidity": 45},
        "New York": {"temp": 18, "condition": "partly cloudy", "humidity": 62},
    }
    return weather_data.get(city, {"temp": 20, "condition": "unknown", "humidity": 50})


def get_time(timezone: str) -> dict:
    """Simulated time API."""
    from datetime import datetime, timedelta

    offsets = {"UTC": 0, "EST": -5, "PST": -8, "IST": 5, "JST": 9}
    offset = offsets.get(timezone.upper(), 0)
    now = datetime.utcnow() + timedelta(hours=offset)
    return {"timezone": timezone, "time": now.strftime("%H:%M:%S")}


TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "get_time": get_time,
}

# --- Agent loop ---

def run_agent(query: str, model: str = "llama3.1:8b"):
    print(f"\n🧑 User: {query}\n")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to tools. "
                "When you need external data, call a tool by responding with JSON: "
                '{"tool": "tool_name", "args": {"param": "value"}}. '
                "Available tools: get_weather(city), get_time(timezone). "
                "If you don't need a tool, just respond normally."
            ),
        },
        {"role": "user", "content": query},
    ]

    for step in range(5):  # Max 5 steps
        response = ollama.chat(model=model, messages=messages)
        reply = response["message"]["content"].strip()

        # Try to parse as tool call
        try:
            parsed = json.loads(reply)
            if "tool" in parsed and "args" in parsed:
                tool_name = parsed["tool"]
                tool_args = parsed["args"]
                print(f"🤖 Agent: I need to call a tool.\n")
                print(f"📞 Tool Call: {tool_name}({json.dumps(tool_args)})")

                if tool_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[tool_name](**tool_args)
                    print(f"📋 Tool Result: {json.dumps(result)}\n")

                    messages.append({"role": "assistant", "content": reply})
                    messages.append({
                        "role": "user",
                        "content": f"Tool result: {json.dumps(result)}. Now answer the original question using this data.",
                    })
                    continue
                else:
                    print(f"❌ Unknown tool: {tool_name}")
                    break
        except (json.JSONDecodeError, TypeError):
            pass

        # Regular response — agent is done
        print(f"🤖 Agent: {reply}")
        break


if __name__ == "__main__":
    run_agent("What's the weather like in London right now?")
