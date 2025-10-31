import streamlit as st
from src.DB import DBConn
import pandas as pd

st.title("Data Exploration")

@st.cache_data
def fetch_data() -> pd.DataFrame:
    C = DBConn("postgres", "postgres", "frenchmtpldb", "localhost", 2022)

    with C.connect_postgres() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM frenchmtpl_table")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        cur.close()
        conn.close()
    return df

data = fetch_data()
# Initialization
if 'data' not in st.session_state:
    st.session_state['data'] = data

st.dataframe(data)



