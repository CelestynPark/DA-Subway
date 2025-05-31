import pandas as pd
import os

DATA_PATH = os.path.abspath('../data/subway_clean.csv')
COORD_DATA = os.path.abspath('../data/station_coords.csv')
FORECAST_DIR = os.path.abspath('../output/forecast/')
MAP_PATH = os.path.abspath('../output/maps/congestion_map.html')

def load_clean_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    df['total'] = df['ride'] + df['getoff']
    return df

def get_station_list(df: pd.DataFrame):
    return sorted(df['station'].unique())

def load_forecast(station_name: str) -> pd.DataFrame:
    path = os.path.join(FORECAST_DIR, f"forecast_{station_name}.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path, parse_dates=['ds'])