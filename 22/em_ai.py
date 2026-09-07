from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv("C:\\Users\\Asus\\ai-agent-study\\.env")   # 绝对路径,避免在不同目录下运行时找不到 .env 文件
api_key = os.getenv('API_KEY_ZH')  # ← 这里换成你在智谱官网申请的 Key
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

resp = client.embeddings.create(
    model="embedding-3",
    input=["Python 是一门编程语言", "今晚吃火锅还是烧烤"],
)

vec = resp.data[0].embedding
print(type(vec).__name__)        # list             —— 就是普通浮点数列表
print(len(vec))                  # 2048             —— embedding-3 的维度
print(vec[:3])                   # [0.0121, -0.0334, 0.0087, ...]
print(resp.usage.prompt_tokens)  # 20               —— 输入按 token 计费

# 和聊天接口的两点不同:
# ① 没有 messages,只有 input(一次可以传一个列表,批量算)
# ② 没有 temperature 等参数——embedding 是确定性映射,同一文本永远得到同一向量
import numpy as np, itertools

progs = ["装饰器是什么", "GIL 是什么", "列表推导式怎么写", "虚拟环境 venv", "Git rebase 用法",
         "什么是递归", "字典和列表的区别", "HTTP 404 是什么", "正则表达式入门", "deepseek 怎么计费"]
foods = ["火锅底料选牛油还是清油", "红烧肉的糖色怎么炒", "煮溏心蛋要几分钟", "拿铁和卡布奇诺区别", "寿司醋和米饭的比例",
         "奶茶三分糖什么意思", "面包发酵的温度", "辣椒油怎么做才香", "披萨要不要加菠萝", "清蒸鲈鱼几分钟"]
texts = progs + foods
vecs = [client.embeddings.create(model="embedding-3", input=[t]).data[0].embedding for t in texts]

M = np.array(vecs)                                 # (20, 2048)
M = M / np.linalg.norm(M, axis=1, keepdims=True)   # 归一化后点积=余弦
S = M @ M.T                                        # (20, 20) 相似度矩阵

pairs = sorted(((S[i][j], i, j) for i, j in itertools.combinations(range(20), 2)), reverse=True)
print("最像的 5 对:", [(round(s, 2), i, j) for s, i, j in pairs[:5]])
print("最不像的 5 对:", [(round(s, 2), i, j) for s, i, j in pairs[-5:]])

# 典型结果:最像的 5 对几乎全是编程内部或美食内部(0.55~0.8),
# 最不像的 5 对全是「编程 × 美食」跨主题(0.05~0.25)。
# 若不归一化,S[i][i] 不等于 1,读图容易误判——先归一化再点积是标准动作。
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

pts = TSNE(n_components=2, perplexity=5, random_state=42).fit_transform(M)
plt.scatter(pts[:10, 0], pts[:10, 1], c="tab:blue", label="编程")
plt.scatter(pts[10:, 0], pts[10:, 1], c="tab:orange", label="美食")
plt.legend()
plt.show()

# 观察点:
# ① 两团是否分离?重叠区是哪些句子(常是跨域词,如「deepseek 怎么计费」靠向钱的话题)
# ② 只看「抱团与否」,别读坐标距离——t-SNE 只保局部近邻,全局距离没有意义
# ③ perplexity(应远小于样本数 20)和 random_state 影响布局,固定才能复现
# ④ 20 个点噪声大,扩到 50+ 句图像会稳定得多