import streamlit as st
import pandas as pd
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

DATA_FILE = "reviews.csv"

if not os.path.exists(DATA_FILE):
    pd.DataFrame(
        columns=["rating","review","ai_response","summary","recommended_action"]
    ).to_csv(DATA_FILE, index=False)

st.title("User Dashboard")

rating = st.selectbox("Rating", [1,2,3,4,5])
review = st.text_area("Write your review")

if st.button("Submit"):
    prompt = f"""
You are a polite customer support assistant.
Rating: {rating}
Review: "{review}"
"""
    resp = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role":"user","content":prompt}]
    )

    ai_response = resp.choices[0].message.content

    df = pd.read_csv(DATA_FILE)
    df.loc[len(df)] = [rating, review, ai_response, "", ""]
    df.to_csv(DATA_FILE, index=False)

    st.success("Review submitted!")
    st.write("### AI Response")
    st.write(ai_response)
