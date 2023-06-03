import pandas as pd
import streamlit as st

st.title("SEO Dashboard")


# Read in data from the Google Sheet.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)


df = load_data(st.secrets["public_gsheets_URL"])
st.dataframe(df)
