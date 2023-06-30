import numpy as np


class Node:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0

    def print_node(self):
        return str(self.pos) + ' f = ' + str("{:.4f}".format(self.f)) + ' g = ' + str("{:.4f}".format(self.g)) + ' h = ' + str("{:.4f}".format(self.h))


class Astar:
    def __init__(self, map, start, finish):
        self.map = map
        self.start = start
        self.finish = finish

    # get f value of a node along with g and h
    def get_h(self, node):
        # h = distance to the finish node with pythagorean theorem
        node.h = np.sqrt((node.pos[0] - self.finish.pos[0]) ** 2 + (node.pos[1] - self.finish.pos[1]) ** 2)

    # returns a list of nodes
    def get_neighbours(self, node):
        neighbours = []

        # get all 8 neighbours in 8 directions: up, down, left, right, and 4 diagonals
        for i in range(-1, 2):
            for j in range(-1, 2):
                # skip the current node
                if i == 0 and j == 0:
                    continue
                # get the neighbour's position from left to right, from top to bottom
                x = node.pos[0] + j
                y = node.pos[1] + i
                # skip the neighbour if it's out of the map
                if x < 0 or x >= len(self.map) or y < 0 or y >= len(self.map[0]):
                    continue
                # skip the neighbour if it's a wall
                if self.map[y][x] == 'Z':
                    continue
                # add the neighbour to the list with the current node as its parent
                neighbours.append(Node([x, y], node))
        return neighbours


def node_in_open(node_to_check, open_list):
    for node in open_list:
        if node_to_check.pos == node.pos:
            return True
    return False


def node_in_close(node_to_check, close):
    for node in close:
        if node_to_check.pos == node.pos:
            return True
    return False


def print_open_closed(open_list, closed_list, count):
    print(str(count) + '. iteration')

    open_output = []
    closed_output = []

    print('Open:')
    for node in open_list:
        open_output.append(node.print_node())

    for node in open_output:
        print(node)

    print('Closed:')
    for node in closed_list:
        closed_output.append(node.print_node())

    for node in closed_output:
        print(node)


def astar():
    # initializations
    # x coordinate is the column, y coordinate is the row, so if we want to get the value of a node, we use [y][x]
    map = [
        [9, 9, 9, 9, 9, 'Z', 9, 9, 9, 9],
        [7, 9, 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 9],
        [6, 9, 9, 9, 8, 'Z', 6, 2, 'Z', 9],
        [3, 3, 3, 3, 3, 'Z', 4, 5, 'Z', 9],
        [7, 9, 7, 4, 9, 3, 3, 3, 3, 3],
        [9, 8, 8, 2, 9, 'Z', 8, 8, 9, 9],
        [8, 7, 'Z', 'Z', 'Z', 'Z', 7, 5, 6, 6],
        [9, 7, 8, 7, 8, 'Z', 5, 7, 7, 7],
        [9, 8, 7, 7, 9, 'Z', 8, 8, 8, 8],
        [9, 9, 9, 9, 9, 'Z', 7, 6, 8, 8]
    ]

    # list of nodes we went through
    help_table = []

    start = Node([3, 5], None)
    finish = Node([7, 2], None)

    a_star = Astar(map, start, finish)

    open_list = []
    closed_list = []

    open_list.append(start)
    a_star.get_h(start)
    start.f = start.h
    current = start
    help_table.append(start.print_node())

    count = 0
    print_open_closed(open_list, closed_list, count)

    # main loop
    while True:
        # if the current node is the finish node, break the loop
        if current.pos == finish.pos:
            break
        # get the neighbours of the current node and add it to the open list
        neighbours = a_star.get_neighbours(current)
        for neighbour in neighbours:
            # add the neighbours to the open list and calculate their f values
            if not node_in_open(neighbour, open_list) and not node_in_close(neighbour, closed_list):
                a_star.get_h(neighbour)
                neighbour.g = current.g + a_star.map[neighbour.pos[1]][neighbour.pos[0]]
                neighbour.f = neighbour.g + neighbour.h
                open_list.append(neighbour)

        # remove the current node from the open list and add it to the closed list
        open_list.remove(current)
        closed_list.append(current)

        # if the open list is empty, break the loop
        if len(open_list) == 0:
            break

        # get the node with the lowest f value from the open list
        current = open_list[0]
        for node in open_list:
            # choose a node from the nodes with the lowest f value
            if node.f <= current.f:
                if node.f == current.f and node.h < current.h:
                    current = node
                elif node.f < current.f:
                    current = node

        # output the current node
        help_table.append(current.print_node())
        count += 1
        print_open_closed(open_list, closed_list, count)

    # print the help table
    print('Help table: ')
    for node in help_table:
        print(node)

    path = []
    while current.parent is not None:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1]


if __name__ == '__main__':
    path = astar()

    # list of nodes in the path
    path_list = []
    for node in path:
        path_list.append(node.print_node())

    # print the path
    print('Path: ')
    for node in path_list:
        print(node)