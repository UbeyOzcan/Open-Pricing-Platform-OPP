import pandas as pd
import streamlit as st
from src.Data import Analyzer
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

st.sidebar.write(f"Model : {st.session_state['model']['Model Name']}")
st.sidebar.write(f"Response : {st.session_state['model']['Response']}")
st.sidebar.write(f"Offset : {st.session_state['model']['Offset']}")
st.sidebar.write(f"Distribution : {st.session_state['model']['Distribution']}")


st.title("Modelling")
if 'data' not in st.session_state:
    st.warning('No data found')

else:
    data=st.session_state['data']
    A = Analyzer(df=data)
    rfs = A.get_vars(y=st.session_state['model']['Response'], exposure=st.session_state['model']['Offset'])
    mod_df = pd.DataFrame({"Variable" : rfs,
                           "Included" : np.repeat(False, len(rfs))})
    selected = st.data_editor(mod_df, width="content", disabled=[0, 1])
    selected = selected[selected["Included"] == True]
    expr = "ClaimNb ~ 1"
    FreqPoisson = smf.glm(formula=expr,
                          data=data,
                          offset=np.log(data['Exposure']),
                          family=sm.families.Poisson(link=sm.families.links.log())).fit()
    st.write(np.exp(FreqPoisson.params[0]))
    st.write(FreqPoisson)
