import pandas as pd
import os

RAW_PATH = os.path.abspath('data/subway_raw.csv')
SAVE_PATH = os.path.abspath('data/subway_clean.csv')

COLUMN_RENAME_MAP = {
    'USE_YMD': 'date',
    'SBWY_ROUT_LN_NM': 'line',
    'SBWY_STNS_NM': 'station',
    'GTON_TNOPE': 'ride',
    'GTOFF_TNOPE': 'getoff',
    'REG_YMD': 'registered_at'
}

def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str)

    expected = set(COLUMN_RENAME_MAP.keys())
    actual = set(df.columns)
    if not expected.issubset(actual):
        raise ValueError(f"컬럼 누락됨: {expected - actual}")
    
    df = df.rename(columns=COLUMN_RENAME_MAP)

    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors="coerce")
    df['registered_at'] = pd.to_datetime(df['registered_at'], format='%Y%m%d', errors='coerce')

    df['ride'] = pd.to_numeric(df['ride'], errors='coerce')
    df['getoff'] = pd.to_numeric(df['getoff'], errors='coerce')

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    initial_rows = len(df)

    df = df.dropna(subset=['date', 'line', 'station', 'ride', 'getoff'])

    df = df.drop_duplicates(subset=['date', 'line', 'station'])

    final_rows = len(df)
    print(f"[전처리] {initial_rows} → {final_rows} rows after cleaning")

    return df

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['weekday'] = df['date'].dt.weekday
    df['weekpart'] = df['weekday'].apply(lambda x: 'weekday' if x < 5 else 'weekend')
    return df

def run():
    df = load_raw_data(RAW_PATH)
    df = clean_data(df)
    df = add_derived_columns(df)
    df.to_csv(SAVE_PATH, index=False, encoding='utf-8')
    print(f"[저장 완료] 전처리된 데이터 → {SAVE_PATH}")

if __name__ == '__main__':
    run()