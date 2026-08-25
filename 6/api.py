import requests

API_KEY = "1b086f85596c49239a23cb01d20b9e1e"
url = "https://me5egp6k2r.re.qweatherapi.com/v7/weather/now"
def get_weather(city_id):
    params = {"location": city_id, "key": API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    if data.get("code") != "200":
        print("查询失败:", data.get("code"))
        return
    now = data["now"]
    print(f"🌤 {now['text']}  温度 {now['temp']}℃  体感 {now['feelsLike']}℃")
    print(f"湿度 {now['humidity']}%  风向 {now['windDir']}  风力 {now['windScale']} 级")

get_weather("101010100")    # 北京
get_weather("101020100")    # 上海
get_weather("101280101")    # 广州         # ← 直接看服务器到底回了什么



