import numpy as np
from world import World
import pygame as pg
from time import sleep
from collections import deque

X = 640
Y = 640


# def get_matrix():
#     map_of = world.map
#     map_of = [[map_of[i][j] if map_of[i][j] != 0 and map_of[i][j] != 64 else 1 for i in range(world.size[0])] for j in
#               range(world.size[1])]
#     print(map_of)
#     matrix = []
#     for i in range(1, world.size[0] - 1):
#         for j in range(1, world.size[1] - 1):
#             matrix.append(((i, j), (i - 1, j, map_of[i - 1][j]), (i, j + 1, map_of[i][j + 1]),
#                            (i + 1, j, map_of[i + 1][j]), (i, j - 1, map_of[i][j - 1])))
#     return matrix
#
#
# def get_next_nodes(x, y):
#     check_next_node = lambda x, y: True if 0 <= x < world.size[1] and 0 <= y < world.size[0] and not get_matrix()[y][
#         x] else False
#     ways = [-1, 0], [0, -1], [1, 0], [0, 1]
#     return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]
#
#
# def Dijkstra(matrix):
#     graph = matrix
#
#     def bfs(start, goal, graph):
#         queue = deque([start])
#         visited = {start: None}
#
#         while queue:
#             cur_node = queue.popleft()
#             if cur_node == goal:
#                 break
#
#             next_nodes = graph[cur_node]
#             for next_node in next_nodes:
#                 if next_node not in visited:
#                     queue.append(next_node)
#                     visited[next_node] = cur_node
#         return visited
#
#     start = pos
#     goal = search(pos)
#     visited = bfs(start, goal, graph)
#
#     cur_node = goal
#     print(f'\npath from {goal} to {start}: \n {goal} ', end='')
#     while cur_node != start:
#         cur_node = visited[cur_node]
#         print(f'---> {cur_node} ', end='')


def search(pos):
    dusts = []
    for i in range(world.size[0]):
        for j in range(world.size[1]):
            if world.map[i][j] == 1:
                dusts.append((i, j))
    distances = [np.abs(pos[0] - dust[0]) + np.abs(pos[1] - dust[1]) for dust in dusts]
    if len(distances) != 0:
        min_distance = min(distances)
        min_index = distances.index(min_distance)
        return dusts[min_index]
    else:
        return None


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((640, 640))
    pg.display.set_caption('Cleaner')
    clock = pg.time.Clock()
    world = World(0.5)
    pos = world.cleaner.pos
    dust = search(pos)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        colors = np.array(world.get_colors())
        surface = pg.surfarray.make_surface(colors)
        surface = pg.transform.scale(surface, (X, Y))
        screen.blit(surface, (0, 0))
        pg.display.flip()

        pos = world.cleaner.pos
        dust = search(pos)
        if dust is None and world.count_of_dusts() == 0:
            print("END")
            green = (0, 255, 0)
            blue = (0, 0, 128)
            font = pg.font.Font('freesansbold.ttf', 32)
            text = font.render('Count of steps = {0}/{1}'
                               .format(world.count_of_steps, (world.size[0] - 2) * (world.size[1] - 2)), True, green,
                               blue)
            textRect = text.get_rect()
            textRect.center = (X // 2, Y // 2)
            screen.blit(text, textRect)
            pg.display.update()
            sleep(3)
            pg.quit()
            break
        if pos[0] > dust[0]:
            world.move("LEFT")
        elif pos[0] < dust[0]:
            world.move("RIGHT")
        elif pos[1] > dust[1]:
            world.move("UP")
        elif pos[1] < dust[1]:
            world.move("DOWN")
        print("pos", pos)
        print("dust", dust)
        clock.tick(200)
