matrix = [[1, 2, 3], [4, 5, 6]]
transposed = [[row[i] for row in matrix] for i in range(3)]
# 结果: [[1, 4], [2, 5], [3, 6]]
print(transposed)