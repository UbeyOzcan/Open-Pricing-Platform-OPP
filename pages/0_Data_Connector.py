import streamlit as st
from src.DB import DBConn
import pandas as pd
import json
import numpy as np

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


if auth is not None:
    st.session_state["auth"] = json.load(auth)
    USER = st.session_state["auth"]["user"]
    PASSWORD = st.session_state["auth"]["password"]
    HOST = st.session_state["auth"]["host"]
    PORT = st.session_state["auth"]["port"]
    DBNAME = st.session_state["auth"]["database"]
    TABLE = st.session_state["auth"]["table"]
if model is not None:
    st.session_state["model"] = json.load(model)

go = st.button(label="GET !")


def fetch_data() -> pd.DataFrame:
    C = DBConn(USER, PASSWORD, DBNAME,HOST, PORT)
    cols = ', '.join([f'"{col}"' for col in st.session_state["model"]["Columns"]])
    query = f"SELECT {cols} FROM {TABLE} "
    with C.connect_postgres() as conn:
        cur = conn.cursor()
        cur.execute(query)
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
            data['Random'] = np.random.uniform(0,1,len(data))
            # Initialization
            if 'data' not in st.session_state:
                st.session_state['data'] = data[data['Random'] <= 0.8]
                st.session_state['test'] = data[data['Random'] > 0.8]
                st.session_state['data'].drop(['Random'], axis=1, inplace=True)
                st.session_state['test'].drop(['Random'], axis=1, inplace=True)
                st.dataframe(st.session_state['data'].head())
                st.success("Data found")

        except Exception as e:
            st.error(e)
    else:
        st.error("Oracle and Snowflake database are not connected yet :pensive:")


if 'data' not in st.session_state:
    st.warning("No data found")



