
from collections import Counter
from collections import namedtuple
from collections import defaultdict

dd = defaultdict(list)      # 默认值是空列表
dd["水果"].append("苹果")    # 不需要先判断键在不在！
dd["水果"].append("香蕉")
# defaultdict(list, {'水果': ['苹果', '香蕉']})

x=((x,y) for x in range(5) for y in range(5))
print(list(x))
k="aaaaavvvvvcccccsssss"
print(Counter(k))

point = namedtuple('Point', ['x', 'y', 'z'])
pp = point(1, 2, 3)
print(pp[0])
print(pp.x)