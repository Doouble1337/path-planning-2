from math import *
import dijkstra
import cv2
import numpy as np


class Graph:

    def __init__(self):
        self.mask = None
        self.cell_size = None

    def gen_graph(self, mask, cell_sz, speed = 1, radius = 0.000001):
        self.mask = mask
        self.cell_size = cell_sz
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
                if mask[i][j] == 255:
                    table[i // cell_sz][j // cell_sz] = 1
        '''
        res = np.zeros((height, width, 3), np.uint8)
        for i in range(height):
            for j in range(width):
                if(table[i // cell_sz][j // cell_sz] == 1):
                    res[i][j] = (255, 255, 255)
        return res
        '''

        # связываем и называем вершины
        move_weight = cell_sz / speed
        alpha = pi / 2
        turn_weight = (alpha * radius) / (2 * speed)
        weights = [move_weight, turn_weight]
        #weights = [1, 0]

        # нормирование весов
        for i in range(len(weights)):
            weights[i] = int(weights[i] * speed * 100)
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
            graph.add_edge(str(y) + "-" + str(x) + "-" + str(first), str(y) + "-" + str(x) + "-" + str(second),
                           weights[1])
            graph.add_edge(str(y) + "-" + str(x) + "-" + str(second), str(y) + "-" + str(x) + "-" + str(first),
                           weights[1])
            if check(y, x, directions[k][1], directions[k][2]):
                graph.add_edge(str(y) + "-" + str(x) + "-" + str(first),
                               str(y + directions[k][1]) + "-" + str(x + directions[k][2]) + "-" + str(first),
                               weights[1])

        for i in range(height):
            for j in range(width):
                for k in range(len(directions) - 1):
                    if table[i][j] == 0:
                        edge(i, j, k)
        self.graph, self.nodes =  graph, nodes

        res = np.zeros((mask.shape[0], mask.shape[1], 3), np.uint8)
        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                if (table[i // cell_sz][j // cell_sz] == 1):
                    res[i][j] = (255, 255, 255)
        return res

    def search_path_dijkstra(self, start, finish):
        graph, nodes = self.graph, self.nodes
        if self.mask is None:
            return None, None
        mask = self.mask
        cell_sz = self.cell_size
        start_vertex = str(start[0] // cell_sz) + "-" + str(start[1] // cell_sz) + "-" + str(start[2])
        finish_vertex = str(finish[0] // cell_sz) + "-" + str(finish[1] // cell_sz) + "-" + str(finish[2])
        graph = dijkstra.DijkstraSPF(graph, start_vertex)
        path = graph.get_path(finish_vertex)
        for i in range(len(path)):
            path[i] = [path[i].split("-")[0], path[i].split("-")[1]]

        map = np.zeros([len(mask), len(mask[0]), 3], np.uint8)
        # print(map)
        for i in range(1, len(path)):
            A = [int(path[i - 1][0]) * cell_sz + cell_sz // 2, int(path[i - 1][1]) * cell_sz + cell_sz // 2]
            B = [int(path[i][0]) * cell_sz + cell_sz // 2, int(path[i][1]) * cell_sz + cell_sz // 2]
            # print(A, B)
            if A != B:
                cv2.line(map, A, B, (0, 255, 0), 1)
        for i in range(len(mask)):
            for j in range(len(mask[i])):
                # print(22111)
                if (map[i][j] != [0, 255, 0]).any():
                    if mask[i][j] != 1:
                        map[i][j] = np.array([0, 0, 0])
                    else:
                        map[i][j] = np.array([255, 255, 255])
        return path, map