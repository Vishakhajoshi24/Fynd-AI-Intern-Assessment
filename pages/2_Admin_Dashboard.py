import streamlit as st
import pandas as pd
import os

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
            st.markdown("### Review")
            st.write(f" Rating: {row['rating']}")
            st.write(row['review'])

            st.markdown("### AI Response")
            st.write(row['ai_response'])

            st.divider()

