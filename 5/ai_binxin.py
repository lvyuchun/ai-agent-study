import asyncio
import time
import aiohttp
import requests
async def Pinch(session,url):
        try:
                async with session.get(url) as response:
                        return len(await response.text())
        except Exception as e:
                print(f"{url} 失败: {type(e).__name__}")
                return 0
async def cmprass(session,urls):
                lens = [Pinch(session,url) for url in urls]
                return await asyncio.gather(*lens) 
                
async def main():
        https = [f"https://www.qq.com/get?n={i}" for i in range(10)]
        TIME = time.time()    
        async with aiohttp.ClientSession() as session:
                get = await cmprass(session, https)
                print(get)
        end = time.time()-TIME
        print("aiohttp.request.get 耗时:",end)
        requestq = []
        TIME = time.time()
        for http in https:
                try:
                      tasst =  requests.get(http, timeout=10)
                      requestq.append(len(tasst))
                except Exception as e:
                        print(f"{http} 失败: {type(e).__name__}")
        end = time.time()-TIME
        print("requests.get 耗时:",end)
        PRINT = await asyncio.gather(*requestq)
asyncio.run(main())
   