import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# --- Get the project root folder ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_FILE = os.path.join(PROJECT_ROOT, "feedback.csv")

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Dancing Plague Assistant - Dashboard")

# --- Load feedback data ---
def load_feedback():
    try:
        df = pd.read_csv(FEEDBACK_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# --- Add a refresh button ---
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

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

st.divider()

# --- Row 1: Two charts side by side ---
col_left, col_right = st.columns(2)

# --- Chart 1: Pie Chart - Feedback Distribution ---
with col_left:
    st.subheader("Feedback Distribution")
    
    feedback_counts = df["feedback"].value_counts()
    labels = []
    values = []
    colors = []
    
    for val, count in feedback_counts.items():
        if val == 1:
            labels.append("👍 Helpful")
            colors.append("#4CAF50")
        else:
            labels.append("👎 Not Helpful")
            colors.append("#FF6B6B")
        values.append(count)
    
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# --- Chart 2: Donut Chart - Most Asked Topics ---
with col_right:
    st.subheader("Most Asked Topics")
    
    def categorize_question(q):
        q_lower = q.lower()
        if any(word in q_lower for word in ["cause", "why", "trigger", "start", "began", "caused"]):
            return "Causes & Origins"
        elif any(word in q_lower for word in ["die", "death", "dead", "kill", "fatal"]):
            return "Deaths & Fatalities"
        elif any(word in q_lower for word in ["theory", "modern", "psychogenic", "hysteria", "illness", "psychological"]):
            return "Modern Theories"
        elif any(word in q_lower for word in ["book", "film", "movie", "fiction", "video", "inspire"]):
            return "Pop Culture"
        else:
            return "General"
    
    df["topic"] = df["question"].apply(categorize_question)
    topic_counts = df["topic"].value_counts()
    
    fig2, ax2 = plt.subplots()
    wedges, texts, autotexts = ax2.pie(
        topic_counts.values, 
        labels=topic_counts.index, 
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig2.gca().add_artist(centre_circle)
    ax2.axis('equal')
    st.pyplot(fig2)

st.divider()

# --- Chart 3: Gauge Chart - Average Response Time ---
st.subheader("📊 Average Response Time")

fig3, ax3 = plt.subplots(figsize=(6, 3))

if avg_response_time < 2.0:
    color = "#4CAF50"
    status = "Fast ⚡"
elif avg_response_time < 4.0:
    color = "#FFC107"
    status = "Okay 🟡"
else:
    color = "#FF6B6B"
    status = "Slow 🐢"

ax3.barh(0, 1, color="#E0E0E0", height=0.3)
ax3.barh(0, min(avg_response_time / 10, 1), color=color, height=0.3)

ax3.set_xlim(0, 10)
ax3.set_xlabel("Response Time (seconds)")
ax3.set_yticks([])
ax3.set_ylim(-0.5, 0.5)

ax3.text(avg_response_time + 0.3, 0, f"{avg_response_time:.2f}s", 
         fontsize=14, fontweight='bold', va='center')
ax3.text(10.5, 0, status, fontsize=12, fontweight='bold', color=color, va='center')

ax3.axvline(x=2.0, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
ax3.axvline(x=4.0, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
ax3.text(2.0, -0.3, '2s', fontsize=8, color='gray', ha='center')
ax3.text(4.0, -0.3, '4s', fontsize=8, color='gray', ha='center')

st.pyplot(fig3)

st.divider()

# --- Chart 4: Response time over time ---
st.subheader("Response Time Over Time")
df_response = df[["timestamp", "response_time"]].copy()
df_response = df_response.set_index("timestamp")
st.line_chart(df_response)

# --- Chart 5: Questions per day ---
st.subheader("Questions Per Day")
questions_per_day = df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")
questions_per_day.columns = ["Date", "Questions"]
st.bar_chart(questions_per_day.set_index("Date"))

# --- Recent feedback table ---
st.divider()
st.subheader("Recent Feedback")
st.dataframe(df.tail(10))