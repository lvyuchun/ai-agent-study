# summarize.py 的完整防御结构

import json
from pathlib import Path
import sys
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv("C:\\Users\\Asus\\ai-agent-study\\.env")   # 绝对路径,避免在不同目录下运行时找不到 .env 文件
api_key = os.getenv('API_KEY_ZH')  # ← 这里换成你在智谱官网申请的 Key
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")
def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    return parser.parse_args()
def run_summarize(text):
    # 这里是调用 API 的逻辑,可能会抛出异常
    # 模拟 API 调用
    if "error" in text:
        raise ValueError("模拟 API 错误")
    return {"summary": text[:50] + "..."}  # 简单返回前 50 个字符作为摘要
from pydantic import BaseModel, Field

class ArticleInfo(BaseModel):
    title: str = Field(description="文章标题")
    keywords: list[str] = Field(description="3-5个关键词")
    entities: list[str] = Field(description="提到的关键实体(人名/产品/公司)")
    sentiment: str = Field(description="整体情感:正面/负面/中性")
    key_numbers: list[str] = Field(description="文中出现的重要数字及含义")

PROMPT = """从文章中抽取结构化信息,严格输出 JSON,字段定义:
- title: 文章标题
- keywords: 3-5个关键词
- entities: 提到的关键实体(人名/产品/公司)
- sentiment: 整体情感,只能是 正面/负面/中性
- key_numbers: 文中出现的重要数字及含义,如 ["营收120亿:年度营收"]
未提到的字段输出空列表或空字符串,不要编造。

文章:{article}"""

# 抽取和摘要的本质区别:摘要是「压缩」,抽取是「定位+结构化」。
# 抽取的字段必须有明确定义和取值范围,否则模型自由发挥。
def summarize_long(text: str, chunk_size: int = 3000) -> str:
    chunks = split_text(text, chunk_size)          # 切块
    # Map:每块独立摘要(可并发,Day 5 的 asyncio 派上用场)
    partials = [summarize(
        f"总结以下片段,200 字内:\n{c}") for c in chunks]
    # Reduce:合并分摘要
    joined = "\n---\n".join(partials)
    return summarize(
        f"以下是文章各部分的摘要,请合并成一篇 300 字内的总摘要:\n{joined}")

# 注意:Reduce 输入也可能超长——分摘要的长度要控制
# (10 块 × 200 字 = 2000 字,安全)。
def main():
    args = parse_args()
    # ① 输入文件问题
    path = Path(args.input)
    if not path.exists():
        sys.exit(f"错误: 文件不存在 {path}")
    text = path.read_text(encoding="utf-8")   # ② 编码问题(gbk 文件会炸)
    if len(text) < 50:
        sys.exit("错误: 文件内容太短,无需摘要")
    try:
        result = run_summarize(text)          # ③ API 调用失败
    except Exception as e:
        sys.exit(f"API 调用失败: {e}")
    # ④ 输出问题
    if args.output:
        Path(args.output).write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8")
        print(f"已保存到 {args.output}")
    else:
        print(result["summary"])
    response = client.chat.completions.create(
    model="...",
    messages=[{"role": "user", "content": PROMPT.format(article=text)}],
    temperature=0.1
    )
    json_string = response.choices[0].message.content
# sys.exit(中文提示):用户看到的是人话,不是 Python traceback
