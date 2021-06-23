class undirectedGraph:
    def __init__(self, num_vertex):
        # Number of vertex
        self.num_vertex = num_vertex
        # Initialisation of adjacency lists
        self.adj = [[] for i in range(num_vertex)]

    # DFS algorithm
    def DFS_algorithm(self, temp, v, visited):
        visited[v] = True
        temp.append(v)
        for i in self.adj[v]:
            if not visited[i]:
                temp = self.DFS_algorithm(temp, i, visited)
        return temp

    # Method to add an edge to an undirected graph
    def add_edge(self, v1, v2):
        self.adj[v1].append(v2)
        self.adj[v2].append(v1)

    def find_connected_components(self):
        visited = []  # List of index that have been visited
        cc = []  # List of the connected components
        for i in range(self.num_vertex):
            visited.append(False)
        for v in range(self.num_vertex):
            if not visited[v]:
                temp = []
                cc.append(self.DFS_algorithm(temp, v, visited))
        return cc, len(cc)


my_graph = undirectedGraph(7)
my_graph.add_edge(1, 0)
my_graph.add_edge(2, 3)
my_graph.add_edge(3, 4)
my_graph.add_edge(5, 0)
my_graph.add_edge(2, 4)

connected_comp, nb_connected_comp = my_graph.find_connected_components()
print('The number of connected components are: {}'.format(nb_connected_comp))
