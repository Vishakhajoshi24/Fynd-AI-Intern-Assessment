import streamlit as st
import pandas as pd
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

DATA_FILE = "reviews.csv"

st.title("Admin Dashboard")

if not os.path.exists(DATA_FILE):
    st.info("No reviews submitted yet.")
else:
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        st.info("No reviews submitted yet.")
    else:
        for i, row in df.iterrows():
            if row["summary"] == "":
                df.at[i,"summary"] = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[{"role":"user","content":f"Summarize: {row['review']}"}]
                ).choices[0].message.content

            if row["recommended_action"] == "":
                df.at[i,"recommended_action"] = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[{"role":"user","content":f"Suggest business action: {row['review']}"}]
                ).choices[0].message.content

        df.to_csv(DATA_FILE, index=False)
        st.dataframe(df, use_container_width=True)
