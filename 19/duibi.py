"""批量对比不同 prompt 版本的效果"""
import json
from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv("C:\\Users\\Asus\\ai-agent-study\\.env")   # 绝对路径,避免在不同目录下运行时找不到 .env 文件
api_key = os.getenv('API_KEY')
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

TEST_CASES = json.loads(
    Path("tests/articles.json").read_text(encoding="utf-8"))  # 测试文章集


def run_version(prompt_file: str) -> list[str]:
    template = Path(prompt_file).read_text(encoding="utf-8")
    outputs = []
    for article in TEST_CASES:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user",
                       "content": template.format(article=article)}],
            temperature=0)
        outputs.append(resp.choices[0].message.content)
    return outputs

# 用法:python prompt_test.py prompts/summarize/v2.md prompts/summarize/v3.md
# 把两版输出并排打出来,人工对比+记录,形成你的 prompt 评测习惯