from math import *
import dijkstra
import cv2
import numpy as np
import heapq


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

class Graph:

    def __init__(self):
        self.mask = None
        self.cell_size = None

    def gen_graph(self, mask, cell_sz, speed = 1, radius = 1):
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

        map = self.gen_map(path)
        return path, map

    def astar(self, start, end, allow_diagonal_movement=False):
        maze = self.mask
        """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param maze:
        :param start:
        :param end:
        :return:
        """

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Heapify the open_list and Add the start node
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = 2500#len(maze) * len(maze[0]) // 2

        # what squares do we search
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
        if allow_diagonal_movement:
            adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

        # Loop until you find the end
        while len(open_list) > 0:
            outer_iterations += 1

            if outer_iterations > max_iterations:
                # if we hit this point return the path such as it is
                # it will not contain the destination
                path = return_path(current_node)
                return path, self.gen_map(path, False)

                # Get the current node
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = return_path(current_node)
                return path, self.gen_map(path, False)

            # Generate children
            children = []

            for new_position in adjacent_squares:  # Adjacent squares
                outer_iterations += 1
                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                outer_iterations += 1
                # Child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in open_list if
                        child.position == open_node.position and child.g > open_node.g]) > 0:
                    continue

                # Add the child to the open list
                heapq.heappush(open_list, child)

        return None, None

    def gen_map(self, path, use_detalization = True):
        mask = self.mask
        cell_sz = self.cell_size
        if(not use_detalization):
            cell_sz = 1
        map = np.zeros([len(mask), len(mask[0]), 3], np.uint8)
        # print(map)
        for i in range(1, len(path)):
            A = [int(path[i - 1][1]) * cell_sz + cell_sz // 2, int(path[i - 1][0]) * cell_sz + cell_sz // 2]
            B = [int(path[i][1]) * cell_sz + cell_sz // 2, int(path[i][0]) * cell_sz + cell_sz // 2]
            # print(A, B)
            if A != B:
                cv2.line(map, A, B, (0, 255, 0), 1)
                #print(A, B)
        for i in range(len(mask)):
            for j in range(len(mask[i])):
                # print(22111)
                if (map[i][j] != [0, 255, 0]).any():
                    if mask[i][j] != 1:
                        map[i][j] = np.array([0, 0, 0])
                    else:
                        map[i][j] = np.array([255, 255, 255])
        return map