import streamlit as st
from src.DB import DBConn
import pandas as pd

st.title("Data Connector")

dbs = st.selectbox(
    "What type of database are you using?",
    ("Postgres", "Oracle", "Snowflake"),
    index=None,
    placeholder="Select database...",
)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    user = st.text_input(label="Username", value="postgres")
with col2:
    pwd = st.text_input(label = "Enter a password", value="postgres", type="password")
with col3:
    db = st.text_input(label="db name", value="frenchmtpldb")
with col4:
    table = st.text_input(label="tablename", value="frenchmtpl_table")
with col5:
    hostname = st.text_input(label="hostname", value="localhost")
with col6:
    port = st.text_input(label="port", value="2022")

go = st.button(label="GET !")

@st.cache_data
def fetch_data() -> pd.DataFrame:
    C = DBConn(user, pwd, db,hostname, port)

    with C.connect_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
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
            st.dataframe(data)
        except Exception as e:
            st.error(e)
    else:
        st.error("Oracle and Snowflake database are not connected yet :pensive:")



