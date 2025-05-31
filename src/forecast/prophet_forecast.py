import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os
import sys
import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False
DATA_PATH = os.path.abspath('data/subway_clean.csv')
OUTPUT_DIR = os.path.abspath('output/forecast/')
os.makedirs(OUTPUT_DIR, exist_ok=True)

failed_list = []

def prepare_time_series(df: pd.DataFrame, station_name: str) -> pd.DataFrame:
    df['total'] = df['ride'] + df['getoff']
    station_df = df[df['station'] == station_name]

    ts = (
        station_df.groupby('date')['total']
        .sum()
        .reset_index()
        .rename(columns={'date': 'ds', 'total': 'y'})
        .sort_values('ds')
    )
    return ts

def run_forecast(station: str, period: int = 30):
    try:
        df = pd.read_csv(DATA_PATH, parse_dates=['date'])
        ts = prepare_time_series(df, station)

        if ts.empty or len(ts) < 60:
            print(f"[오류] '{station}' 데이터가 충분하지 않습니다.")
            # sys.exit(1)
            return
        
        model = Prophet()
        model.fit(ts)

        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)

        forecast_file = os.path.join(OUTPUT_DIR, f"forecast_{station}.csv")
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(forecast_file, index=False, encoding='utf-8')

        fig = model.plot(forecast)
        fig.suptitle(f"{station} 혼잡도 예측 (30일)", fontsize=14)
        plot_file = os.path.join(OUTPUT_DIR, f"forecast_{station}.png")
        fig.savefig(plot_file)
        plt.close(fig)
        print(f"[완료] 예측 결과 저장 → {forecast_file}, {plot_file}")
    except Exception as e:
        print(f"[실패] {station} → {e}")
        failed_list.append(station)

if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH)
    stations = df['station'].dropna().unique()

    results = []

    for name in stations:
        run_forecast(name)

    print("실패한 목록")
    for name in failed_list:
        print(f"- {name}")
    # target_station = '강남'
    # run_forecast(target_station)