import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))

def estimate_cost(prompt, output_len=500):
    """估算调用费用（GPT-3.5-turbo 价格示意，实际价格以官方为准）"""
    input_tokens = count_tokens(prompt)
    input_cost = input_tokens / 1_000_000 * 0.5      # 输入 ¥0.5/百万token(约)
    output_cost = output_len / 1_000_000 * 1.5       # 输出 ¥1.5/百万token(约)
    return input_cost + output_cost

prompt = "请用中文写一篇关于人工智能的 500 字介绍。"
print("输入 token 数:", count_tokens(prompt))
print("估算费用: ¥", round(estimate_cost(prompt), 6))
