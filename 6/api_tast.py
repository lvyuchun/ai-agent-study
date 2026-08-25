import requests
API_KEY = "1b086f85596c49239a23cb01d20b9e1e"
Address = "https://me5egp6k2r.re.qweatherapi.com/v7/weather/now"
def get_Weather(code):
    params = {"location":code,"key":API_KEY}
    resp =requests.get(Address,params=params,timeout=10)
    data = resp.json()
    if data.get("code") != "200":
        print("查询失败:",data.get("code"))
        return
    now = data["now"]
    print(f"🌤 {now['text']}  温度 {now['temp']}℃  体感 {now['feelsLike']}℃")
    print(f"湿度 {now['humidity']}%  风向 {now['windDir']}  风力 {now['windScale']} 级")
get_Weather("101010100")  # 北京