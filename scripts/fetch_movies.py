import requests
import json
from datetime import datetime, timedelta

# 请将此处替换为您的 TMDB API Key
API_KEY = 'a024a2c52f349da4cbceee0c4b82f066'
# 设置地区：CN (中国内地), HK (香港)
REGIONS = ['CN', 'HK']

def fetch_movies():
    all_movies = []
    # 获取当月和下个月的日期范围
    today = datetime.now()
    start_date = today.strftime('%Y-%m-01')
    # 简单计算下一个月的大概日期
    end_date = (today.replace(day=28) + timedelta(days=7)).replace(day=28).strftime('%Y-%m-28')

    for region in REGIONS:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&region={region}&release_date.gte={start_date}&release_date.lte={end_date}&sort_by=release_date.asc&language=zh-CN"
        response = requests.get(url).json()
        
        for movie in response.get('results', []):
            all_movies.append({
                "title": f"{movie['title']} ({region})",
                "start": movie['release_date'],
                "url": f"https://www.themoviedb.org/movie/{movie['id']}"
            })
    
    # 将获取的数据保存为 JSON 文件，供网页读取
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_movies()
