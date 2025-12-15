import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# ---------- OpenRouter ----------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

DATA_FILE = "reviews.csv"

# ---------- Helpers ----------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["rating","review","ai_response","summary","recommended_action"])

def generate_summary(review):
    prompt = f"""
Summarize the following customer review in one short sentence:

"{review}"
"""
    resp = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content.strip()

def generate_action(review):
    prompt = f"""
Based on the following customer review, suggest one recommended action for the business:

"{review}"
"""
    resp = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content.strip()

# ---------- UI ----------
st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("Admin Dashboard – Customer Feedback")

df = load_data()

if df.empty:
    st.info("No reviews submitted yet.")
else:
    # Generate AI insights if missing
    for i, row in df.iterrows():
        if pd.isna(row["summary"]) or row["summary"] == "":
            df.at[i, "summary"] = generate_summary(row["review"])
        if pd.isna(row["recommended_action"]) or row["recommended_action"] == "":
            df.at[i, "recommended_action"] = generate_action(row["review"])

    df.to_csv(DATA_FILE, index=False)

    st.dataframe(df, use_container_width=True)

    st.subheader("Basic Analytics")
    st.write("Average Rating:", round(df["rating"].mean(), 2))
    st.write("Total Reviews:", len(df))
