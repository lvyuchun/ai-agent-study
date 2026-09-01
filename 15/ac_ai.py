import collections
import openai
client = openai.OpenAI(
    api_key="1",                    # ← 换成你的 Key
    base_url="https://api.deepseek.com",      # ← 换地址就换模型商
)
question = "23 * 45 等于多少？"
question_with_cot = question + "\n让我们一步步计算："

answers = []
for _ in range(5):
    r = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": question_with_cot}],
        temperature=0.7)               # 必须 >0,否则 5 次完全一样
    answers.append(r.choices[0].message.content)

counter = collections.Counter(answers)
print(counter)
  #→ Counter({"1545": 4, "1554": 1})   # 多数票取 1545,比单次采样可靠
