# 方案 1:f-string——简单场景够用
PROMPT = "用不超过{n}字总结下面的文章,重点保留数字:\n{article}"

def make_prompt(article: str, n: int = 100) -> str:
    return PROMPT.format(article=article, n=n)

# 方案 2:Jinja2——模板复杂时用(条件/循环/继承)
from jinja2 import Template

tpl = Template("""你是{{ role }}。任务:{{ task }}
{% if examples %}
参考示例:
{% for ex in examples %}- {{ ex }}
{% endfor %}
{% endif %}""")

print(tpl.render(role="编辑", task="改写标题",
                 examples=["原标题:xx → 新标题:yy"]))

# 选择建议:变量少于 3 个用 f-string;
# 需要按条件拼示例、拼 few-shot 列表时上 Jinja2