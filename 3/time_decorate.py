import functools
import random
import time
def log(fun):
    @functools.wraps(fun)
    def wraper(*args,**kawrds):
        start = time.perf_counter()
        for attemp in range(3):
           try:
               fun(*args, **kawrds)
               elpase = time.perf_counter() - start
               print(f"{fun.__name__} executed in {elpase:.4f} seconds")
               return wraper
           except Exception as e:
               print(f"Attempt {attemp+1} failed: {e}")
               if attemp == 2:
                raise
               time.sleep(attemp+1) 
    return wraper
@log
def fun():
    if random.random() <0.6:
        raise ConnectionError("网络抖动")
fun() 
