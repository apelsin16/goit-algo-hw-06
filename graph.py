import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import random

# Створення графа
G = nx.Graph()

# Додавання вузлів (зупинок)
stops = ["Stop 1", "Stop 2", "Stop 3", "Stop 4", "Stop 5", 
         "Stop 6", "Stop 7", "Stop 8", "Stop 9", "Stop 10"]
G.add_nodes_from(stops)

# Додавання ребер (доріг або маршрутів)
routes = [("Stop 1", "Stop 2"), ("Stop 1", "Stop 3"), ("Stop 2", "Stop 4"),
          ("Stop 3", "Stop 5"), ("Stop 4", "Stop 5"), ("Stop 5", "Stop 6"),
          ("Stop 6", "Stop 7"), ("Stop 7", "Stop 8"), ("Stop 8", "Stop 9"),
          ("Stop 9", "Stop 10"), ("Stop 10", "Stop 1"), ("Stop 4", "Stop 6"),
          ("Stop 3", "Stop 7"), ("Stop 2", "Stop 8"), ("Stop 1", "Stop 9")]

for u, v in routes:
    G.add_edge(u, v, weight=random.randint(1, 10))

G.add_edges_from(routes)

# Візуалізація графа з вагами ребер
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Розташування вузлів
nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black', edge_color='gray')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title('Транспортна мережа міста з вагами ребер')
plt.show()

# Кількість вузлів і ребер
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

# Ступінь кожного вузла
degree_dict = dict(G.degree())

# Середній ступінь
avg_degree = sum(degree_dict.values()) / num_nodes

# Вивід результатів
print(f"Кількість вузлів: {num_nodes}")
print(f"Кількість ребер: {num_edges}")
print(f"Ступінь кожного вузла: {degree_dict}")
print(f"Середній ступінь вузла: {avg_degree:.2f}")

# DFS алгоритм
def dfs_path(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        return path
    for neighbor in graph.neighbors(start):
        if neighbor not in path:
            new_path = dfs_path(graph, neighbor, goal, path + [neighbor])
            if new_path:
                return new_path
    return None

# BFS алгоритм
def bfs_path(graph, start, goal):
    queue = deque([(start, [start])])
    while queue:
        (vertex, path) = queue.popleft()
        for neighbor in graph.neighbors(vertex):
            if neighbor not in path:
                if neighbor == goal:
                    return path + [neighbor]
                else:
                    queue.append((neighbor, path + [neighbor]))
    return None

# Знаходження шляхів
start_node = "Stop 1"
goal_node = "Stop 10"

dfs_result = dfs_path(G, start_node, goal_node)
bfs_result = bfs_path(G, start_node, goal_node)

print(f"DFS шлях від {start_node} до {goal_node}: {dfs_result}")
print(f"BFS шлях від {start_node} до {goal_node}: {bfs_result}")
"""
Пояснення результатів
DFS шлях може бути довшим та не оптимальним. Це пов'язано з тим, що алгоритм спершу йде вглиб, і може знайти шлях через вузли, які не обов'язково наближують до цілі.
BFS шлях буде найкоротшим в плані кількості кроків, оскільки алгоритм проходить всі можливі шляхи одного рівня, перш ніж рухатися далі.
Це пояснює різницю в отриманих шляхах для DFS та BFS.
"""

# Алгоритм Дейкстри для знаходження найкоротшого шляху
def dijkstra_shortest_path(graph, start, goal):
    return nx.dijkstra_path(graph, start, goal)

# Знаходження найкоротших шляхів між всіма вершинами
shortest_paths = {}
for start in stops:
    shortest_paths[start] = {}
    for goal in stops:
        if start != goal:
            shortest_paths[start][goal] = dijkstra_shortest_path(G, start, goal)

# Виведення результатів
for start in shortest_paths:
    for goal in shortest_paths[start]:
        print(f"Найкоротший шлях від {start} до {goal}: {shortest_paths[start][goal]} (вага шляху: {nx.dijkstra_path_length(G, start, goal)})")