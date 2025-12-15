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

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def generate_response(rating, review):
    prompt = f"""
You are a polite customer support assistant.

Customer Rating: {rating}
Customer Review: "{review}"

Reply politely and empathetically.
"""
    try:
        resp = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role":"user","content":prompt}],
            temperature=0.5
        )
        return resp.choices[0].message.content
    except:
        return "Thank you for your feedback!"

# ---------- UI ----------
st.title("Customer Review")

rating = st.selectbox("Rating", [1,2,3,4,5])
review = st.text_area("Write your review")

if st.button("Submit"):
    ai_reply = generate_response(rating, review)

    df = load_data()
    df.loc[len(df)] = [rating, review, ai_reply, "", ""]
    save_data(df)

    st.success("Review submitted!")
    st.write("### AI Response")
    st.write(ai_reply)
