import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

DATA_PATH = os.path.abspath('data/subway_clean.csv')
PLOT_DIR = os.path.abspath('output/plots/')
os.makedirs(PLOT_DIR, exist_ok=True)

def plot_total_daily_trend(df: pd.DataFrame):
    df['total'] = df['ride'] + df['getoff']
    daily = df.groupby('date', as_index=False)['total'].sum()

    monthly = daily.copy()
    monthly['month'] = monthly['date'].dt.to_period('M').dt.to_timestamp()
    monthly_avg = monthly.groupby('month', as_index=False)['total'].mean()

    plt.figure(figsize=(16, 6))
    sns.lineplot(data=daily, x='date', y='total', label='Daily Total')
    sns.lineplot(data=monthly_avg, x='month', y='total', label='Monthly Avg', linestyle='--')

    plt.title('일별 총 승하차 인원 추이 (일간/월간)')
    plt.xlabel('날짜')
    plt.ylabel('총 승하차 인원')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'date_trend.png'))
    plt.close()

def plot_weekday_avg(df: pd.DataFrame):
    df['total'] = df['ride'] + df['getoff']

    weekday_map = {
        0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'
    }
    df['weekday_label'] = df['weekday'].map(weekday_map)

    weekly_avg = df.groupby('weekday_label')['total'].mean().reindex(['월', '화', '수', '목', '금', '토', '일'])

    plt.figure(figsize=(10, 6))
    sns.barplot(x=weekly_avg.index, y=weekly_avg.values, palette='viridis')
    plt.title('요일별 평균 승하차 인원')
    plt.ylabel('평균 승하차 인원')
    plt.xlabel('요일')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'weekday_avg.png'))
    plt.close()

def plot_linewise_daily_trend(df: pd.DataFrame):
    df['total'] = df['ride'] + df['getoff']
    by_line = df.groupby(['date', 'line'])['total'].sum().reset_index()

    plt.figure(figsize=(16, 8))
    sns.lineplot(data=by_line, x='date', y='total', hue='line', palette='tab10', lw=1.2)
    plt.title('호선별 일일 승하차 인원 추이')
    plt.xlabel('날짜')
    plt.ylabel('총 승하차 인원')
    plt.legend(title='호선', loc='upper right', bbox_to_anchor=(1.12, 1))
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'line_trend.png'))
    plt.close()

def plot_top10_stations(df: pd.DataFrame):
    df['total'] = df['ride'] + df['getoff']
    top10 = df.groupby('station')['total'].sum().nlargest(10).reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='total', y='station', data=top10, palette='magma')
    plt.title('혼잡역 Top 10 (전체 긱간)')
    plt.xlabel('총 승하차 인원')
    plt.ylabel('역명')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, 'top10_stations.png'))
    plt.close()

def run():
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    plot_total_daily_trend(df)
    plot_weekday_avg(df)
    plot_linewise_daily_trend(df)
    plot_top10_stations(df)
    print(f"[시각화 완료] 모든 그래픈는 {PLOT_DIR} 경로에 저장되었습니다.")

if __name__ == '__main__':
    run()