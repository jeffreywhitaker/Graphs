from graph import Graph

def make_graph(ancestors):
    # make graph as dictionary
    graph = Graph()
    # input data is nodes of parent / child
    for node in ancestors:
        # if parent not in graph
        if node[0] not in graph.vertices:
            # add parent
            graph.add_vertex(node[0])
        # if child not in graph
        if node[1] not in graph.vertices:
            # add child
            graph.add_vertex(node[1])
        # add child / parent relationship
        graph.add_edge(node[1], node[0])
    return graph

def earliest_ancestor(ancestors, starting_node):
    # input data to graph
    graph = make_graph(ancestors)
    # make paths variable and lengths variable
    paths = []
    lengths = []

    # for each person in graph
    for person in graph.vertices:
        # find path to them from starting person
        path = graph.dfs(starting_node, person)
        # remove null links
        if path is not None:
            paths.append(path)

    # make list of lengths for each path
    for path in paths:
        lengths.append(len(path))

    # return traversal with longest path
    for path in paths:
        # if one of possibly many equal longest lengths
        if len(path) is max(lengths):
            # if longest length is self, return -1
            if path[-1] is starting_node:
                return(-1)
            # otherwise ...
            else:
                # make a list of possible options
                possible = []
                possible.append(path[-1])
                # return lowest ID route
                return min(possible)