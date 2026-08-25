import tiktoken

# ① 获取编码器（cl100k_base 是 GPT-4 / GPT-3.5 用的分词器）
enc = tiktoken.get_encoding("cl100k_base")

# ② 编码：文本 → token ID 列表
text = "Hello, world! 你好，世界！"
tokens = enc.encode(text)

print("原文:", text)
print("token ID 列表:", tokens)     # 每个数字代表一个 token
print("token 数量:", len(tokens))   # ← 这就是你要的数

# ③ 看每个 token 到底切成了啥（直观理解分词）
for t in tokens[:10]:
    print(t, "→", enc.decode_single_token_bytes(t))
