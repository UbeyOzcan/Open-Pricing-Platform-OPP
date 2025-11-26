import numpy as np
import streamlit as st
from src.Data import Analyzer
st.title("Large Loss, EVT and Claims Capping")


if 'data' not in st.session_state:
    st.warning('No data found')
else:
    data=st.session_state['data']
    A = Analyzer(df=data)
    fig = A.plot_density(x=A.df[A.df['ClaimAmount'] > 0]['ClaimAmount'])
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    params_gamma = A.fit_gamma()
    params_lg = A.fit_lognormal()
    st.write(params_gamma)
    st.write(params_lg)
    simulate_gamma = A.simulate_gamma(params=params_gamma)
    simulate_lg = A.simulate_lognormal(params=params_lg)
    fig2 = A.plot_density(x = np.exp(simulate_gamma))
    fig3 = A.plot_density(x = np.exp(simulate_lg))
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True, key='fig2')
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True, key='fig3')