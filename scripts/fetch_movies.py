import urllib.request
import json
import ssl

# 忽略 SSL 证书检查，防止网络错误
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'a024a2c52f349da4cbceee0c4b82f066' # 务必填入你的实际 Key

def fetch_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=zh-CN&region=CN&page=1"
    
    print(f"尝试访问 URL: {url.replace(API_KEY, 'HIDDEN')}")
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)
            print(f"抓取成功，共找到 {len(data.get('results', []))} 部电影")
            
            # 把结果写入 movies.json
            with open('movies.json', 'w', encoding='utf-8') as f:
                json.dump(data.get('results', []), f, ensure_ascii=False, indent=2)
                
    except Exception as e:
        print(f"【重大错误】抓取失败: {str(e)}")

if __name__ == "__main__":
    fetch_movies()
