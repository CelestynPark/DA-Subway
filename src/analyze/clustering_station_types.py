import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

DATA_PATH = os.path.abspath('data/subway_clean.csv')
SAVE_CSV_PATH = os.path.abspath('data/station_clusters.csv')
PLOT_PATH = os.path.abspath('output/plots/station_cluster_pca.png')
os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)

def cluster_stations(df: pd.DataFrame, n_cluster: int = 3) -> pd.DataFrame:
    df['total'] = df['ride'] + df['getoff']
    agg = df.groupby('station').agg({
        'total': ['mean', 'std']
    })
    agg.columns = ['avg_total', 'std_total']
    agg = agg.dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(agg)

    kmeans = KMeans(n_clusters=n_cluster, n_init=10, random_state=42)
    agg['cluster'] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    agg['pca1'] = X_pca[:, 0]
    agg['pca2'] = X_pca[:, 1]

    return agg.reset_index()

def plot_clusters(df_clustered: pd.DataFrame):
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        x='pca1', y='pca2',
        hue='cluster',
        data=df_clustered,
        palette='Set2',
        s=100
    )
    plt.title('지하철 역 유형 클러스터 (PCA 2D)')
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.legend(title='클러스터')
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    plt.close()

def run():
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    result = cluster_stations(df, n_cluster=3)
    result.to_csv(SAVE_CSV_PATH, index=False, encoding='utf-8')
    plot_clusters(result)
    print(f'[완료] 군집 분석 CSV 저장 → {SAVE_CSV_PATH}')
    print(f'[완료] 시각화 저장 → {PLOT_PATH}')

if __name__ == '__main__':
    run()