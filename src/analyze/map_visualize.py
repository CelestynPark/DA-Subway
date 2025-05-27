import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os
CLEAN_DATA_PATH = os.path.abspath('data/subway_clean.csv')
COORD_PATH = os.path.abspath('data/station_coords.csv')
MAP_SAVE_PATH = os.path.abspath('output/maps/congestion_map.html')
os.makedirs(os.path.dirname(MAP_SAVE_PATH), exist_ok=True)

def load_data() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=['date'])
    coords = pd.read_csv(COORD_PATH)
    df['total'] = df['ride'] + df['getoff']

    total_by_station = df.groupby('station')['total'].sum().reset_index()
    merged = pd.merge(total_by_station, coords, on='station', how='inner')
    return merged

def generate_map(df: pd.DataFrame):
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11, tiles='CartoDB positron')
    marker_cluster = MarkerCluster().add_to(m)

    quantile = df['total'].quantile([0.25, 0.5, 0.75, 0.9])
    def color_scale(value):
        if value >= quantile[0.9]:
            return 'darkred'
        elif value >= quantile[0.75]:
            return 'orange'
        elif value >= quantile[0.5]:
            return 'lightblue'
        else:
            return 'gray'
        
    for _, row in df.iterrows():
        popup_text = f"{row['station']}<br>혼잡도: {int(row['total']):,}명"
        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=6,
            popup=popup_text,
            tooltip=row['station'],
            color=color_scale(row['total']),
            fill=True,
            fill_opacity=0.7
        ).add_to(marker_cluster)
    
    m.save(MAP_SAVE_PATH)
    print(f"[완료] 혼잡도 지도 저장: {MAP_SAVE_PATH}")

def run():
    merged = load_data()
    generate_map(merged)

if __name__ == '__main__':
    run()