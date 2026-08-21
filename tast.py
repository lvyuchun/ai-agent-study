import aiohttp
import brotli
from aiohttp.http_parser import HAS_BROTLI

print("aiohttp:", aiohttp.__version__)
print("brotli:", brotli.__version__)

# ① 验证 brotli 本身能不能解压（排除库坏掉的可能）
data = brotli.compress(b"hello world")
print("brotli 解压测试:", brotli.decompress(data))   # 应输出 b'hello world'

# ② 看 aiohttp 是否识别到了 brotli
print("aiohttp 支持 br:", HAS_BROTLI)
