import streamlit as st
from fp_ingest import load_qa_kb, build_index
from agentic_assistant import AgenticRAG

# --- Load the data and create the agent ---
@st.cache_resource
def load_agent():
    documents = load_qa_kb()
    index = build_index(documents)
    return AgenticRAG(index)

# --- Page setup ---
st.set_page_config(page_title="Dancing Plague Assistant", page_icon="🕺")
st.title("🕺 Dancing Plague of 1518 - History Tutor")
st.markdown("Ask me anything about the Dancing Plague of 1518!")

# --- Load the agent ---
agent = load_agent()

# --- Chat interface ---
user_input = st.text_input("Your question:", placeholder="e.g., What caused the dancing plague?")

if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            answer = agent.ask(user_input)
        st.success("Answer:")
        st.write(answer)
    else:
        st.warning("Please enter a question first.")