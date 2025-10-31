import streamlit as st

if 'data' not in st.session_state:
    st.warning('No data found')
else:
    data=st.session_state['data']
    st.dataframe(data)