import streamlit as st
import plotly.express as px
import colorsys

st.set_page_config(page_title='admin panel', layout='wide')

st.cache_data.clear()

conn_apt = st.connection('apt_db')
conn_airflow = st.connection('airflow_db')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# getting data
query_perf = f'''
            select *
            from apt_log
            order by date desc
            '''
df_perf = conn_airflow.query(query_perf, index_col='id')

query_apt = f'''
            select *
            from apt_estymations
            order by date desc
            '''
df_apt = conn_apt.query(query_apt, index_col='id')

query_rps = f'''
            select *
            from rps_usage
            order by date desc
            '''
df_rps = conn_apt.query(query_rps, index_col='id')

st.header('piotrpietka.pl models performance & usage data', divider='red')
st.subheader('apartment price estimator')

st.markdown('model performance')

# performance table
st.write(df_perf)

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
                        hover_data='date',
                        size_max=20,
                        opacity=1,
                        color_continuous_scale=px.colors.sequential.Jet,
                        height=800,
                        title='Prices of sq m')
fig.update_layout(mapbox_style='light')
st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def get_n_hexcol(n=5):
    hsv_tuples = [(0.9, 1, x * 1.0 / n) for x in range(n-1, -1, -1)]
    hex_out = []
    for rgb in hsv_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

# date map
px.set_mapbox_access_token(st.secrets.mapbox.token)
fig = px.scatter_mapbox(df_apt,
                        lat='lat',
                        lon='lng',
                        zoom=5.4,
                        color='date',
                        hover_data='xgb_price_m2',
                        size_max=20,
                        opacity=1,
                        color_discrete_sequence=get_n_hexcol(df_apt.shape[0]),
                        height=800,
                        title='Estimation dates')
fig.update_layout(mapbox_style='light')
st.plotly_chart(fig, theme='streamlit', use_container_width=True)

st.subheader('simple gesture recognition')
st.markdown('last 10 estimations')

# rps table
st.write(df_rps)
