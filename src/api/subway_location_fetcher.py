import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
KAKAO_KEY = os.getenv('KAKAO_API_KEY')

if not KAKAO_KEY:
    raise ValueError('KAKAO_API_KEY가 .env 파일에 정의되어 있지 않습니다.')

HEADERS = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

CLUSTER_PATH = os.path.abspath('data/station_clusters.csv')
OUTPUT_path = os.path.abspath('data/station_coords.csv')

def fetch_coords(query: str):
    params = {"query": f"{query}역"}
    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
        result = response.json()
        
        if response.status_code != 200 or not result['documents']:
            return None, None
        
        top = result['documents'][0]
        return float(top['y']), float(top['x'])

    except Exception as e:
        print(f"[에러] {query}: {e}")
        return None, None
    
def run():
    df = pd.read_csv(CLUSTER_PATH)
    stations = df['station'].dropna().unique()

    results = []

    for name in stations:
        lat, lng = fetch_coords(name)
        if lat and lng:
            print(f"[성공] {name} → lat: {lat}, lng: {lng}")
            results.append({'station': name, 'lat': lat, 'lng': lng})
        else:
            print(f"[실패] {name} → 좌표 없음")
        time.sleep(0.2)
    
    coord_df = pd.DataFrame(results)
    coord_df.to_csv(OUTPUT_path, index=False, encoding='utf-8')
    print(f"[완료] {len(coord_df)}개 역 좌표 저장 → {OUTPUT_path}")

if __name__ == '__main__':
    run()