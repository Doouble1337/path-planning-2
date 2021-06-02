from sklearn.linear_model import LinearRegression

data = [[1, 2], [3, 4]]
print(data)
print(data[0])
print(data[0][1])

data1 = [[[1, 2], [3,4]], [[5, 6], [7, 8]]]
print(data1[0][1][1])

line = [[[]]]
line[0][0].append(1)
print(line)
lines = [[[1, 1], [2, 2]], [[100, 100]], [[3, 3], [4, 4]]]
lines[-1].append(lines[0])
print(*lines)