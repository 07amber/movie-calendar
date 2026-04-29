import requests
import json
from datetime import datetime, timedelta

API_KEY = 'a024a2c52f349da4cbceee0c4b82f066'
REGIONS = ['CN', 'HK']

def get_date_range():
    today = datetime.now()
    # 起始日期设为当月 1 号，确保抓取当月完整数据
    start_date = today.replace(day=1).strftime('%Y-%m-%d')
    # 截止日期：计算到下个月底
    next_month = (today.replace(day=28) + timedelta(days=4))
    last_day_of_next_month = (next_month.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    return start_date, last_day_of_next_month.strftime('%Y-%m-%d')

def fetch_movies():
    all_movies = []
    start_date, end_date = get_date_range()
    
    for region in REGIONS:
        # 增加页码循环，抓取前 3 页数据以保证数据量完整
        for page in range(1, 4):
            url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=zh-CN&region={region}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&sort_by=primary_release_date.asc&page={page}"
            
            try:
                response = requests.get(url, timeout=10).json()
                results = response.get('results', [])
                if not results: break # 如果没数据了直接跳出
                
                for movie in results:
                    all_movies.append({
                        "title": f"{movie.get('title')} ({region})",
                        "start": movie.get('release_date'),
                        "url": f"https://www.themoviedb.org/movie/{movie.get('id')}"
                    })
            except Exception as e:
                print(f"Error: {e}")
            
    # 去重并排序
    unique_movies = {m['title'] + m['start']: m for m in all_movies}.values()
    sorted_movies = sorted(unique_movies, key=lambda x: x['start'])
            
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(list(sorted_movies), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_movies()
