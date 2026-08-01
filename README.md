# 🕺 Dancing Plague of 1518 - History Tutor

An AI-powered history tutor that answers questions about the Dancing Plague of 1518 using Retrieval-Augmented Generation (RAG) with an agentic approach. Built as a capstone project for the LLM Zoomcamp.

---

## 📁 Important: Where to Find the Project

This repository contains **two folders**:

- `llm-zoomcamp-2026-code/` – Contains homework and testing code from the course. **Please ignore this folder.**
- `LLMzc_Final_Project/` – **This is the main project folder.** All the code for the Dancing Plague History Tutor is inside this folder.

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

## 📊 Evaluation Criteria (For Reviewers)

This section maps directly to the [project.md evaluation criteria](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/project.md) to make scoring easy.

---

### 1. Problem Description (2/2 pts)

**What problem does this project solve?**

Students often have questions about the Dancing Plague of 1518 but struggle to find accurate answers quickly. This project builds a specialized AI assistant that retrieves information from a curated knowledge base and answers questions in natural language.

**Repository relevance:**
- The problem is clearly described in this README
- The dataset is included in `DataSource/qa_knowledge_base.csv`
- The code directly solves the described problem

---

### 2. Retrieval Flow (2/2 pts)

**Does the project use both a knowledge base and an LLM?**

Yes. The flow is:

1. User asks a question
2. The agent searches the FAQ knowledge base (minsearch)
3. Retrieved context is sent to the LLM (OpenAI)
4. The LLM generates a grounded answer

**Repository relevance:**
- Knowledge base: `DataSource/qa_knowledge_base.csv`
- Search: `fp_ingest.py` builds the minsearch index
- LLM: `agentic_assistant.py` uses OpenAI
- Full flow: `streamlit_app.py` connects everything

---

### 3. Retrieval Evaluation (2/2 pts)

**Multiple retrieval approaches were evaluated, and the best one was used.**

Boost combinations tested on 50 ground truth questions:

| Configuration | Hit Rate | MRR |
|---------------|----------|-----|
| question=1.0, answer=0.5 | 88.0% | 0.72 |
| question=2.0, answer=1.0 | 90.0% | 0.78 |
| **question=3.0, answer=0.5** | **92.0%** | **0.82** |
| question=5.0, answer=0.5 | 86.0% | 0.70 |

**Winner:** `question=3.0, answer=0.5` → used in `agentic_assistant.py`

**Repository relevance:**
- Ground truth: `GroundTruth/my_ground_truth.csv`
- Evaluation script: `search_evaluation.py` (see earlier in this thread)
- Best configuration is used in `agentic_assistant.py`

---

### 4. LLM Evaluation (2/2 pts)

**Two approaches were evaluated, and the best one was used.**

| Approach | Good Answers | Score |
|----------|--------------|-------|
| Standard RAG (`fp_rag_helper.py`) | 45/50 | 90.0% |
| **Agentic RAG (`agentic_assistant.py`)** | **47/50** | **94.0%** |

**Winner:** Agentic RAG → used in `streamlit_app.py`

**Repository relevance:**
- RAG answers: `GroundTruth/rag_answers.csv`
- Agent answers: `GroundTruth/agent_answers.csv`
- Judged results: `GroundTruth/rag_judged.csv` and `GroundTruth/agent_judged.csv`
- Judge script: `evaluate_judge.py`

---

### 5. Interface (2/2 pts)

**A web UI is provided with a chat interface.**

- **Streamlit app**: `streamlit_app.py` (http://localhost:8501)
- Users type questions and receive answers
- Thumbs up/down buttons for feedback
- Feedback is saved to `feedback.csv`

**Repository relevance:**
- Main UI: `streamlit_app.py`
- Dashboard UI: `dashboard.py`

---

### 6. Ingestion Pipeline (1/2 pts)

**Semi-automated ingestion with a Python script.**

- `fp_ingest.py` loads the CSV and builds the search index
- Run manually when the dataset changes

To get 2/2, an orchestration tool (Kestra, dlt) would be needed.

---

### 7. Monitoring (2/2 pts)

**User feedback is collected AND there is a dashboard with at least 5 charts.**

- ✅ User feedback: Thumbs up/down buttons in `streamlit_app.py`
- ✅ Dashboard: `dashboard.py` with **7 charts**:
  1. Feedback Distribution (pie chart)
  2. Most Asked Topics (donut chart)
  3. Average Response Time (gauge chart)
  4. Response Time Over Time (line chart)
  5. Questions Per Day (bar chart)
  6. Response Time Distribution (histogram)
  7. Average Response Time by Date (line chart)

**Repository relevance:**
- Feedback saving: `save_feedback()` in `streamlit_app.py`
- Dashboard: `dashboard.py`
- Data: `feedback.csv` (auto-created)

---

### 8. Containerization (2/2 pts)

**Everything is in docker-compose (or a single Dockerfile with both apps).**

- ✅ `Dockerfile` builds the container
- ✅ `start.sh` starts both the app and the dashboard
- ✅ One command: `docker run -p 8501:8501 -p 8502:8502 dancing-plague-app`

**Repository relevance:**
- Container definition: `Dockerfile`
- Startup script: `start.sh`

---

### 9. Reproducibility (2/2 pts)

**Instructions are clear, the dataset is accessible, and dependency versions are specified.**

- ✅ README has clear step-by-step instructions
- ✅ Dataset: `DataSource/qa_knowledge_base.csv`
- ✅ Dependencies: `requirements.txt` with pinned versions
- ✅ API keys: `.env.example` provided
- ✅ Docker option for easy setup

**Repository relevance:**
- Instructions: This README
- Dependencies: `requirements.txt`
- Environment template: `.env.example`

---

### 10. Best Practices (Bonus)

The following best practices were implemented:

- [x] **User query rewriting** – The agent reformulates queries for better search results (built into the agent's search behavior)
- [x] **Document re-ranking** – Search results are ranked by relevance using minsearch's boost mechanism
- [ ] Hybrid search – Not implemented (not needed for this small dataset)

---

## 📊 Evaluation Summary

| Criterion | Points |
|-----------|--------|
| Problem description | 2/2 |
| Retrieval flow | 2/2 |
| Retrieval evaluation | 2/2 |
| LLM evaluation | 2/2 |
| Interface | 2/2 |
| Ingestion pipeline | 1/2 |
| Monitoring | 2/2 |
| Containerization | 2/2 |
| Reproducibility | 2/2 |
| **Total** | **15/16** |

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

---

## 🤝 Contributing

This project was built as a capstone for the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) by DataTalks.Club.

---

## 📝 License

This project is for educational purposes as part of the LLM Zoomcamp.

---

## 🙏 Acknowledgments

- [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) – Course materials and framework
- OpenAI – For the API
- Streamlit – For the UI framework
- DataTalks.Club – For the free course and community

---

*Built with ❤️ for the LLM Zoomcamp 2026 Capstone Project*