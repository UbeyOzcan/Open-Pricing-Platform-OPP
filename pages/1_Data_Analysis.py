import streamlit as st
from src.Data import Analyzer



st.title("Data Analysis")
if 'data' not in st.session_state:
    st.warning('No data found')
else:
    col1, col2, col3, col4 = st.columns(4)
    data=st.session_state['data']
    cols = data.columns.tolist()
    with col1:
        st.session_state['resp_freq'] = st.selectbox('Select response for Frequency Model',cols)
    with col2:
        st.session_state['exp_freq'] = st.selectbox('Select exposure for Frequency Model',cols)
    with col3:
        st.session_state['resp_sev'] = st.selectbox('Select response for Severity Model',cols)
    with col4:
        st.session_state['exp_sev'] = st.selectbox('Select exposure for Severity Model',cols)
    A =Analyzer(df=data)
    try:
        Y = [st.session_state['resp_freq'], st.session_state['resp_sev']]
        E = [st.session_state['exp_freq'], st.session_state['exp_sev']]
        rfs = A.get_vars(y=Y, exposure=E)
        rf = st.selectbox('Select Variable',rfs)
        uni_df = A.univariate(x=rf, y = Y, exposure= E)
        uni_df_calc = A.calc_freq_sev(df=uni_df, y = Y, exposure = E)
        st.dataframe(uni_df_calc)
    except Exception as e:
        st.error(e)
