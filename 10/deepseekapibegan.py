from openai import OpenAI

# 关键：用 OpenAI SDK 但把 base_url 指向 DeepSeek
client = OpenAI(
    api_key="1",                    # ← 换成你的 Key
    base_url="https://api.deepseek.com",      # ← 换地址就换模型商
)

# 第一次对话：system + user
resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一位耐心的编程老师"},
        {"role": "user", "content": "用简单的话解释什么是递归"},
    ],
    temperature=0.7,
)

# 任务 3：打印回复
print("💬 回复:", resp.choices[0].message.content)
print("=" * 40)

# 任务 4：打印 usage（token 消耗）
print("输入 token:", resp.usage.prompt_tokens)
print("输出 token:", resp.usage.completion_tokens)
print("总 token:", resp.usage.total_tokens)
# DeepSeek 常见价格（输入 ¥0.5/M，输出 ¥2/M，实际以官网为准）
INPUT_PRICE = 0.5 / 1_000_000      # 每 token 输入价格
OUTPUT_PRICE = 2 / 1_000_000       # 每 token 输出价格

cost = (resp.usage.prompt_tokens * INPUT_PRICE +
        resp.usage.completion_tokens * OUTPUT_PRICE)
print(f"💰 本次调用费用: ¥{cost:.6f}")   # 通常显示 0.000几，这就是"几分钱"的真相
