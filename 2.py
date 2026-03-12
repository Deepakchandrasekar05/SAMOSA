class Graph:
    visited = set()
    def __init__(self):
        self.graph = {}
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)
    def dft(self, V):
        for i in range(V):
            if i not in Graph.visited:
                self.dfs(i)
    def dfs(self, node):
        Graph.visited.add(node)
        print(node, end=" ")
        for neighbour in self.graph[node]:
            if neighbour not in Graph.visited:
                self.dfs(neighbour)
graph = Graph()
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 4)
graph.add_edge(2, 5)
graph.add_edge(2, 6)
graph.add_edge(3, 7)
graph.add_edge(4, 7)
graph.add_edge(5, 7)
graph.add_edge(6, 7)
print("Depth-first traversal:")
graph.dft(8)

