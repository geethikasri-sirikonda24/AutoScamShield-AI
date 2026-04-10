# 🛡️ AutoScamShield AI
### Agentic Email Monitoring, Scam Detection & Autonomous Threat Response System with RAG and Live Dashboard*

> A real-time agentic AI system that automatically monitors incoming emails, detects scam and phishing attempts using LLMs and RAG, and autonomously takes action while providing a live dashboard for monitoring and control.
---

## 📋 Table of Contents

1. [Business Problem](#1-business-problem)
2. [Possible Solutions](#2-possible-solutions)
3. [Implemented Solution](#3-implemented-solution)
4. [Tech Stack](#4-tech-stack-used)
5. [Architecture Diagram](#5-architecture-diagram)
6. [How to Run Locally](#6-how-to-run-locally)
7. [References & Resources](#7-references--resources)
8. [Recording](#8-recording)
9. [Screenshots](#9-screenshots)
10. [Problems Faced & Solutions](#10-problems-faced--solutions)

---

## 1. Business Problem

Email-based scams are one of the fastest-growing cybersecurity threats globally:

| Statistic | Value |
|-----------|-------|
| 📧 Phishing emails sent per day | **3.4 Billion** |
| 💸 Losses to email scams in 2023 | **$17.4 Billion** |
| 🏢 Organisations that faced phishing attacks | **83%** |

### Core Challenges

- **Spam filters miss sophisticated scams** — modern scam emails mimic legitimate senders so closely that traditional rule-based filters fail to catch them
- **Manual review doesn't scale** — human review is slow, expensive, and error-prone, especially at inbox volumes of dozens to hundreds of emails per day
- **Scam patterns evolve faster than static rules** — attackers continuously adapt their language and formatting to evade known filters
- **Users lack explanations** — even when emails are flagged, users rarely receive a per-email, human-readable explanation of *why* it was marked as dangerous

---

## 2. Possible Solutions

| Approach | Description | Limitation |
|----------|-------------|------------|
| Rule-based spam filters | Keyword blocklists, sender blacklists | Easily bypassed by paraphrasing |
| ML classifiers (Naive Bayes, SVM) | Trained on labelled email datasets | Struggle with novel scam patterns |
| Fine-tuned LLMs | Domain-specific model training | Expensive, requires large labelled datasets |
| **Agentic AI + RAG (Chosen)** | LLM reasoning + vector memory + autonomous agents | Best balance of accuracy, explainability, and adaptability |

The agentic RAG approach was selected because it combines the deep reasoning ability of large language models with a persistent knowledge base of known scam patterns — and it can explain its decisions in natural language.

---

## 3. Implemented Solution

**AutoScamShield AI** is a 6-agent agentic system that automatically scans your inbox, analyses each email using Claude AI + RAG memory, and classifies every email as **Safe** or **Scam** in real-time — with a risk score, category, reasoning, and automated action.

### How It Works

```
Gmail IMAP / Manual Input
        ↓
  [1] Fetcher Agent   →  Pulls raw email content
        ↓
  [2] RAG Agent       →  Searches FAISS vector store for known scam patterns
        ↓
  [3] LLM Agent       →  Sends email + RAG context to Claude claude-opus-4-5 for analysis
        ↓
  [4] Scorer Agent    →  Computes 0–100 composite risk score
        ↓
  [5] Response Agent  →  Decides: Block / Quarantine / Deliver
        ↓
  [6] Dashboard Agent →  Updates live UI, charts, logs in real-time
```

### Key Features

- 🔌 **Real Gmail Scan** — Connects to Gmail via IMAP and reads your last 10 real emails automatically
- 🧠 **Claude AI Analysis** — Each email body is sent to `claude-opus-4-5` for deep scam pattern detection
- 🔍 **RAG Memory** — FAISS vector store of 500+ known scam patterns retrieved at inference time
- 📊 **Risk Scoring (0–100)** — Composite score with automated action: Block, Quarantine, or Deliver
- 📡 **Live Dashboard** — Real-time charts, email feed, agent pipeline view, and system log
- 🤖 **6-Agent Pipeline** — Fully autonomous agents orchestrated via Flask

---

## 4. Tech Stack Used

| Layer | Technology |
|-------|-----------|
| **AI / LLM** | Anthropic Claude (`claude-opus-4-5`) |
| **Vector Store / RAG** | FAISS (`faiss-cpu`) + NumPy embeddings |
| **Backend** | Python 3, Flask, Gunicorn |
| **Frontend** | Vanilla HTML/CSS/JS, Chart.js (CDN) |
| **Email Access** | Gmail IMAP (`imaplib`) |
| **Environment** | `python-dotenv` for secret management |
| **Deployment** | Render.com |
| **Dev Environment** | Cursor AI Editor |
| **Version Control** | Git + GitHub |

---

## 5. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│         Gmail IMAP  │  Manual Simulate  │  Webhook          │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                      AGENTIC LAYER                          │
│  Fetcher → RAG Agent → LLM Agent → Scorer → Response →     │
│                                              Dashboard      │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────┐
│               AI / LLM LAYER                 │
│   Claude claude-opus-4-5  │  Prompt Templates  │  RAG Context  │
└──────────────────────────────────────────────┘
          ↓                          ↓
┌──────────────────┐      ┌─────────────────────────┐
│   DATA LAYER     │      │      ACTION LAYER        │
│  FAISS Vector DB │      │ Block │ Quarantine │      │
│  Scam Pattern DB │      │ Deliver │ Audit Log │     │
│  Email Metadata  │      └─────────────────────────┘
└──────────────────┘               ↓
                    ┌──────────────────────────────┐
                    │     PRESENTATION LAYER        │
                    │ Dashboard │ Charts │ Feed │    │
                    │       System Log              │
                    └──────────────────────────────┘
```

> All layers are orchestrated by **Flask (Python)**. Data flows top-down: Email → Agents → Claude AI → Decision → UI Update

---

## 6. How to Run Locally

### Prerequisites

- Python 3.9+
- An [Anthropic API Key](https://console.anthropic.com/)
- Node.js (optional, for `docx` tooling)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/geethikasri-sirikonda24/abcd-agentic-training-vnr-Geethikasri.git
cd abcd-agentic-training-vnr-Geethikasri
```

### Step 2 — Install Dependencies

```bash
pip install flask openai anthropic faiss-cpu numpy python-dotenv
```

### Step 3 — Configure Environment

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_key_here
```

> ⚠️ Never commit your `.env` file to GitHub. Add it to `.gitignore`.

### Step 4 — Run the App

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

### Step 5 — Test the App

1. Click **"+ Simulate Email"** in the top right
2. Enter a subject like `"Urgent: Your account is suspended"`
3. Enter body text like `"Click here to verify your bank details immediately"`
4. Click **Analyze** — the system will call Claude AI and return a risk score, category, and action

### Project File Structure

```
autoscamshield/
├── app.py               # Flask backend + Claude API + RAG
├── templates/
│   └── index.html       # Full dashboard UI (single-file)
├── static/
│   └── style.css        # Optional additional styles
├── .env                 # API keys (not committed)
├── requirements.txt     # Python dependencies

```

## 7. References & Resources

| Resource | Link |
|----------|------|
| Anthropic Claude API Docs | [https://docs.anthropic.com](https://docs.anthropic.com) |
| Anthropic Console (API Keys) | [https://console.anthropic.com](https://console.anthropic.com) |
| Flask Documentation | [https://flask.palletsprojects.com](https://flask.palletsprojects.com) |
| FAISS (Facebook AI Similarity Search) | [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) |
| Chart.js Documentation | [https://www.chartjs.org/docs](https://www.chartjs.org/docs) |
| Render.com Deployment | [https://render.com/docs](https://render.com/docs) |
| Python dotenv | [https://pypi.org/project/python-dotenv](https://pypi.org/project/python-dotenv) |
| Cursor AI Editor | [https://cursor.sh](https://cursor.sh) |
| ABCD Agentic Training Repo | [https://github.com/geethikasri-sirikonda24/abcd-agentic-training-vnr-Geethikasri.git](https://github.com/geethikasri-sirikonda24/abcd-agentic-training-vnr-Geethikasri.git) |

---

## 8. Recording

> 🎥 **Demo Video:** https://drive.google.com/file/d/1J_B7DYfepwnd9MyyWtXXeLtu_j6N_Nbf/view?usp=sharing
>
> The recording demonstrates:
> - Live Gmail inbox scan and classification
> - Manual email simulation with Claude AI analysis
> - Agent pipeline execution in real-time
> - Dashboard charts, email feed, and system log
> - RAG memory retrieval demo
> - Syllabus coverage and architecture tabs

---

## 9. Screenshots

### Dashboard — Empty State
<img width="1905" height="977" alt="image" src="https://github.com/user-attachments/assets/878656d2-0e0a-4754-ab4f-dcf1acce172d" />

> Initial dashboard view with system initialized. The live email feed awaits the first simulation.

### Dashboard — After Inbox Scan
<img width="1918" height="988" alt="image" src="https://github.com/user-attachments/assets/db6803bc-0ee4-41d4-9a3c-191d71752acc" />
<img width="1919" height="973" alt="image" src="https://github.com/user-attachments/assets/02f6c629-8b52-4837-a516-5909d4b8dd88" />
<img width="1904" height="247" alt="image" src="https://github.com/user-attachments/assets/64d5f762-b241-4e21-87ce-570aac547b6c" />

> After scanning `sirikondageethikasri@gmail.com` — 8 emails processed: 4 scams detected, 4 safe. Each email shows risk score, category, action, and reasoning.

### Threat Distribution Charts
<img width="1918" height="997" alt="image" src="https://github.com/user-attachments/assets/5d729b3e-6511-43e6-9fca-80c5e0afeee9" />

> Left: Doughnut chart showing threat category breakdown. Right: Risk score trend line across processed emails.

### Safe Emails — Filtered View
<img width="1911" height="844" alt="image" src="https://github.com/user-attachments/assets/039cbda6-9d78-4488-a06a-09683ac1d5cc" />
<img width="1917" height="839" alt="image" src="https://github.com/user-attachments/assets/59c1db2c-17c9-4f00-b75e-51d58d1cb78e" />

> Filtering to Safe emails only — showing legitimate Amazon, GitHub, Medium, and Google Calendar emails with low risk scores (2%–6%).

---


## 10. Formatting Note
This README follows standard GitHub Markdown formatting:

•	All sections clearly numbered and linked in Table of Contents

•	Code blocks used for all commands and env variables

•	Tables used for structured comparisons

•	Architecture shown using ASCII diagram (renders in all GitHub views)

•	Consistent heading hierarchy throughout

---

## 11. Problems Faced & Solutions

### Problem 1 — Claude API returning unstructured text instead of JSON

**Problem:** The `/simulate` endpoint sometimes received plain-text responses from Claude instead of valid JSON, causing `json.loads()` to crash.

**Solution:** Added a strict JSON-only instruction at the top of the prompt (`Respond ONLY with valid JSON:`), plus a `try/except` block around `json.loads()` with a fallback mock result so the UI never breaks even if the API misbehaves.

---

### Problem 2 — Chart.js not updating dynamically

**Problem:** After adding emails, the pie and line charts did not update — they stayed empty.

**Solution:** The `updateCharts()` function had to call both `.data.datasets[0].data = [...]` and `.update()` on each chart object after every new email. The chart instances (`pieChart`, `lineChart`) were stored in global scope so they remained accessible across function calls.

---

### Problem 3 — Tab switching broke the feed filter buttons

**Problem:** The filter buttons (All / Scam / Safe) inside the Dashboard tab shared the same `.tab` CSS class as the top navigation tabs. Clicking a filter button would accidentally deactivate the Dashboard tab styling.

**Solution:** Scoped the tab selector in `filterFeed()` to `#tab-dashboard .tabs .tab` instead of the global `.tabs .tab`, so filter buttons and nav buttons are styled independently.

---

### Problem 4 — FAISS not available on Windows without additional setup

**Problem:** `faiss-cpu` failed to install on Windows directly, causing the backend to crash on startup.

**Solution:** Used a simplified in-memory list (`RAG_MEMORY`) as a mock FAISS store for local development. On Linux/Render.com deployment, `faiss-cpu` installs cleanly. A note in `requirements.txt` documents this.

---

### Problem 5 — Modal submit with no backend running caused uncaught error

**Problem:** When running the frontend without the Flask backend (e.g., opening `index.html` directly), clicking Analyze threw an unhandled network error.

**Solution:** Added a `catch` block to `submitEmail()` that falls back to a mock scam result using basic keyword matching. This makes the UI fully demoable even without the backend, which is helpful for class presentations.

---

### Problem 6 — Gmail IMAP connection refused on some networks

**Problem:** IMAP access to Gmail was blocked on college network firewalls, preventing real inbox scanning.

**Solution:** The app gracefully falls back to the "Manual Simulate" mode, which uses the same Claude AI analysis pipeline without requiring IMAP. The inbox scan feature works on unrestricted networks or when "Less secure app access" / App Passwords are configured in Gmail settings.

---

<br>
