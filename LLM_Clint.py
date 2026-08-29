import time
import openai

class LLMClient:
    def __init__(self, api_key, base_url, model="deepseek-chat", max_retries=3):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model                  # 当前模型（可切换）
        self.max_retries = max_retries      # 最大重试次数
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def switch_model(self, model_name):
        """运行时切换模型——改 self.model 即可，下次调用立即生效"""
        old = self.model
        self.model = model_name
        print(f"✅ 模型切换: {old} → {model_name}")
        return self.model

    def chat(self, messages, temperature=0.7, stream=False):
        """对话：带指数退避重试（最多 3 次，间隔 1s/2s/4s）"""
        for attempt in range(self.max_retries):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,       # ← 用的就是 self.model，切模型即时生效
                    messages=messages,
                    temperature=temperature,
                    stream=stream,
                )
                if stream:
                    return self._stream(resp)
                return resp.choices[0].message.content   # 成功：返回结果
            except Exception as e:
                wait = 2 ** attempt          # 指数退避：1, 2, 4 秒
                print(f"⚠️ 第 {attempt+1}/{self.max_retries} 次失败: {type(e).__name__}: {e}")
                if attempt == self.max_retries - 1:
                    raise                    # 最后一次失败：抛出，不再重试
                print(f"⏳ 等待 {wait} 秒后重试...")
                time.sleep(wait)
        return None                          # 实际不会到这

    def _stream(self, resp):
        """流式响应：逐段吐出（生成器）"""
        try:
            for chunk in resp:
                piece = chunk.choices[0].delta.content
                if piece:
                    yield piece
        except Exception as e:
            print(f"流式中断: {e}")
llm = LLMClient("1", "https://api.deepseek.com", "deepseek-chat")

# ① 模型切换
llm.switch_model("deepseek-reasoner")      # ✅ 模型切换: deepseek-chat → deepseek-reasoner
llm.switch_model("deepseek-chat")          # 切回来

# ② 普通对话（自动带重试）
text = llm.chat([{"role": "user", "content": "讲个笑话"}])
print(text)

# ③ 验证重试生效：故意传个不存在的模型
llm.switch_model("不存在的模型")
try:
    llm.chat([{"role": "user", "content": "你好"}])
except Exception as e:
    print("最终失败，异常已抛出:", type(e).__name__)
# 你会看到:
# ⚠️ 第 1/3 次失败: ... ⏳ 等待 1 秒后重试...
# ⚠️ 第 2/3 次失败: ... ⏳ 等待 2 秒后重试...
# ⚠️ 第 3/3 次失败: ... (抛出)
#上下文管理
class LLMClient:
    def __init__(self, api_key, base_url, model="deepseek-chat", max_retries=3):
        ...
        self.messages = []      # ★ 对话历史（上下文）存这里

    def add_message(self, role, content):
        """向历史追加一条消息"""
        self.messages.append({"role": role, "content": content})

    def set_system(self, content):
        """设定人设（每次对话开头调用一次）"""
        self.messages.insert(0, {"role": "system", "content": content})

    def chat(self, user_input, temperature=0.7):
        self.add_message("user", user_input)            # ① 追加你的话
        resp = self.client.chat.completions.create(     # ② 传完整历史
            model=self.model,
            messages=self.messages,                     # ← 整个列表
            temperature=temperature,
        )
        reply = resp.choices[0].message.content
        self.add_message("assistant", reply)            # ③ 把回答也存回去
        return reply

