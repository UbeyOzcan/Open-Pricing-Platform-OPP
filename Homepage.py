import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon=":streamlit:",
    layout="wide",
    initial_sidebar_state="expanded"
    #menu_items={
    #    'Get Help': 'https://www.extremelycoolapp.com/help',
    #    'Report a bug': "https://www.extremelycoolapp.com/bug",
    #    'About': "# This is a header. This is an *extremely* cool app!"
    #}
)

st.title("Homepage :streamlit:")
st.markdown("Welcome to OPP, Open Pricing Platform")

clear = st.button("Clear Cache", width="stretch")
if clear:
    for key in st.session_state.keys():
        del st.session_state[key]