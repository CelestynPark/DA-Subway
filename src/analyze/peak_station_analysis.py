import pandas as pd
import os

DATA_PATH = os.path.abspath('data/subway_clean.csv')
OUTPUT_PATH = os.path.abspath('data/peak_per_station.csv')

def find_peak_per_station(df: pd.DataFrame) -> pd.DataFrame:
    df ['total'] = df['ride'] + df['getoff']
    peak_rows = (
        df.sort_values(['station', 'total'], ascending=[True, False])
            .groupby('station')
            .first()
            .reset_index()
            [['station', 'line', 'date', 'total']]
    )
    return peak_rows

def run():
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    peak_df = find_peak_per_station(df)
    peak_df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    print(f'[완료] 각 역의 혼잡 피크 기록 저장 → {OUTPUT_PATH}')

if __name__ == '__main__':
    run()