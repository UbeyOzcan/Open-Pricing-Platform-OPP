import streamlit as st
from src.Data import Analyzer
import pandas as pd

st.title("Univariate Analysis")
if 'data' not in st.session_state:
    st.warning('No data found')

else:
    data=st.session_state['data']
    A = Analyzer(df=data)
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

        uni_df_calc.insert(loc=3, column='Relative Exposure', value=uni_df_calc[st.session_state['model']['Offset']]/uni_df_calc[st.session_state['model']['Offset']].sum())
        uni_df_calc.insert(loc=1, column=f'{rf}_fmt', value=uni_df_calc[rf])
        uni_df_calc_edited = st.data_editor(uni_df_calc, disabled=[0, 1, 3, 4, 5])

        do_create = st.button('Create')
        do_delete = st.button('Delete')
        if do_create:
            fmt_dict = uni_df_calc_edited.set_index(rf).to_dict()[f'{rf}_fmt']
            new_col_df = uni_df_calc_edited[[rf, f'{rf}_fmt']]
            st.session_state['data'] = pd.merge(st.session_state['data'], new_col_df, how='left')
        if do_delete:
            st.session_state['data'] = st.session_state['data'].drop(rf, axis=1)
        fig = A.plot_univariate(df=uni_df_calc,
                                x=rf,
                                model_name=st.session_state['model']['Model Name'],
                                exposure=st.session_state['model']['Offset'])
        st.plotly_chart(fig, theme="streamlit", width="stretch", selection_mode="box")

    except Exception as e:
        st.error(e)
