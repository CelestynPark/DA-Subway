from subway_fetcher import fetch_all_data_parallel
import os

if __name__ == "__main__":
    SAVE_PATH = os.path.abspath("C:/Users/sbeep/Desktop/DataAnalysis/Projects/DA-subway/data/subway_raw.csv")
    fetch_all_data_parallel(
        start_date="2024-01-01",
        end_date="2025-05-19",
        output_path=SAVE_PATH,
        max_workers=6
    )