from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
class Extraction(BaseModel):
    title: str = Field(description="文章标题")
    keywords: list[str] = Field(min_length=3, max_length=5)
    sentiment: str

    @field_validator("sentiment")
    @classmethod
    def check_sentiment(cls, v: str) -> str:
        if v not in ("正面", "负面", "中性"):
            raise ValueError(f"sentiment 必须是 正面/负面/中性,收到: {v}")
        return v

# Field(description=...) 还有一层妙用:把字段描述写进 prompt,
# 告诉模型每个字段是什么意思——schema 即文档
client = OpenAI(api_key="...", base_url="https://api.deepseek.com")

class Summary(BaseModel):
    title: str
    keywords: list[str]
    summary: str

prompt = f"""分析以下文章,严格输出 JSON(不要其他文字):
{{"title": "标题", "keywords": ["关键词"], "summary": "100字内摘要"}}

文章:{article}"""

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
)
result = Summary.model_validate_json(
    resp.choices[0].message.content)
print(result.title, result.keywords)   # 类型正确的 Python 对象
def structured_chat(prompt: str, schema: type[BaseModel],
                    max_retries: int = 2) -> BaseModel:
    messages = [{"role": "user", "content": prompt}]
    for _ in range(max_retries + 1):
        resp = client.chat.completions.create(
            model="deepseek-chat", messages=messages, temperature=0)
        text = resp.choices[0].message.content
        try:
            return schema.model_validate_json(text)   # 成功:返回
        except ValidationError as e:
            messages.append({"role": "assistant", "content": text})
            messages.append({"role": "user", "content":
                f"你的输出不符合要求,错误:{e}\n"
                f"请修正后重新输出完整 JSON,不要其他文字。"})
    raise RuntimeError("多次重试后仍无法获得合法输出")

# 三层防线:temperature=0 稳定输出 → Pydantic 严格验证 →
# 失败把错误发回模型修正 → 还不行就明确抛错(绝不静默吞掉)