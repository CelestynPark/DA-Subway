import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
API_KEY = os.getenv("SEOUL_OPEN_API_KEY")
assert API_KEY, "환경 변수에 SEOUL_OPEN_KEY가 없습니다."

BASE_URL = "http://openapi.seoul.go.kr:8088"

def build_url(use_ymd: str, start_idx: int, end_idx: int, route:  str = "", station: str = "", data_type: str = "json") -> str:
    encoded_route = quote(route)
    encoded_station = quote(station)
    url = f"{BASE_URL}/{API_KEY}/{data_type}/CardSubwayStatsNew/{start_idx}/{end_idx}/{use_ymd}/{encoded_route}/{encoded_station}"
    return url

def fetch_subway_data(use_ymd: str, start_idx: int = 1, end_idx: int = 1000, route: str = "", station: str = "", data_type: str = "json") -> list[dict]:
    url = build_url(use_ymd, start_idx, end_idx, route, station, data_type)
    response = requests.get(url, timeout=10)
    
    if response.status_code != 200:
        raise RuntimeError(f"API 요청 실패: status_code={response.status_code}, url={url}")
    
    json_data = response.json()
    if "CardSubwayStatsNew" not in json_data:
        raise ValueError(f"예상 응답 구조와 다름: {json_data}")
    
    items = json_data["CardSubwayStatsNew"].get("row", [])
    return items

def get_all_dates(start_date: str, end_date: str) -> list[str]:
    s_date = datetime.strptime(start_date, "%Y-%m-%d")
    e_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = e_date - s_date

    return [(s_date + timedelta(days=i)).strftime("%Y%m%d") for i in range(delta.days + 1)]

def fetch_day_date(use_ymd: str, max_page: int = 50, chunk_size: int = 1000) -> pd.DataFrame:
    day_data = []
    for page in range(max_page):
        start = page * chunk_size + 1
        end = (page + 1) * chunk_size
        try:
            rows = fetch_subway_data(use_ymd, start, end)
            if not rows:
                break
            day_data.extend(rows)
        except Exception as e:
            print(f"[경고] {use_ymd} {start}-{end} 요청 실패: {e}")
            break
    
    return pd.DataFrame(day_data)

def fetch_all_data_parallel(start_date: str, end_date: str, output_path: str, max_workers: int = 8):
    date_list = get_all_dates(start_date, end_date)
    all_results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_day_date, date): date for date in date_list}
        for future in tqdm(as_completed(futures), total=len(futures), desc="수집 진행 중"):
            date = futures[future]
            try:
                df = future.result()
                if not df.empty:
                    all_results.append(df)
            except Exception as e:
                print(f"[오류] {date} 수집 실패: {e}")
        
    final_df = pd.concat(all_results, ignore_index=True)
    final_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[완료] {len(final_df)}개 행 저장됨 → {output_path}")

