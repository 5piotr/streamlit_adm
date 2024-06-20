import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

conn = st.connection('apt_db')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# getting data
query_apt = f'''
            select *
            from apt_estymations
            order by date desc
            '''
df_apt = conn.query(query_apt, index_col='id')

query_rps = f'''
            select *
            from rps_usage
            order by date desc
            '''

df_rps = conn.query(query_rps, index_col='id')

st.header('piotrpietka.pl usage data', divider='red')
st.subheader('apartment price estimator')
st.markdown('last 10 estimations')

# apt table
st.write(df_apt.iloc[:10,:])

# price of sqm map
px.set_mapbox_access_token(st.secrets.mapbox.token)
fig = px.scatter_mapbox(df_apt,
                        lat='lat',
                        lon='lng',
                        zoom=5.4,
                        color='xgb_price_m2',
                        size_max=20,
                        opacity=1,
                        color_continuous_scale=px.colors.sequential.Jet,
                        height=800,
                        title='Prices of sq m')
fig.update_layout(mapbox_style='light')
st.plotly_chart(fig, theme='streamlit', use_container_width=True)

# date map
px.set_mapbox_access_token(st.secrets.mapbox.token)
fig = px.scatter_mapbox(df_apt,
                        lat='lat',
                        lon='lng',
                        zoom=5.4,
                        color='date',
                        size_max=20,
                        opacity=1,
                        color_continuous_scale=px.colors.sequential.Jet,
                        height=800,
                        title='Estimation dates')
fig.update_layout(mapbox_style='light')
st.plotly_chart(fig, theme='streamlit', use_container_width=True)

st.subheader('simple gesture recognition')
st.markdown('last 10 estimations')

# rps table
st.write(df_rps)
