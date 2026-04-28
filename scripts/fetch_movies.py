import requests
import json
from datetime import datetime, timedelta

API_KEY = '你的_TMDB_API_KEY'
REGIONS = ['CN', 'HK']

def fetch_movies():
    all_movies = []
    today = datetime.now()
    
    # 扩大窗口：从今天开始，向后抓取 60 天（确保覆盖本月和下月）
    start_date = today.strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=60)).strftime('%Y-%m-%d')

    for region in REGIONS:
        # 强制指定 language=zh-CN，并使用 release_date 过滤
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&region={region}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&sort_by=release_date.asc&language=zh-CN"
        
        try:
            response = requests.get(url, timeout=10).json()
            for movie in response.get('results', []):
                # 再次确认标题和日期有效性
                title = movie.get('title', '未知影片')
                release_date = movie.get('release_date')
                
                if release_date:
                    all_movies.append({
                        "title": f"{title} ({region})",
                        "start": release_date,
                        "url": f"https://www.themoviedb.org/movie/{movie['id']}"
                    })
        except Exception as e:
            print(f"Error fetching {region}: {e}")
    
    # 排序：按日期从小到大
    all_movies.sort(key=lambda x: x['start'])
    
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_movies()
