import pandas as pd
import streamlit as st
from src.Data import Analyzer
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


st.title("Modelling")
if 'data' not in st.session_state:
    st.warning('No data found')

else:
    st.sidebar.write(f"Model : {st.session_state['model']['Model Name']}")
    st.sidebar.write(f"Response : {st.session_state['model']['Response']}")
    st.sidebar.write(f"Offset : {st.session_state['model']['Offset']}")
    st.sidebar.write(f"Distribution : {st.session_state['model']['Distribution']}")
    st.sidebar.write("---")
    data=st.session_state['data']
    A = Analyzer(df=data)
    rfs = A.get_vars(y=st.session_state['model']['Response'], exposure=st.session_state['model']['Offset'])

    if "selected_df" not in st.session_state:
        mod_df = pd.DataFrame({"Variable": rfs,
                               "Included": np.repeat(False, len(rfs))})
    else:
        mod_df = st.session_state['selected_df']
    selected_df = st.data_editor(mod_df)
    selected = selected_df[selected_df["Included"] == True]
    ls_selected = list(selected['Variable'])

    if 'exp' not in st.session_state:
        if len(ls_selected) == 0 :
            expr_full = f"ClaimNb ~ 1"
            st.sidebar.write(expr_full)
        else:
            expr = ' + '.join(ls_selected)
            expr_full = f"ClaimNb ~ {expr}"
            st.sidebar.write(expr_full)
    else:
        expr_full = st.session_state['exp']
        del st.session_state['exp']

    if 'MODEL' not in st.session_state:
        FreqPoisson = smf.glm(formula=expr_full,
                                  data=data,
                                  offset=np.log(data['Exposure']),
                                  family=sm.families.Poisson(link=sm.families.links.Log())).fit()

    else:
        FreqPoisson = st.session_state['MODEL']
        del st.session_state['MODEL']

    df_params = pd.DataFrame(FreqPoisson.params).reset_index().rename(columns={'index':'Variable', 0 : 'Beta'})
    df_params_exp = pd.DataFrame(np.exp(FreqPoisson.params)).reset_index().rename(columns={'index': 'Variable', 0: 'Exp(Beta)'})
    df_pvalues = pd.DataFrame(round(FreqPoisson.pvalues, 4)).reset_index().rename(columns={'index':'Variable', 0 : 'P-Value'})
    df_summary = pd.merge(df_params, df_params_exp, on='Variable')
    df_summary = pd.merge(df_summary, df_pvalues, on='Variable')
    st.dataframe(df_summary)

    def do_save_session():
        st.session_state['selected_df'] = selected_df
        st.session_state['exp'] = expr_full


    st.sidebar.button("SAVE !", on_click=do_save_session)