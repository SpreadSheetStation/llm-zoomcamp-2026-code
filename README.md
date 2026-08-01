# 🕺 Dancing Plague of 1518 - History Tutor (LLMzc_Final_Project)
Hello there! Welcome to my Final Capstone Project for the LLM Zoomcamp 2026!

An AI-powered history tutor that answers questions about the Dancing Plague of 1518 using Retrieval-Augmented Generation (RAG) with an agentic approach.

This project was built as my Final Capstone Project for the LLM Zoomcamp by DataTalks.Club.

✨👋🏻 For Peer Reviewers [click here](./evaluationCriteria.md) for reviewing help.
---

## 📁 Important: Where to Find the Project

This repository contains **three folders**:
- 🙅🏻‍♂️ `Images/` – Contains images only for this README.md. **Please ignore this folder.**
- 🙅🏻‍♂️ `llm-zoomcamp-2026-code/` – Contains homework and testing code from the course. **Please ignore this folder.**
- 💡 `LLMzc_Final_Project/` – **This is the main project folder.** All the code for the Dancing Plague History Tutor is inside this folder.

**For reviewers:** Please `cd` into `LLMzc_Final_Project` before running any commands.

```bash
cd LLMzc_Final_Project
```

All instructions below assume you are in the `LLMzc_Final_Project` folder.

---

## 📋 Project Overview

### Problem Statement

Students and history enthusiasts often have questions about historical events like the Dancing Plague of 1518. Finding accurate answers from scattered online sources is time-consuming. This project solves that problem by building a specialized AI assistant that:

- Answers questions using a curated knowledge base
- Uses an agentic approach that searches multiple times to find the best answer
- Provides a clean web interface for asking questions and viewing responses
- Tracks user feedback and response times through a live dashboard

### Dataset

The knowledge base consists of 10 question-answer pairs about the Dancing Plague of 1518, covering:
- What happened (the outbreak itself)
- Causes and theories (psychogenic, ergotism)
- Death toll and fatalities
- Pop culture references (books, films)

---

## 🚀 How to Run the Project

> **Important:** All commands below must be run from the `LLMzc_Final_Project` folder.

```bash
# First, navigate to the project folder
cd LLMzc_Final_Project
```

### Prerequisites

- **Option A (Python):** Python 3.12+ and an OpenAI API key
- **Option B (Docker):** Docker Desktop installed

---

### Option A: Run with Python

```bash
# 1. Clone the repository
git clone https://github.com/SpreadSheetStation/llm-zoomcamp-2026-code
cd llm-zoomcamp-2026-code/LLMzc_Final_Project

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the main app
streamlit run streamlit_app.py
# Open http://localhost:8501

# 6. Run the dashboard (in a separate terminal)
streamlit run dashboard.py --server.port=8502
# Open http://localhost:8502
```

---

### Option B: Run with Docker (Recommended for Reviewers)

```bash
# 1. Clone the repository
git clone https://github.com/SpreadSheetStation/llm-zoomcamp-2026-code
cd llm-zoomcamp-2026-code/LLMzc_Final_Project

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Build the container
docker build -t dancing-plague-app .

# 4. Run the container (both app and dashboard start automatically)
docker run -p 8501:8501 -p 8502:8502 dancing-plague-app

# 5. Open your browser:
# Main app: http://localhost:8501
# Dashboard: http://localhost:8502
```

> 💡 **Tip for reviewers:** Docker is the easiest way to run this project. Both apps start with one command.

---

## 📁 Project Structure

```
llm-zoomcamp-2026-code/          # Course homework (ignore)
└── LLMzc_Final_Project/         # ⭐ MAIN PROJECT FOLDER
    ├── DataSource/
    │   └── qa_knowledge_base.csv
    ├── GroundTruth/
    │   ├── my_ground_truth.csv
    │   ├── rag_answers.csv
    │   ├── agent_answers.csv
    │   ├── rag_judged.csv
    │   └── agent_judged.csv
    ├── streamlit_app.py         # Main chat interface
    ├── dashboard.py             # Analytics dashboard
    ├── agentic_assistant.py     # Agentic RAG (WINNER)
    ├── fp_rag_helper.py         # Standard RAG (baseline)
    ├── fp_ingest.py             # Data loading and indexing
    ├── evaluate_rag.py          # RAG evaluation
    ├── evaluate_agent.py        # Agent evaluation
    ├── evaluate_judge.py        # LLM judge
    ├── Dockerfile               # Containerization
    ├── start.sh                 # Start both apps in Docker
    ├── requirements.txt         # Python dependencies
    ├── .env.example             # Environment variables template
    └── feedback.csv             # User feedback (auto-created)
```

---


## 🔧 Configuration

Create a `.env` file from `.env.example`:

```bash
OPENAI_API_KEY=your_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

---

## 📈 Monitoring Dashboard

The dashboard shows:

- **Feedback distribution** – Pie chart of thumbs up/down
- **Most asked topics** – Donut chart of question categories
- **Average response time** – Gauge chart with color coding
- **Response time over time** – Line chart
- **Questions per day** – Bar chart
- **Recent feedback** – Table of latest interactions

---

## 🐳 Docker

The project is containerized with Docker for easy setup.

```bash
# Build
docker build -t dancing-plague-app .

# Run (both app and dashboard start automatically)
docker run -p 8501:8501 -p 8502:8502 dancing-plague-app
```

Then open:
- Main app: http://localhost:8501
- Dashboard: http://localhost:8502

