import streamlit as st
from src.Statistics import Stat
from src.Data import Analyzer

if 'data' not in st.session_state:
    st.warning('No data found')
else:
    resp1 = st.session_state['resp_freq']
    resp2 = st.session_state['resp_sev']
    resp = [resp1,resp2]
    y = st.selectbox('Select Response Variable', resp)
    S = Stat(df=st.session_state['data'])
    dist = S.response_dist(y = y)
    st.dataframe(dist)

