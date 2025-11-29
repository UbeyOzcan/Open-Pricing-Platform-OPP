import streamlit as st


if 'data' not in st.session_state:
    st.warning('No data found')
else:
    df  = st.session_state['data']

    st.write(f"This is the table of the {st.session_state['model']['Response']} Distribution and the related {st.session_state['model']['Offset']}")
    response_distribution = df.groupby(st.session_state['model']['Response']).agg({st.session_state['model']['Response'] : 'count',
                                                                                   st.session_state['model']['Offset'] : 'sum'})
    st.dataframe(response_distribution, width='content')

    metric = df[st.session_state['model']['Response']].sum()/df[st.session_state['model']['Offset']].sum()

    metric = round(metric * 100, 2) if st.session_state['model']['Model Name'] == "Frequency" else round(metric, 2)

    st.write(f"{st.session_state['model']['Model Name']} is {metric :.2f} { "%" if st.session_state['model']['Model Name'] == "Frequency" else "" } ")
