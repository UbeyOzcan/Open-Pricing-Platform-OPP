import streamlit as st
from src.Statistics import Stat
from src.Data import Analyzer

if 'data' not in st.session_state:
    st.warning('No data found')
else:
    st.warning('Under construction')

