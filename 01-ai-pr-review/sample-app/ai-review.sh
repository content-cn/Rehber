#!/bin/bash
# AI-Powered Code Review — runs locally via Ollama
# Usage: ./ai-review.sh [base_branch] [model]
# Example: ./ai-review.sh main qwen2.5-coder:7b

BASE_BRANCH="${1:-main}"
MODEL="${2:-qwen2.5-coder:7b}"

echo "🔍 AI Code Review: comparing against '$BASE_BRANCH' using model '$MODEL'"
echo "---"

DIFF=$(git diff "$BASE_BRANCH"...HEAD)

if [ -z "$DIFF" ]; then
    echo "✅ No changes found against $BASE_BRANCH."
    exit 0
fi

PROMPT="You are a senior code reviewer performing a thorough first-pass review on a pull request diff.

Analyze the following git diff carefully and report every issue you find.

For EACH issue, use this exact format:
---
SEVERITY: [Bug | Warning | Style | Suggestion]
FILE: [filename]
LINE: [approximate line or function name]
ISSUE: [Clear description of the problem]
WHY: [Why this is a problem — what could go wrong in production]
FIX: [Specific code change to resolve it]
---

What to look for:
1. Missing edge-case handling that would pass happy-path tests but fail in production
2. HTTP protocol violations (ignoring standard headers, retrying non-retryable status codes)
3. Unbounded loops, delays, or resource usage
4. Exception types that are too narrow or too broad
5. Logic that works for the common case but breaks under adversarial or unexpected inputs
6. Missing input validation (negative numbers, zero, None/null, empty collections)
7. Security issues (injection, path traversal, hardcoded secrets)

IMPORTANT: Think about how this code behaves in production under real-world conditions — not just during local testing with simple inputs.

If no issues are found, respond with: '✅ No issues found. Code looks good.'

Here is the git diff to review:"

echo "$DIFF" | ollama run "$MODEL" "$PROMPT

$(cat)"
