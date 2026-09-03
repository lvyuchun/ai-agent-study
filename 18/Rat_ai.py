import collections
from openai import OpenAI

client = OpenAI(api_key="...", base_url="https://api.deepseek.com")

question = "一个班级 30 人,60% 是女生,女生比男生多几人?"

answers = []
for i in range(5):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user",
                   "content": question + "\n让我们一步步思考。"}],
        temperature=0.7)              # 随机性是「多路径」的前提
    answers.append(resp.choices[0].message.content)

# 统计最终数字分布
import re
finals = [re.search(r"(\d+)\s*人?$", a.strip()) for a in answers]
dist = collections.Counter(m.group(1) for m in finals if m)
print(dist)   # → Counter({"6": 4, "8": 1})  多数票:6

# 验算:30×0.6=18 女,12 男,差 6 人 ✓
# 单次采样可能撞上错误路径,5 次投票后错误被淹没