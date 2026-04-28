import requests
import json

API_KEY = '你的_TMDB_API_KEY'

def fetch_movies():
    all_movies = []
    # 访问“正在上映”接口，不加日期筛选，直接抓取当前热门
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=zh-CN&region=CN&page=1"
    
    try:
        response = requests.get(url).json()
        for movie in response.get('results', []):
            if movie.get('release_date'):
                all_movies.append({
                    "title": movie['title'],
                    "start": movie['release_date'],
                    "url": f"https://www.themoviedb.org/movie/{movie['id']}"
                })
    except Exception as e:
        print(f"Error: {e}")
    
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_movies()
