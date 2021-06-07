from math import *

def gen_graph(mask, speed, radius):
    cell_sz = 1
    height, width = [len(mask), len(mask[0])]
    cell_num = [height // cell_sz, width // cell_sz]
    table = []
    # инициализация граф-табличка
    for i in range (cell_num[0]):
            if mask[i][j] == 0:
                table[i // cell_sz][j // cell_sz] = 1

    # связываем и называем вершины
    move_weight = cell_sz / speed
    turn_weight = (pi * radius) / (4 * speed)
    weights = [move_weight, turn_weight]
    # нормирование весов
    weights *= speed
    for i in range (len(weights)):
