from math import *
import dijkstra
import cv2
import numpy as np

mask = []
n, m = 100, 100
for i in range (n):
    mask.append([])
    for j in range(m):
        mask[i].append(0)
def gen_graph(mask, speed, radius):
    cell_sz = 1
    height, width = [len(mask), len(mask[0])]
    cell_num = [height // cell_sz, width // cell_sz]
    table = []
    for i in range(cell_num[0]):
        table.append([])
        for j in range(cell_num[1]):
            table[i].append(0)
    # инициализация граф-табличка
    for i in range(height):
        for j in range(width):
            if mask[i][j] == 1:
                table[i // cell_sz][j // cell_sz] = 1

    # связываем и называем вершины
    move_weight = cell_sz / speed
    alpha = pi / 2
    turn_weight = (alpha * radius) / (2 * speed)
    weights = [move_weight, turn_weight]

    # нормирование весов
    for i in range (len(weights)):
        weights[i] = int(weights[i] * speed * 100)
    weights = [1, 1]
    # создание графа; в формате h-w-s, где h обозначает строк w - столбец, а s - направление
    height, width = height // cell_sz, width // cell_sz
    nodes = []
    graph = dijkstra.Graph()
    # массив направлений; в конец массива записываем первое направление, для удобства обращения
    directions = [[1, -1, 0], [2, 0, 1], [3, 1, 0], [4, 0, -1], [1, -1, 0]]
    for i in range(height):
        for j in range(width):
            for k in range(len(directions) - 1):
                nodes.append(str(i) + "-" + str(j) + "-" + str(directions[k][0]))
    def check(y, x, dy, dx):
        if height > y + dy > -1 and width > x + dx > -1:
            # тут будет более умная проверка
            if table[y + dy][x + dx] == 0:
                return True
        return False

    def edge(y, x, k):
        first = directions[k][0]
        second = directions[k + 1][0]
        graph.add_edge(str(y) + "-" + str(x) + "-" + str(first), str(y) + "-" + str(x) + "-" + str(second), weights[1])
        graph.add_edge(str(y) + "-" + str(x) + "-" + str(second), str(y) + "-" + str(x) + "-" + str(first), weights[1])
        if check(y, x, directions[k][1], directions[k][2]):
            graph.add_edge(str(y) + "-" + str(x) + "-" + str(first), str(y + directions[k][1]) + "-" + str(x + directions[k][2]) + "-" + str(first), weights[1])

    for i in range(height):
        for j in range(width):
            for k in range(len(directions) - 1):
                edge(i, j, k)
    return graph, nodes
graph, nodes = gen_graph(mask, 1, 1)
graph = dijkstra.DijkstraSPF(graph, "1-0-1")
print("%-5s %-5s" % ("label", "distance"))
for u in nodes:
    print("%-5s %10.2f" % (u, graph.get_distance(u)))
print(" -> ".join(graph.get_path("1-9-3")))


for i in range (n):
    for j in range(m):
        mask[i][j] = 255 - mask[i][j]

mask = np.array(mask, np.uint8)
cv2.namedWindow ("frame", cv2.WINDOW_NORMAL)

cv2.resizeWindow ("frame", (960, 720))
cv2.rectangle(mask, (40, 40), (50, 50), (0, 255, 0), 1)
cv2.line(mask,(0, 0),(50, 50),(0,0,255),2)
cv2.imshow("frame", mask)
cv2.waitKey(0)
#time.sleep(0.01)
