import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    load_clean_data,
    get_station_list,
    load_forecast,
    MAP_PATH
)

st.set_page_config(page_title='서울 지하철 혼잡도 분석', layout='wide')

st.title('서울 지하철 혼잡도 대시보드')

df = load_clean_data()
station_list = get_station_list(df)

station = st.selectbox('분석할 지하철 역을 선택하세요', station_list, index=station_list.index('강남'))

st.subheader(f'{station} - 일별 승하차 인원 추이')
station_df = df[df['station'] == station].groupby('date')['total'].sum().reset_index()
fig = px.line(station_df, x='date', y='total', labels={'total': '총 승하차 인원', 'date': '날짜'})
st.plotly_chart(fig, use_container_width=True)

st.subheader(f'{station} - 요일별 평균 승하차 인원')
df['weekday'] = df['date'].dt.weekday
weekday_avg = (
    df[df['station'] == station]
    .groupby('weekday')['total']
    .mean()
    .reindex(range(7))
    .reset_index()
)
weekday_avg['요일'] = ['월', '화', '수', '목', '금', '토', '일']
fig = px.bar(weekday_avg, x='요일', y='total', labels={'total': '평균 승하차 인원'})
st.plotly_chart(fig, use_container_width=True)

st.subheader('전체 혼잡역 Top 10')
top10 = df.groupby('station')['total'].sum().nlargest(10).reset_index()
st.dataframe(top10)

fig = px.bar(top10, x='total', y='station', orientation='h', labels={'total': '총 승하차 인원', 'station': '역명'})
st.plotly_chart(fig, use_container_width=True)

forecast_df = load_forecast(station)
if not forecast_df.empty:
    st.subheader(f'{station} 미래 혼잡도 예측 (30일)')
    fig = px.line(forecast_df, x='ds', y='yhat', labels={'ds': '날짜', 'yhat': '예측 승하차 인원'})

    fig.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper'], mode='lines', name='상한')

    fig.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower'], mode='lines', name='하한')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning('선택한 역에 대한 예측 데이터가 없습니다. 먼저 예측 분석을 실행하세요.')

st.subheader('혼잡도 지도 보기')
st.components.v1.html(open(MAP_PATH, 'r', encoding='utf-8').read(), height=600)