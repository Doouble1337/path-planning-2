import dijkstra
nodes = ["SS", "T", "A", "B", "C", "D", "E", "F", "G"]

graph = dijkstra.Graph()
graph.add_edge("SS", "A", 4)

graph.add_edge("SS", "B", 3)
graph.add_edge("SS", "D", 7)
graph.add_edge("A", "C", 1)
graph.add_edge("B", "SS", 3)
graph.add_edge("B", "D", 4)
graph.add_edge("C", "E", 1)
graph.add_edge("C", "D", 3)
graph.add_edge("D", "E", 1)
graph.add_edge("D", "T", 3)
graph.add_edge("D", "F", 5)
graph.add_edge("E", "G", 2)
graph.add_edge("G", "E", 2)
graph.add_edge("G", "T", 3)
graph.add_edge("T", "F", 5)

dijkstra = dijkstra.DijkstraSPF(graph, "SS")
print("%-5s %-5s" % ("label", "distance"))
for u in nodes:
    print("%-5s %8d" % (u, dijkstra.get_distance(u)))


