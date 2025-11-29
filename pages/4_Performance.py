import streamlit as st

st.sidebar.write(f"Model : {st.session_state['model']['Model Name']}")
st.sidebar.write(f"Response : {st.session_state['model']['Response']}")
st.sidebar.write(f"Offset : {st.session_state['model']['Offset']}")
st.sidebar.write(f"Distribution : {st.session_state['model']['Distribution']}")