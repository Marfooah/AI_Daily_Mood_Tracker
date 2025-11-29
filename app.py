# app.py — Daily Mood Tracker (Streamlit + Groq)

import os
import json
import re
from datetime import datetime, timezone

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# ---------------------------------------
# Configuration
# ---------------------------------------
st.set_page_config(page_title="Daily Mood Tracker", layout="wide")

DATA_FILE = "data.json"
MOOD_CATEGORIES = ["happy", "sad", "stressed", "angry", "anxious", "neutral", "excited"]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# ---------------------------------------
# Helpers for file storage
# ---------------------------------------
def load_entries():
    try:
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print("🔥 load_entries ERROR:", e)
        return []


def save_entry(entry):
    try:
        entries = load_entries()
        entries.append(entry)
        with open(DATA_FILE, "w") as f:
            json.dump(entries, f, indent=4)
    except Exception as e:
        print("🔥 save_entry ERROR:", e)


# ---------------------------------------
# Groq model call
# ---------------------------------------
def analyze_mood_with_groq(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are a mood analysis assistant. Extract the following:

                    1. mood (one word)
                    2. summary (1 sentence)
                    3. suggestion (Islamic reminder)

                    Respond ONLY in JSON:
                    {{
                      "mood": "...",
                      "summary": "...",
                      "suggestion": "..."
                    }}

                    User: {text}
                    """
                }
            ]
        )

        raw = response.choices[0].message.content.strip()

        # extract JSON
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("Groq returned invalid JSON")

        return json.loads(match.group())

    except Exception as e:
        print("🔥 ERROR in Groq:", e)
        return {
            "mood": "neutral",
            "summary": "Could not analyze because of an error.",
            "suggestion": "Take a breath. Allah sees your patience."
        }


# ---------------------------------------
# Plotting
# ---------------------------------------
def plot_distribution(dist):
    fig, ax = plt.subplots(figsize=(5, 4))
    if not dist:
        ax.text(0.5, 0.5, "No data yet", ha='center')
        return fig

    labels, values = zip(*dist.items())
    ax.bar(labels, values)
    ax.set_ylabel("Percentage")
    ax.set_title("Mood Distribution (%)")
    return fig


def plot_time_series(ts):
    fig, ax = plt.subplots(figsize=(6, 4))
    if not ts:
        ax.text(0.5, 0.5, "Not enough data", ha='center')
        return fig

    dates = [d["date"] for d in ts]
    counts = [d["count"] for d in ts]

    ax.plot(dates, counts)
    ax.set_title("Mood Entries Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Entries")
    fig.autofmt_xdate()
    return fig


# ---------------------------------------
# Dashboard calculation
# ---------------------------------------
def generate_dashboard():
    entries = load_entries()
    if not entries:
        return {
            "distribution": {},
            "time_series": [],
            "most_7d": "None",
            "most_30d": "None"
        }

    df = pd.DataFrame(entries)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    now = datetime.now(timezone.utc)

    # 7 days & 30 days
    last_7 = df[df["timestamp"] >= now - pd.Timedelta(days=7)]
    last_30 = df[df["timestamp"] >= now - pd.Timedelta(days=30)]

    most_7d = last_7["mood"].mode().iloc[0] if not last_7.empty else "None"
    most_30d = last_30["mood"].mode().iloc[0] if not last_30.empty else "None"

    # distribution
    dist = df["mood"].value_counts(normalize=True).mul(100).round(1).to_dict()

    # time series
    ts = (
        df.groupby(df["timestamp"].dt.date)
          .size()
          .reset_index(name="count")
    )
    ts_list = ts.rename(columns={"timestamp": "date"}).to_dict(orient="records")

    return {
        "distribution": dist,
        "time_series": ts_list,
        "most_7d": most_7d,
        "most_30d": most_30d
    }


# ---------------------------------------
# STREAMLIT UI
# ---------------------------------------
st.markdown("<h1 style='text-align:center;'>Daily Mood Tracker</h1>", unsafe_allow_html=True)

tabs = st.tabs(["Enter Mood", "Analytics", "Data"])

# -----------------------------
# TAB 1 — Enter Mood
# -----------------------------
with tabs[0]:
    st.subheader("How are you feeling today?")

    with st.form("mood_form"):
        user_text = st.text_area("Write your mood entry", height=150)
        submit = st.form_submit_button("Analyze & Save")

    if submit:
        if not user_text.strip():
            st.warning("Write something first.")
        else:
            analysis = analyze_mood_with_groq(user_text)

            timestamp = datetime.now(timezone.utc).isoformat()
            entry_data = {
                "timestamp": timestamp,
                "text": user_text,
                "mood": analysis.get("mood", "neutral"),
                "summary": analysis.get("summary", ""),
                "suggestion": analysis.get("suggestion", "")
            }
            save_entry(entry_data)

            st.success("Saved!")
            st.write("### Mood:", analysis["mood"])
            st.write("### Summary:", analysis["summary"])
            st.write("### Suggestion:", analysis["suggestion"])


# -----------------------------
# TAB 2 — Analytics
# -----------------------------
with tabs[1]:
    st.subheader("Mood Analytics")
    if st.button("Refresh Dashboard"):
        stats = generate_dashboard()

        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(plot_distribution(stats["distribution"]))

        with col2:
            st.pyplot(plot_time_series(stats["time_series"]))

        st.write(f"**Most frequent (last 7 days):** {stats['most_7d']}")
        st.write(f"**Most frequent (last 30 days):** {stats['most_30d']}")

        if stats["distribution"]:
            st.write("### Breakdown")
            for k, v in stats["distribution"].items():
                st.write(f"- {k}: {v}%")


# -----------------------------
# TAB 3 — Data
# -----------------------------
with tabs[2]:
    st.subheader("All Entries")
    data = load_entries()
    df = pd.DataFrame(data)
    st.dataframe(df if not df.empty else pd.DataFrame(columns=["timestamp","text","mood","summary","suggestion"]))
