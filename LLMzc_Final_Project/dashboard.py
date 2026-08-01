import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

# --- Get the project root folder ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_FILE = os.path.join(PROJECT_ROOT, "feedback.csv")

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Dancing Plague Assistant - Dashboard")

# --- Load feedback data ---
@st.cache_data
def load_feedback():
    try:
        df = pd.read_csv(FEEDBACK_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_feedback()

# --- Check if we have data ---
if df.empty:
    st.warning("No feedback data available yet. Ask some questions first!")
    st.stop()

# --- Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

total_questions = len(df)
total_thumbs_up = (df["feedback"] == 1).sum()
total_thumbs_down = (df["feedback"] == -1).sum()
avg_response_time = df["response_time"].mean()

col1.metric("Total Questions", total_questions)
col2.metric("👍 Thumbs Up", total_thumbs_up)
col3.metric("👎 Thumbs Down", total_thumbs_down)
col4.metric("Avg Response Time", f"{avg_response_time:.2f}s")

st.divider()

# --- Chart 1: Feedback over time ---
st.subheader("Feedback Over Time")
feedback_by_day = df.groupby(df["timestamp"].dt.date)["feedback"].sum().reset_index()
feedback_by_day.columns = ["Date", "Net Feedback"]
st.line_chart(feedback_by_day.set_index("Date"))

# --- Chart 2: Thumbs up vs thumbs down ---
st.subheader("Thumbs Up vs Thumbs Down")
thumbs_counts = df["feedback"].value_counts().sort_index(ascending=False)
thumbs_counts.index = ["👍 Helpful", "👎 Not Helpful"]
st.bar_chart(thumbs_counts)

# --- Chart 3: Response time over time ---
st.subheader("Response Time Over Time")
df_response = df[["timestamp", "response_time"]].copy()
df_response = df_response.set_index("timestamp")
st.line_chart(df_response)

# --- Chart 4: Response time distribution ---
st.subheader("Response Time Distribution")
fig, ax = plt.subplots()
ax.hist(df["response_time"], bins=10, edgecolor="black")
ax.set_xlabel("Response Time (seconds)")
ax.set_ylabel("Number of Questions")
st.pyplot(fig)

# --- Chart 5: Questions per day ---
st.subheader("Questions Per Day")
questions_per_day = df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")
questions_per_day.columns = ["Date", "Questions"]
st.bar_chart(questions_per_day.set_index("Date"))

# --- Chart 6: Average response time by date ---
st.subheader("Average Response Time by Date")
avg_response_by_day = df.groupby(df["timestamp"].dt.date)["response_time"].mean().reset_index()
avg_response_by_day.columns = ["Date", "Avg Response Time"]
st.line_chart(avg_response_by_day.set_index("Date"))

# --- Chart 7: Most asked questions ---
st.subheader("Most Asked Questions")
top_questions = df["question"].value_counts().head(5).reset_index()
top_questions.columns = ["Question", "Count"]
st.bar_chart(top_questions.set_index("Question"))

# --- Recent feedback table ---
st.divider()
st.subheader("Recent Feedback")
st.dataframe(df.tail(10).drop(columns=["question_length"]))