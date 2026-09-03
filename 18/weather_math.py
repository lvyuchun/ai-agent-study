import re
from openai import OpenAI       # ① 换成这个
client = OpenAI(                # ② 创建客户端（这行之前缺失！）
    api_key="1",       #    换成你的 DeepSeek Key
    base_url="https://api.deepseek.com",
)
REACT_PROMPT = """你是一个会调用工具完成任务的智能助手。

可用工具（只有这两个，不要编造其他工具）：
- Calculator[表达式]：四则运算，如 Calculator[(15+3)*2]
- Weather[城市名]：查询城市当前天气，如 Weather[北京]

你必须严格按下面的格式输出，每轮只输出一次 Thought 和一次 Action：
Thought: 你此刻的推理
Action: 工具调用，格式为 工具名[参数]；若信息已足够，则输出 Finish[最终答案]

规则：
1. 每轮只能输出一个 Thought 和一个 Action，不要一次输出多步
2. 不要编造工具返回结果——工具真正返回什么，我会作为 Observation 发给你
3. 信息足够回答时就输出 Action: Finish[最终答案] 结束

用户问题：{question}"""

def calculator(expr: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        return "错误：表达式含有非法字符"
    try:
        return f"{expr} = {eval(expr)}"
    except Exception as e:
        return f"计算失败: {e}"

def weather(city: str) -> str:
    mock = {"北京": "晴 25℃", "上海": "多云 28℃", "广州": "雷阵雨 31℃"}
    return mock.get(city, f"暂不支持查询 {city}（演示版仅有北京/上海/广州）")

def parse_action(reply: str):
    """从模型回复提取 Action → (工具名, 参数)。
    健壮版：不依赖正则，不怕反斜杠丢失，全角/半角冒号都认。"""
    for line in reply.split("\n"):                # 逐行扫
        line = line.strip()
        if not line.startswith("Action"):         # 只认 Action 开头（大小写都行）
            continue
        rest = line[6:].lstrip(":： \t")          # 去掉 "Action" 和冒号/空白
        if "[" not in rest or not rest.endswith("]"):
            return None                           # 这一行格式不对就放弃
        name = rest[:rest.index("[")].strip()     # "[" 左边 = 工具名
        arg  = rest[rest.index("[") + 1:-1]       # "[" 和 末尾"]" 之间 = 参数
        return name, arg
    return None                                   # 整段都没 Action 行


def run_agent(question: str, max_steps: int = 6):
    messages = [{"role": "user", "content": REACT_PROMPT.format(question=question)}]

    for step in range(1, max_steps + 1):
        print(f"\n═══ 第 {step} 轮 ═══")
        reply = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0,
        ).choices[0].message.content
        print("🤖 模型:", reply)

        act = parse_action(reply)
        if act is None:
            print("⚠️ 没解析到 Action，结束"); return None
        name, arg = act

        if name == "Finish":
            print("✅ 最终答案:", arg); return arg

        tools = {"Calculator": calculator, "Weather": weather}
        obs = tools.get(name, lambda a: f"未知工具: {name}")(arg)
        print("🔧 工具返回:", obs)

        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Observation: {obs}\n请继续。"})

    print("⚠️ 达到最大步数，停止"); return None

# 测试
run_agent("北京天气怎么样？")
run_agent("(15+3)*2 等于多少？")



