import functools
import random
import time

def log_and_retry(times=3):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                start = time.perf_counter()          # ① 每次尝试单独计时
                try:
                    result = fun(*args, **kwargs)    # ② 记住返回值
                    elapsed = time.perf_counter() - start
                    print(f"{fun.__name__} executed in {elapsed:.4f} seconds")
                    return result                    # ③ 成功：立刻返回，退出循环！
                except Exception as e:
                    elapsed = time.perf_counter() - start
                    print(f"Attempt {attempt+1}/{times} failed: {e}")
                    if attempt == times - 1:         # ④ 最后一次失败
                        raise                        #    才把异常抛出去
                    time.sleep(attempt + 1)          # ⑤ 1, 2, 3 秒递增等待
        return wrapper
    return decorator

@log_and_retry()
def fun(x, y):
    if random.random() < 0.6:
        raise ConnectionError("网络抖动")
    return x + y            # ⑥ 返回计算结果

print(fun(3, 4))            # 成功时会打印耗时 + 7
