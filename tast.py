import requests
r = requests.get("https://api.deepseek.com", timeout=10)
print("状态码:", r.status_code)     # 200/404 都算通
