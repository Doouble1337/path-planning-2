from math import *
import dijkstra


class PathOptimizer:

    def gen_graph(self, mask, speed, radius):
        cell_sz = 1
        height, width = [len(mask), len(mask[0])]
        cell_num = [height // cell_sz, width // cell_sz]
        table = []
        # инициализация граф-табличка
        for i in range(cell_num[0]):
                if mask[i][j] == 0:
                    table[i // cell_sz][j // cell_sz] = 1

        # связываем и называем вершины
        move_weight = cell_sz / speed
        turn_weight = (2 * pi * radius) / (2 * speed)
        weights = [move_weight, turn_weight]

        # нормирование весов
        for i in range (len(weights)):
            weights[i] = int(weights[i] * speed * 100)
        # создание графа; в формате h-w-s, где h обозначает строк w - столбец, а s - направление
        height, width = height // cell_sz, width // cell_sz
        nodes = []
        graph = dijkstra.Graph()
        # массив направлений; в конец массива записываем первое направление, для удобства обращения
        directions = [[1, 0, 1], [2, 1, 0], [3, 0, -1], [4, -1, 0], [1, 0, 1]]

        def edge(i, j, k):
            first = directions[k][0]
            second = directions[k + 1][0]
            graph.add_edge(str(i) + "-" + str(j) + "-" + str(first), str(i) + "-" + str(j) + "-" + str(second), weights[1])
            if height > i + directions[k][2] > -1 and width > j + directions[k][1] > -1:
                graph.add_edge(str(i) + "-" + str(j) + "-" + str(first), str(i + directions[k][2]) + "-" + str(j + directions[k][1]) + "-" + str(first), weights[1])

        for i in range(height):
            for j in range(width):
                for k in range(len(directions) - 1):
                    edge(i, j, k)