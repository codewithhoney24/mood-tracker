import streamlit as st
import pandas as pd
import datetime
import csv
import os

MOOD_FILE = "mood_log.csv"

# Function to read mood data from CSV
def load_mood_data():
    if not os.path.exists(MOOD_FILE) or os.stat(MOOD_FILE).st_size == 0:
        return pd.DataFrame(columns=["Date", "Mood"])
    
    df = pd.read_csv(MOOD_FILE, names=["Date", "Mood"], skiprows=1)
    df.columns = df.columns.str.strip()  # Remove any spaces in column names
    return df

# Function to save mood entry
def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)
    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Mood"])  # Write headers if file is new
        writer.writerow([date, mood])

# Apply CSS for styling
st.markdown("""
    <style>
        body, .stApp { background-color: black; color: white; }
        h1, h2, h3, h4, h5, h6, p, label { color: white; }
        .stButton>button { background: linear-gradient(90deg, #ff7e5f, #feb47b); color: white; }
        .stButton>button:hover { background: linear-gradient(90deg, #ff512f, #dd2476); }
        .stSelectbox, .stTextInput { background-color: #222; color: white; }
    </style>
    """, unsafe_allow_html=True)

# App UI
st.title("📝 Mood Tracker")
today = datetime.date.today()
st.subheader("😊 How are you feeling today?")
mood = st.selectbox("Select your mood", ["Happy", "Sad", "Angry", "Neutral"])

if st.button("Log Mood"):
    save_mood_data(today, mood)
    st.success("✅ Mood Logged Successfully!")

# Load and display mood data
data = load_mood_data()

if not data.empty:
    st.subheader("📊 Mood Trends Over Time")
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")  # Handle errors
    mood_counts = data["Mood"].value_counts()  # Count occurrences of each mood
    st.bar_chart(mood_counts)

st.write("Built with ❤️ by [Nousheen Atif](https://github.com/codewithhoney)")
