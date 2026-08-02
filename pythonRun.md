### Running the project with Python 🐍

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