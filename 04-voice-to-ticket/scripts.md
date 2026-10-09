# Voice-to-Ticket: Automated Meeting Action Item Extraction — Scripts

---

## PART A — Hook Script (~1 minute)

> **[HOOK — open with the pain point]**
>
> You just wrapped a 45-minute sprint planning call. Five people made commitments. Nobody wrote them down. Two days later, half those action items are forgotten, and your PM is chasing everyone on Slack asking "who was supposed to do what?"
>
> **[HIGH-LEVEL WORKFLOW — what we're building]**
>
> In this video, I'm going to show you how to build an end-to-end automation that solves this permanently — using Fireflies.ai, n8n, the Gemini API, Slack, and Jira.
>
> Here's how it works at a high level:
> 1. Fireflies joins your meeting automatically and records it.
> 2. Once the call ends, n8n picks up the transcript and sends it to Gemini.
> 3. Gemini doesn't just summarize — it performs speaker-attributed semantic extraction. It figures out who committed to what, by when, and at what priority — and outputs structured JSON.
> 4. That structured data becomes draft Jira tickets, which get sent to Slack for human approval before anything is created.
> 5. One click, and real, assigned tickets land in your engineers' Jira queues.
>
> **[BENEFITS]**
>
> This workflow saves a team of eight engineers roughly 10 to 15 hours a week of admin time — that's note-taking, ticket writing, and follow-up chasing, gone. Action items stop falling through the cracks. And the best part? There's a human in the loop — AI does the heavy lifting, but you approve every ticket before it's created.
>
> **[CTA]**
>
> And here's the kicker — I built the entire n8n workflow with AI assistance using Claude in under 10 minutes. If you want to learn how to set this up yourself, step by step, keep watching Part B.

---

## SCREEN RECORDING — Suggested Video Splits

Split recordings at these logical breakpoints:

| Video | Steps Covered | Description | Est. Duration |
|-------|--------------|-------------|---------------|
| **Video 1** | Pre-requisites | Account setup: Fireflies, n8n Cloud, Gemini API key, Jira API token, Slack app creation | 8-12 min |
| **Video 2** | Steps 1-2 | AI-assisted workflow scaffolding with Claude + Webhook URL setup | 10-15 min |
| **Video 3** | Steps 3-6 | Configuring all API credentials in n8n nodes (Fireflies, Gemini, Jira, Slack) | 10-12 min |
| **Video 4** | Steps 7-9 | Activating workflow, connecting Fireflies webhook, Slack interactivity setup | 8-10 min |
| **Video 5** | Step 10 | Live end-to-end test with a real meeting — the demo moment | 5-8 min |

**Recording reminders:**
- Light theme on all tools (n8n, Slack, Jira, browser, terminal)
- Record at normal speed, no fast-forwarding
- Voice-over throughout — call out "This is the wow factor" at Step 1 (workflow generation) and Step 4/test results (semantic extraction + JIRA creation)
- Do not crop/trim before uploading
- Update this Part B script if you discover better approaches during recording

---

## PART B — Detailed Implementation Script

---

### PRE-REQUISITES SETUP

Before touching n8n, get all accounts and credentials ready.

#### B0.1 — Fireflies.ai Account

1. Go to [fireflies.ai](https://fireflies.ai) and sign up for a **free account**.
2. Navigate to **Settings → Developer**.
3. Click **Generate API Key**. Copy and save it — you'll need it in Step 3.
4. Find the **Fireflies bot email** (e.g., `fred@fireflies.ai`) — you'll add this as a meeting invitee later.
5. **Data privacy note (mention in video):** Fireflies is SOC 2 Type II and GDPR compliant. They state they do not use meeting content for model training. However, meeting audio IS uploaded to their cloud servers. For this demo, we're using a test meeting with non-sensitive content. For production use in an organization, evaluate the Enterprise plan which offers private storage and HIPAA BAA.

#### B0.2 — n8n Cloud Account

1. Go to [n8n.io](https://n8n.io) and sign up for the **free Cloud tier**.
2. Once signed in, you'll land on the n8n dashboard.
3. **Key point (mention in video):** n8n Cloud gives us persistent, internet-reachable webhook URLs out of the box — no need for ngrok or a static IP. The free tier allows ~100 executions/month and runs on n8n's infrastructure, so there's no impact on your local machine's performance.

#### B0.3 — Google Gemini API Key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Click **Create API Key** and select or create a Google Cloud project.
3. Copy the generated API key and save it.
4. **Data privacy note (mention in video):** On the free API tier, Google may use input/output data to improve their products, and human reviewers may access it. Do NOT send sensitive or confidential transcripts through the free tier. For production, use the paid tier via Vertex AI, which does not use your data for training.

#### B0.4 — Jira Setup

1. Log in to your Jira instance (Atlassian Cloud).
2. Note your **Jira site URL** (e.g., `https://yourteam.atlassian.net`).
3. Note the **email** associated with your Atlassian account.
4. Generate an **API token**: Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens) → **Create API token** → give it a label like "n8n-voice-to-ticket" → copy and save.
5. Create a **test Jira project** (e.g., project key `VTT`) so demo tickets don't pollute real boards.

#### B0.5 — Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**.
2. Name it (e.g., "Voice-to-Ticket Bot") and select your workspace.
3. Under **OAuth & Permissions**, add these Bot Token Scopes:
   - `chat:write`
   - `chat:write.public`
4. Click **Install to Workspace** and authorize.
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`).
6. Create a **test Slack channel** (e.g., `#voice-to-ticket-test`).
7. Invite the bot to the channel: type `/invite @Voice-to-Ticket Bot` in the channel.
8. **Do NOT enable Interactivity yet** — we'll do that in Step 9 once we have the second webhook URL from n8n.

#### B0.6 — Claude Access

1. Open [claude.ai](https://claude.ai) (free tier works) or use Claude via API.
2. We'll use Claude in Step 1 to help scaffold the n8n workflow — this is the "AI-as-developer-tool" moment.

**Say in recording:** *"We're using two LLMs here deliberately. Claude helps us BUILD the workflow — it's our developer assistant. Gemini runs INSIDE the workflow to process transcripts at runtime. This keeps the per-execution cost at zero since Gemini's free tier handles the runtime. Claude could technically do both, but separating build-time from run-time shows two distinct ways to use AI and keeps the demo completely free."*

---

### STEP 1 — Build the Workflow in n8n with AI Assistance

**🎬 WOW FACTOR MOMENT #1 — Call this out in the recording.**

**Say in recording:** *"This is the first wow factor. Instead of manually dragging and dropping eight nodes and figuring out how to wire them together, I'm going to ask Claude to generate the workflow structure for me. What would normally take 30-60 minutes of manual setup, we'll scaffold in minutes with AI assistance."*

#### B1.1 — Prompt Claude to generate the workflow

Open Claude and use the following prompt:

```
I'm building an n8n workflow that automates meeting action-item extraction. Here's what I need:

The workflow should have 8 nodes in this order:
1. Webhook Trigger — receives a POST from Fireflies.ai when a meeting transcript is ready
2. HTTP Request — calls the Fireflies.ai GraphQL API to fetch the full transcript using the meeting ID from the webhook payload
3. HTTP Request (Gemini) — sends the transcript to the Google Gemini API with a prompt that extracts action items as structured JSON (fields: action, owner, deadline, priority)
4. Split In Batches — splits the JSON array of action items into individual items
5. Slack (Send Message) — posts each action item to a Slack channel with Approve/Reject buttons using Block Kit interactive message format
6. Webhook (Wait for Approval) — a second webhook that catches the button click callback from Slack
7. Jira Software (Create Issue) — creates a Jira ticket for each approved action item using the extracted fields
8. Slack (Send Message) — posts a final summary of all created tickets to the Slack channel

For each node, provide:
- The exact n8n node type to use
- The key configuration fields and where to map expressions from previous nodes
- The Gemini prompt that should be used for action-item extraction (output strict JSON)

Also generate the Fireflies GraphQL query to fetch transcript by meeting ID.
```

#### B1.2 — Review Claude's output

- Claude will generate the node structure, configurations, and the Gemini prompt.
- **Important (say in recording):** *"Claude gives us the structure and the logic, but we'll still need to manually plug in our API keys, credentials, and fine-tune the node settings. This is AI-assisted workflow generation — not fully autonomous."*

#### B1.3 — Create the workflow in n8n

1. In n8n Cloud dashboard, click **Add Workflow**.
2. Name it: `Voice-to-Ticket: Meeting Action Items`.
3. Following Claude's output, add the 8 nodes in order:
   - Click **+** → search for each node type → add and position.
   - Wire them together in sequence.
4. Don't configure credentials yet — we'll do that step by step next.

---

### STEP 2 — Save the Webhook URL

#### B2.1 — Get the Webhook Trigger URL

1. Click on the **first node** (Webhook Trigger).
2. Set **HTTP Method** to `POST`.
3. n8n will display a **Production URL** and a **Test URL**.
4. Copy the **Production URL** — this is what Fireflies will call when a transcript is ready.
5. Save this URL somewhere accessible (e.g., a text file or note).

**Say in recording:** *"This is the URL we'll paste into Fireflies' webhook settings later. Because we're on n8n Cloud, this URL is persistent and internet-reachable — it won't go down when we close our laptop."*

#### B2.2 — Get the second Webhook URL (for Slack approval)

1. Click on **Node 6** (the second Webhook — Wait for Approval).
2. Set **HTTP Method** to `POST`.
3. Copy its **Production URL** as well — this is what Slack will call when someone clicks Approve/Reject.
4. Save this URL separately — we'll need it in Step 9 for Slack Interactivity.

---

### STEP 3 — Configure the Fireflies Transcript Node

#### B3.1 — Set up the Fireflies API call

1. Click on **Node 2** (HTTP Request — Fireflies).
2. Set the following:
   - **Method:** `POST`
   - **URL:** `https://api.fireflies.ai/graphql`
   - **Authentication:** Header Auth
     - **Header Name:** `Authorization`
     - **Header Value:** `Bearer YOUR_FIREFLIES_API_KEY` (paste the key from B0.1)
   - **Body Content Type:** JSON
   - **Body:**
     ```json
     {
       "query": "query GetTranscript($transcriptId: String!) { transcript(id: $transcriptId) { id title organizer_email participants sentences { speaker_name text } action_items } }",
       "variables": {
         "transcriptId": "{{ $json.data.transcriptId }}"
       }
     }
     ```
     *(The `transcriptId` expression maps from the Fireflies webhook payload)*

#### B3.2 — Test the node (optional)

- If you already have a Fireflies transcript, you can paste a test transcript ID to verify the API call works.

---

### STEP 4 — Configure the Gemini Action-Item Extraction Node

**🎬 WOW FACTOR MOMENT #2 — Call this out in the recording.**

**Say in recording:** *"This is the core wow factor. We're not just summarizing the meeting — Gemini will perform speaker-attributed semantic extraction. It'll distinguish casual remarks from real commitments, figure out who owns each action item, and output structured JSON. This is the step where a messy human conversation becomes machine-readable project artifacts."*

#### B4.1 — Set up the Gemini API call

1. Click on **Node 3** (HTTP Request — Gemini).
2. Set the following:
   - **Method:** `POST`
   - **URL:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_GEMINI_API_KEY`
     *(paste your Gemini API key from B0.3)*
   - **Body Content Type:** JSON
   - **Body:**
     ```json
     {
       "contents": [
         {
           "parts": [
             {
               "text": "You are a meeting action-item extractor. Analyze the following meeting transcript and extract ONLY concrete action items — commitments where a specific person agreed to do a specific thing.\n\nRules:\n1. Distinguish between casual remarks ('we should probably look at that sometime') and hard commitments ('I will have the auth refactor done by Friday'). Only extract hard commitments.\n2. For each action item, identify: the exact person who made the commitment (owner), what they committed to (action), the deadline if mentioned, and the priority (High/Medium/Low based on context).\n3. If a remark is vague or non-committal, either skip it entirely or mark it as priority: 'Low-Confidence' so a human can review it.\n4. Output ONLY valid JSON — an array of objects with these fields: action, owner, deadline, priority.\n5. If no action items are found, return an empty array [].\n\nTranscript:\n{{ $json.data.transcript.sentences.map(s => s.speaker_name + ': ' + s.text).join('\\n') }}\n\nOutput the JSON array and nothing else."
             }
           ]
         }
       ],
       "generationConfig": {
         "responseMimeType": "application/json"
       }
     }
     ```

#### B4.2 — Key points about this prompt (explain in recording)

- **Speaker attribution:** The prompt receives speaker-labeled sentences (`speaker_name: text`), so Gemini knows WHO said each line.
- **Casual vs commitment filtering:** The prompt explicitly instructs Gemini to skip vague remarks or flag them as "Low-Confidence."
- **Structured JSON output:** Setting `responseMimeType` to `application/json` forces Gemini to return valid JSON — no markdown, no extra text.
- **This is what separates it from generic summarizers** — we get structured, actionable data, not a paragraph of notes.

---

### STEP 5 — Configure the Jira Ticket-Creation Node

#### B5.1 — Add Jira credentials to n8n

1. In n8n, go to **Settings → Credentials → Add Credential**.
2. Search for **Jira Software** and select it.
3. Fill in:
   - **Email:** your Atlassian email
   - **API Token:** the token from B0.4
   - **Domain:** your Jira site URL (e.g., `https://yourteam.atlassian.net`)
4. Click **Save**.

#### B5.2 — Configure the Jira node

1. Click on **Node 7** (Jira Software — Create Issue).
2. Select the credential you just created.
3. Set:
   - **Project:** your test project (e.g., `VTT`)
   - **Issue Type:** `Task`
   - **Summary:** `{{ $json.action }}` (maps from the Gemini output)
   - **Description:** `Auto-generated from meeting. Owner: {{ $json.owner }}. Deadline: {{ $json.deadline }}. Priority: {{ $json.priority }}.`
   - **Assignee:** Map `{{ $json.owner }}` if your Jira users match speaker names, or leave unassigned for manual assignment.
   - **Priority:** Map `{{ $json.priority }}` → Jira priority field.

---

### STEP 6 — Configure Both Slack Nodes

#### B6.1 — Add Slack credentials to n8n

1. In n8n, go to **Settings → Credentials → Add Credential**.
2. Search for **Slack** and select **Slack API (OAuth2)**.
3. Paste the **Bot User OAuth Token** from B0.5.
4. Click **Save**.

#### B6.2 — Configure Node 5 (Slack — Approval Message)

1. Click on **Node 5** (Slack — Send Message).
2. Select your Slack credential.
3. Set **Channel** to your test channel (e.g., `#voice-to-ticket-test`).
4. For the message, use **Block Kit** format to include interactive buttons:
   ```json
   {
     "blocks": [
       {
         "type": "section",
         "text": {
           "type": "mrkdwn",
           "text": "*New Action Item Detected*\n*Action:* {{ $json.action }}\n*Owner:* {{ $json.owner }}\n*Deadline:* {{ $json.deadline }}\n*Priority:* {{ $json.priority }}"
         }
       },
       {
         "type": "actions",
         "elements": [
           {
             "type": "button",
             "text": { "type": "plain_text", "text": "✅ Approve" },
             "value": "approved",
             "action_id": "approve_action"
           },
           {
             "type": "button",
             "text": { "type": "plain_text", "text": "❌ Reject" },
             "value": "rejected",
             "action_id": "reject_action"
           }
         ]
       }
     ]
   }
   ```

#### B6.3 — Configure Node 8 (Slack — Final Summary)

1. Click on **Node 8** (Slack — Send Message).
2. Select the same Slack credential.
3. Set **Channel** to the same test channel.
4. Set the message to:
   ```
   ✅ *Jira ticket created:* {{ $json.key }} — {{ $json.fields.summary }}
   Assigned to: {{ $json.fields.assignee.displayName || 'Unassigned' }}
   ```

---

### STEP 7 — Activate the Workflow

1. In the n8n workflow editor, toggle the **Active** switch in the top-right corner to **ON**.
2. The workflow is now live and listening for incoming webhooks.

**Say in recording:** *"The workflow is now active. Both webhook URLs are live and waiting. When Fireflies sends a transcript or when someone clicks Approve in Slack, n8n will process it immediately."*

---

### STEP 8 — Connect Fireflies to the Workflow

#### B8.1 — Add the webhook in Fireflies

1. Log in to Fireflies.ai.
2. Go to **Integrations → Webhooks**.
3. Click **Add Webhook**.
4. Paste the **Webhook Trigger URL** from Step 2 (Node 1's Production URL).
5. Set the event to fire on **Transcription Completed**.
6. Save.

#### B8.2 — Add Fireflies bot to your calendar

1. Find the Fireflies bot email (shown in your Fireflies dashboard, e.g., `fred@fireflies.ai`).
2. Add this email as an **invitee** to your test meeting calendar event.
3. Alternatively, in Fireflies settings, enable **Auto-join** for all meetings on your calendar.

---

### STEP 9 — Connect Slack Interactivity

#### B9.1 — Enable Interactivity in your Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → select your app.
2. In the left sidebar, click **Interactivity & Shortcuts**.
3. Toggle **Interactivity** to **ON**.
4. In the **Request URL** field, paste the **second Webhook URL** from Step 2 (Node 6's Production URL).
5. Click **Save Changes**.

**Say in recording:** *"This is what makes the approval flow work. When someone clicks Approve or Reject in Slack, Slack sends a POST request to this n8n webhook URL. Because we're on n8n Cloud, this URL is persistent and internet-reachable — there's no ngrok or tunnel needed. If you were self-hosting n8n, you'd need ngrok or a server with a static IP for this to work."*

---

### STEP 10 — Live End-to-End Test

**🎬 THIS IS THE DEMO MOMENT — the payoff.**

**Say in recording:** *"Alright, this is the moment of truth. We're going to hold a short test meeting, say some action items out loud, and watch the entire pipeline fire — from recording to transcript to AI extraction to Slack approval to Jira ticket creation. No manual steps in between."*

#### B10.1 — Hold a test meeting

1. Create a short Google Meet / Zoom call.
2. Make sure the **Fireflies bot** is invited (check that `fred@fireflies.ai` or equivalent is on the invite).
3. Join the call with at least one other person (or use two devices/tabs).
4. Say these lines clearly during the call:
   - **Person A:** *"I'll fix the login page bug by Friday."*
   - **Person B:** *"I'll update the API docs by end of next week."*
   - **Person A:** *"We should probably revisit the database schema at some point."* ← (this is a casual remark — the AI should filter this out or flag it as low-confidence)
5. End the call.

#### B10.2 — Wait for the pipeline to fire

1. Fireflies will process the recording and generate the transcript (this can take 2-5 minutes).
2. Once ready, Fireflies sends a webhook to n8n.
3. n8n fetches the full transcript from Fireflies.
4. Gemini extracts the action items as structured JSON.
5. Watch your **Slack test channel** — approval messages should appear.

#### B10.3 — Approve in Slack

1. In Slack, you should see messages like:
   > **New Action Item Detected**
   > **Action:** Fix the login page bug
   > **Owner:** Person A
   > **Deadline:** Friday
   > **Priority:** High
   > [✅ Approve] [❌ Reject]
2. Click **✅ Approve** on the real action items.
3. Click **❌ Reject** on any low-confidence or incorrect items.

**Say in recording:** *"And here's the human-in-the-loop moment — the best part. This isn't just a meeting summary sitting in a doc that nobody reads. These are real, assigned Jira tickets about to land in engineers' queues, holding them accountable for what they said in the meeting. But we still get final say before anything is created."*

#### B10.4 — Verify in Jira

1. Open your Jira test project.
2. You should see the approved action items as new tickets with:
   - Title matching the extracted action
   - Description with owner, deadline, and priority
   - Linked back to the meeting context.

**Say in recording:** *"That's it. We went from a messy meeting conversation to structured, assigned Jira tickets — fully automated, with human approval in the loop. For a team of 8 engineers having 5 meetings a week, this saves roughly 10 to 15 hours of collective admin time per week. That translates to about $25k to $40k a year in recovered engineering productivity. And the entire setup runs on free tiers."*

#### B10.5 — Show the casual remark was filtered

1. Point out that the casual remark (*"We should probably revisit the database schema at some point"*) was either:
   - Not extracted at all, OR
   - Flagged as `priority: Low-Confidence` and did not become a ticket unless explicitly approved.

**Say in recording:** *"Notice how the AI correctly filtered out the casual remark about the database schema. It understood that 'we should probably' is not a commitment — unlike 'I'll fix the login page by Friday,' which is a clear, owned action item. That's speaker-attributed semantic extraction in action."*

---

## CONSTRAINTS & NOTES TO MENTION IN VIDEO

- **Transcript quality matters:** Background noise, overlapping speakers, and heavy accents can degrade extraction accuracy. Recommend quiet environments and one-speaker-at-a-time.
- **AI can make mistakes:** The Slack approval step exists for a reason. Always review before creating tickets.
- **Free tier data policies:** Remind viewers that Fireflies and Gemini free tiers have data handling implications. Use test meetings for the demo; evaluate paid/enterprise tiers for production.
- **Two-LLM rationale:** Claude builds the workflow (developer tool). Gemini runs inside it (runtime engine). This keeps per-execution cost at $0.
