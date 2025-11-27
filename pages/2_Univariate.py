import streamlit as st
from src.Data import Analyzer

st.title("Data Analysis")
if 'data' not in st.session_state:
    st.warning('No data found')

else:
    data=st.session_state['data']
    A =Analyzer(df=data)
    try:
        rfs = A.get_vars(y=st.session_state['model']['Response'], exposure=st.session_state['model']['Offset'])
        rf = st.selectbox('Select Variable',rfs)
        uni_df = A.univariate(x=rf,
                              y = st.session_state['model']['Response'],
                              exposure= st.session_state['model']['Offset'])

        uni_df_calc = A.calc_resp(df=uni_df,
                                  y = st.session_state['model']['Response'],
                                  exposure = st.session_state['model']['Offset'],
                                  model_name=st.session_state['model']['Model Name'])
        st.dataframe(uni_df_calc)

        fig = A.plot_univariate(df=uni_df_calc,
                                x=rf,
                                model_name=st.session_state['model']['Model Name'],
                                exposure=st.session_state['model']['Offset'])
        st.plotly_chart(fig, theme="streamlit", width="stretch", selection_mode="box")

    except Exception as e:
        st.error(e)
