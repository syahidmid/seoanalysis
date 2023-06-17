import pandas as pd
import streamlit as st


@st.cache_data(ttl=600)
def load_mediao(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)


@st.cache_data(ttl=600)
def load_serpdata(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)
