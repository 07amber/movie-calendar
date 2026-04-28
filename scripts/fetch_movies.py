import requests
import json
from datetime import datetime, timedelta

# 请将此处替换为您的 TMDB API Key
API_KEY = 'a024a2c52f349da4cbceee0c4b82f066'
# 设置地区：CN (中国内地), HK (香港)
REGIONS = ['CN', 'HK']

def fetch_movies():
    all_movies = []
    # 获取当前日期
    today = datetime.now()
    
    # 明确设置起始日期为本月1号
    start_date = today.strftime('%Y-%m-01')
    
    # 将日期向前推，直接设置到下下个月的最后一天，确保覆盖范围足够广
    # 这样可以一次性抓取约 60 天的数据（本月+下月）
    end_date = (today + timedelta(days=60)).strftime('%Y-%m-%d')

    for region in REGIONS:
        # 修改 URL 参数，让日期跨度覆盖下个月
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&region={region}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&sort_by=release_date.asc&language=zh-CN"
        
        response = requests.get(url).json()
        
        for movie in response.get('results', []):
            # 过滤掉日期为空的数据
            if movie.get('release_date'):
                all_movies.append({
                    "title": f"{movie['title']} ({region})",
                    "start": movie['release_date'],
                    "url": f"https://www.themoviedb.org/movie/{movie['id']}"
                })
    
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_movies()
