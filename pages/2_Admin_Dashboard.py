import streamlit as st
import pandas as pd
import os

DATA_FILE = "reviews.csv"

st.title("📊 Admin Dashboard")

if not os.path.exists(DATA_FILE):
    st.info("No reviews submitted yet.")
else:
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        st.info("No reviews submitted yet.")
    else:
        st.dataframe(df, use_container_width=True)
