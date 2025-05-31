# 전국 지하철 혼잡도 분석 (DA-Subway)

전국 지하철 혼잡도를 일자, 요일, 노선, 역 단위로 분석하고 예측하며, 시각화된 정보를 대시보드로 제공하는 프로젝트이다.
실제 서울시 OpenAPI를 활용하고, Prophet을 기반으로 미래 추세까지 예측하며, 지도 기반 혼합도 분포도 함께 제공한다.

---

## 프로젝트 개요

- **분석 대상**: 전구 지하철 역별 일별 승차/하차 인원
- **주요 기능**:
  - 혼잡도 기초 분석 (날짜, 요일, 노선)
  - 혼잡역 Top 10 도출
  - 군집 분석을 통한 역 유형 분류
  - Prophet 기반 혼잡도 시계열 예측
  - Folium 기반 지도 시각화
  - Streamlit 대시보드 통합

---

## 폴더 구조

```bash
DA-Subway/
├── data/                # 수집 및 분석 데이터
│   ├── subway_raw.csv
│   ├── subway_clean.csv
│   ├── peak_per_station.csv
│   ├── station_clusters.csv
│   ├── station_coords.csv
├── output/              # 시각화 및 예측 결과
│   ├── forecast/
│   ├── maps/
│   │   └── congestion_map.html
│   ├── plots/
│   │   ├── date_trend.png
│   │   ├── weekday_avg.png
│   │   ├── line_trend.png
│   │   ├── top10_stations.png
│   │   └── station_cluster_pca.png
├── src/                # 파이썬 분석 스크립트
│   ├── api/
│   │   ├── run_fetch.py
│   │   ├── subway_fetcher.py
│   │   └── subway_location_fetcher.py
│   ├── preprocess/
│   │   └── clean_subway_data.py
│   ├── visualize/
│   │   └── basic_analysis.py
│   ├── analysis/
│   │   ├── clustering_station_types.py
│   │   ├── peak_station_analysis.py
│   │   └── map_visualize.py
│   ├── forecast/
│   │   └── prophet_forecast.py
├── streamlit_app/              # Streamlit 대시보드
│   ├── main.py
│   └── utils.py
├── .env                        # API 키 저장
├── environment.yml             # conda 환경 정의
├── requirements.txt            # pip 기반 환경 정의
├── Readme.md                   # 프로젝트 설명서
└── .gitignore
```

---

## 실행 환경

* Python 3.10 이상
* conda 환경 권장
* API 필요:

  * 서울시 OpenAPI (지하철 통계)
  * 카카오 Local REST API (역 위치 조회)

---

## 실행 순서

1. **conda 환경 구성**

```bash
conda env create -f environment.yml
conda activate subway-analysis
```

2. **API 키 설정** (`.env`)

```env
SEOUL_OPEN_API_KEY=발급받은_서울_API_키
KAKAO_API_KEY=발급받은_카카오_API_키
```

3. **데이터 수집 및 전처리**

```bash
python src/api/run_fetch.py
python src/preprocess/clean_subway_data.py
```

4. **기초 분석 및 시각화**

```bash
python src/visualize/basic_analysis.py
```

5. **심화 분석**

```bash
python src/analyze/peak_station_analysis.py
python src/analyze/clustering_station_types.py
python src/analyze/map_visualize.py
```

6. **역 좌표 수집**

```bash
python src/api/subway_location_fetcher.py
```

7. **Prophet 예측 실행**

```bash
python src/forecast/prophet_forecast.py
```

8. **Streamlit 대시보드 실행**

```bash
streamlit run streamlit_app/main.py
```

---

## 대시보드 기능

| 기능 | 설명 |
|-----|------|
| 역 선택 | 드롭다운으로 분석 대상 역 선택 |
| 일별 혼잡도 추이 | Line plot |
| 요일별 평균 비교 | Bar chart |
| 혼잡역 Top 10 | 표 + 시각화 |
| 예측 시계열 | Prophet 기반 예측 결과 |
| 지도 시각화 | Folium 혼잡도 분포 지도 연동 |

---

## 사용 기술

* **데이터 수집**: requests, 서울시 OpenAPI, 카카오 Local API
* **전처리/분석**: pandas, seaborn, plotly
* **예측**: Prophet (Facebook)
* **대시보드**: Streamlit
* **환경 관리**: conda, dotenv

---

## 정책적 활용 가능성

* 출퇴근 시간대 운행 최적화
* 혼잡한 역 중심의 안전 인력 배치
* 시간대별 이용 요금제 시뮬레이션
* 혼잡도 기반 실시간 알림 시스템 개발

---

## 기여 및 사용

이 프로젝트는 교육 및 실무 연습 목접에 적합하며, 공개된 데이터와 라이브러리를 기반으로 자유롭게 활용 가능하다.
단, 카카오 API의 상업적 이용은 별도 계약이 필요하므로 사용 시 주의가 필요하다.

---

## 문의

* 작성자: \[CelestynPark]
* 이메일: \[[sbeep2001@gmail.com](sbeep2001@gmail.com)]