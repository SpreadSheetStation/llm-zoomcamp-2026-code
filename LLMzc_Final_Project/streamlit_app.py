import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from fp_ingest import load_qa_kb, build_index
from agentic_assistant import AgenticRAG

# --- Get the project root folder ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_FILE = os.path.join(PROJECT_ROOT, "feedback.csv")
print(f"📁 Feedback will be saved to: {FEEDBACK_FILE}")

# --- Load the data and create the agent ---
@st.cache_resource
def load_agent():
    documents = load_qa_kb()
    index = build_index(documents)
    return AgenticRAG(index)

# --- Function to save feedback ---
def save_feedback(question, answer, feedback, response_time):
    timestamp = datetime.now().isoformat()
    
    # Create a simple dictionary
    data = {
        "timestamp": timestamp,
        "question": question,
        "answer": answer,
        "feedback": feedback,
        "response_time": response_time
    }
    
    df_new = pd.DataFrame([data])
    
    # Try to append to existing file, or create new one
    if os.path.exists(FEEDBACK_FILE):
        df_existing = pd.read_csv(FEEDBACK_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(FEEDBACK_FILE, index=False)
        print(f"✅ Appended feedback to {FEEDBACK_FILE}")
    else:
        df_new.to_csv(FEEDBACK_FILE, index=False)
        print(f"✅ Created new feedback file at {FEEDBACK_FILE}")

# --- Page setup ---
st.set_page_config(page_title="Dancing Plague Assistant", page_icon="🕺")
st.title("🕺 Dancing Plague of 1518 - History Tutor")
st.markdown("Ask me anything about the Dancing Plague of 1518!")

# --- Load the agent ---
agent = load_agent()

# --- Initialize session state ---
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "response_time" not in st.session_state:
    st.session_state.response_time = 0.0

# --- Chat interface ---
user_input = st.text_input("Your question:", placeholder="e.g., What caused the dancing plague?")

if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            start_time = time.time()
            answer = agent.ask(user_input)
            response_time = time.time() - start_time
            
            # Store in session state
            st.session_state.last_question = user_input
            st.session_state.last_answer = answer
            st.session_state.response_time = response_time
            
        st.success("Answer:")
        st.write(answer)
        st.caption(f"⏱️ Response time: {response_time:.2f} seconds")
    else:
        st.warning("Please enter a question first.")

# --- Feedback buttons (always visible, but only work if there's a last answer) ---
st.divider()
st.subheader("Was this answer helpful?")

col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Helpful", key="thumbs_up"):
        if st.session_state.last_question:
            save_feedback(
                st.session_state.last_question,
                st.session_state.last_answer,
                1,
                st.session_state.response_time
            )
            st.success("Thank you for your feedback! 👍")
        else:
            st.warning("Please ask a question first!")

with col2:
    if st.button("👎 Not Helpful", key="thumbs_down"):
        if st.session_state.last_question:
            save_feedback(
                st.session_state.last_question,
                st.session_state.last_answer,
                -1,
                st.session_state.response_time
            )
            st.success("Thank you for your feedback! 👎")
        else:
            st.warning("Please ask a question first!")