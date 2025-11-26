import streamlit as st
from src.DB import DBConn
import pandas as pd
import json

st.title("Data Connector")

col1, col2, col3 = st.columns(3)

with col1:
    dbs = st.selectbox(
        "What type of database are you using?",
        ("Postgres", "Oracle", "Snowflake"),
        index=None,
        placeholder="Select database...",
    )
with col2:
    auth = st.file_uploader("Upload Json authentication file", type="json")

with col3:
    model = st.file_uploader("Upload Json Model file", type="json")

auth_json = {}
model_json = {}

if auth is not None:
    auth_json = json.load(auth)
    st.write(auth_json)

if model is not None:
    model_json = json.load(model)
    st.write(model_json)

# Fetch variables
USER = auth_json["user"]
PASSWORD = auth_json["password"]
HOST = auth_json["host"]
PORT = auth_json["port"]
DBNAME = auth_json["database"]
TABLE = auth_json["table"]

go = st.button(label="GET !")

@st.cache_data
def fetch_data() -> pd.DataFrame:
    C = DBConn(USER, PASSWORD, DBNAME,HOST, PORT)

    with C.connect_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {TABLE}")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        cur.close()
        conn.close()
    return df

if go:
    if dbs == "Postgres":
        try:
            data = fetch_data()
            data = data.drop('IDpol', axis=1)
            # Initialization
            if 'data' not in st.session_state:
                st.session_state['data'] = data
                st.dataframe(data.head())
                st.success("Data found")

        except Exception as e:
            st.error(e)
    else:
        st.error("Oracle and Snowflake database are not connected yet :pensive:")


if 'data' not in st.session_state:
    st.warning("No data found")



