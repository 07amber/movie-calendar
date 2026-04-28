import requests
import json
from datetime import datetime, timedelta

API_KEY = 'a024a2c52f349da4cbceee0c4b82f066'

def fetch_movies():
    all_movies = []
    today = datetime.now()
    # 抓取未来 90 天的数据，确保覆盖范围足够大
    start_date = today.strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=90)).strftime('%Y-%m-%d')

    # 我们直接使用 TMDB 的 "即将上映" 接口，它比 discover 接口更精准
    # language=zh-CN 确保返回中文
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=zh-CN&region=CN&page=1"
    
    try:
        response = requests.get(url, timeout=10).json()
        for movie in response.get('results', []):
            release_date = movie.get('release_date')
            if release_date:
                all_movies.append({
                    "title": movie.get('title', '未知') + " (CN)",
                    "start": release_date,
                    "url": f"https://www.themoviedb.org/movie/{movie['id']}"
                })
        
        # 顺便获取一下香港的（稍微改一下 region 参数）
        url_hk = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=zh-CN&region=HK&page=1"
        response_hk = requests.get(url_hk, timeout=10).json()
        for movie in response_hk.get('results', []):
            release_date = movie.get('release_date')
            if release_date:
                all_movies.append({
                    "title": movie.get('title', '未知') + " (HK)",
                    "start": release_date,
                    "url": f"https://www.themoviedb.org/movie/{movie['id']}"
                })
    except Exception as e:
        print(f"Error: {e}")

    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_movies()
