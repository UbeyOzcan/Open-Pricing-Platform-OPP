import pandas as pd
import streamlit as st
from src.Data import Analyzer
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import plotly.figure_factory as ff

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
    test = st.session_state['test']
    A = Analyzer(df=data)
    rfs = A.get_vars(y=st.session_state['model']['Response'], exposure=st.session_state['model']['Offset'])
    response = st.session_state['model']['Response']
    offset = st.session_state['model']['Offset']
    Null_Model = f'{response} ~ 1'

    if 'Null_Model' in st.session_state:

        null_model = smf.glm(formula=Null_Model,
                                  data=data,
                                  offset=np.log(data[offset]),
                                  family=sm.families.Poisson(link=sm.families.links.Log())).fit()

    if "selected_df" not in st.session_state:

        mod_df = pd.DataFrame({"Variable": rfs,
                               "Included": np.repeat(False, len(rfs))})

    else:
        mod_df = st.session_state['selected_df']
        rfs_current = list(mod_df['Variable'])
        c = [x for x in  rfs  if x not in rfs_current]
        add_rfs = pd.DataFrame({'Variable': c, 'Included': np.repeat(False, len(c))})
        mod_df = pd.concat([mod_df, add_rfs])

    selected_df = st.data_editor(mod_df)
    selected = selected_df[selected_df["Included"] == True]
    ls_selected = list(selected['Variable'])

    if 'exp' not in st.session_state:

        if len(ls_selected) == 0 :
            expr_full = Null_Model
            st.sidebar.write(expr_full)

        else:

            expr = ' + '.join(ls_selected)
            expr_full = f"{response} ~ {expr}"
            st.sidebar.write(expr_full)

    else:

        expr_full = st.session_state['exp']
        del st.session_state['exp']


    FreqPoisson = smf.glm(formula=expr_full,
                            data=data,
                            offset=np.log(data[offset]),
                            family=sm.families.Poisson(link=sm.families.links.Log())).fit()


    FreqPoisson_test = smf.glm(formula=expr_full,
                               data=test,
                                offset=np.log(test[offset]),
                                family=sm.families.Poisson(link=sm.families.links.Log())).fit()




    st.write(f"Deviance on Training set : {FreqPoisson.deviance}")
    st.write(f"Deviance Null on Training set : {FreqPoisson.null_deviance}")
    st.write(f"Deviance on Testing set : {FreqPoisson_test.deviance} ")
    st.write(f"Deviance Null  on Testing set : {FreqPoisson_test.null_deviance} ")
    deviance_residual = pd.DataFrame(FreqPoisson.resid_deviance)
    deviance_residual = deviance_residual[0].to_list()
    fitted_value = pd.DataFrame(FreqPoisson.fittedvalues)[0].to_list()
    df_params = pd.DataFrame(FreqPoisson.params).reset_index().rename(columns={'index':'Variable', 0 : 'Beta'})
    df_params_exp = pd.DataFrame(np.exp(FreqPoisson.params)).reset_index().rename(columns={'index': 'Variable', 0: 'Exp(Beta)'})
    df_pvalues = pd.DataFrame(round(FreqPoisson.pvalues, 4)).reset_index().rename(columns={'index':'Variable', 0 : 'P-Value'})
    std_coef = np.diag(FreqPoisson.cov_params())
    conf_int = FreqPoisson.conf_int().reset_index().rename(columns={'index' : 'Variable', 0:'LB 95 %', 1 : 'UB 95 %'})
    df_summary = pd.merge(df_params, df_params_exp, on='Variable')
    df_summary = pd.merge(df_summary, df_pvalues, on='Variable')
    df_summary['std'] = np.sqrt(std_coef)
    df_summary = pd.merge(df_summary, conf_int, on='Variable')
    st.dataframe(df_summary)
    st.write(FreqPoisson)
    def do_save_session():
        st.session_state['selected_df'] = selected_df
        st.session_state['exp'] = expr_full


    st.sidebar.button("SAVE !", on_click=do_save_session)