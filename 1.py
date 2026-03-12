from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}
        self.visited = set()

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bft(self,V):
        for vertex in range(V):
            if vertex not in self.visited:
                self.bfs(vertex)

    def bfs(self, start):
        queue = deque()
        self.visited.add(start)
        queue.append(start)
        while queue:
            vertex = queue.popleft()
            print(vertex, end=" ")
            for neighbour in self.graph[vertex]:
                if neighbour not in self.visited:
                    self.visited.add(neighbour)
                    queue.append(neighbour)

# Example usage
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

print("Graph representation:")
print(graph.graph)
print("Breadth-first traversal:")
graph.bft(8)
