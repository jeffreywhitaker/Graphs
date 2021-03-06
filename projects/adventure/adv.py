from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



def travel_the_map(player):

    # make helper functions
    def bfs(graph, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create a queue
        q = Queue()
        # Enqueue A PATH TO the starting vertex
        q.enqueue([(starting_vertex, None)])
        # Create a set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            vertex = path[-1][0]
            # Check if it's been visited
            # If it hasn't been visited...
            if vertex not in visited:
                # Mark it as visited
                visited.add(vertex)
                # CHECK IF IT'S THE TARGET
                if vertex == destination_vertex:
                    # IF SO, RETURN THE PATH
                    return path
                # Enqueue A PATH TO all it's neighbors
                for direction, room in graph[vertex].items():
                    # MAKE A COPY OF THE PATH
                    path_copy = path.copy()
                    # append neighbor
                    path_copy.append((room, direction))
                    # ENQUEUE THE COPY
                    q.enqueue(path_copy)


    # make set of visited rooms and graph
    visited = set()
    graph = dict()

    # establish pointers
    previous_room = None
    direction_arrived_from = None

    # define opposite rooms
    opp = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    while True:
        # until you hit a dead end
        while previous_room != player.current_room.id:
            print('curr room', player.current_room.id)
            visited.add(player.current_room.id)
            # get list of current exits
            exits = player.current_room.get_exits()
            # if not visited before
            if player.current_room.id not in graph:
                # add to graph
                graph[player.current_room.id] = dict()
                # add exits to graph
                for exit in exits:
                    graph[player.current_room.id][exit] = '?'
            
            # record the previous room into current room's entry
            if previous_room is not None:
                graph[player.current_room.id][opp[direction_arrived_from]] = previous_room.id
            # record current room into previous room's entry
            if previous_room is not None:
                graph[previous_room.id][direction_arrived_from] = player.current_room.id

            # do DFT
            # go in an unexplored direction
            for direction, room in graph[player.current_room.id].items():
                possible_exits = []
                if room == '?':
                    possible_exits.append(direction)
            if len(possible_exits) > 0:
                direction_we_are_going = possible_exits.pop()
                # update pointers
                previous_room = player.current_room
                direction_arrived_from = direction_we_are_going
                #add direction travelled to traversal list, and travel
                traversal_path.append(direction_we_are_going)

                player.travel(direction_we_are_going)
            else:
                break
            
        # do BFS to find route to nearest unexplored room
        travel_directions = bfs(graph, player.current_room.id, '?')

        # stop the loop if no unexplored area remains
        if travel_directions is None:
            break

        # remove first room which is redundant bc it is current room
        travel_directions.pop(0)
        # follow travel_directions
        for room, direction in travel_directions:
            print('curr room', player.current_room.id)
            
            #update pointers
            previous_room = player.current_room
            direction_arrived_from = direction

            # traverse the path and log it
            player.travel(direction)
            traversal_path.append(direction)


# Run the code
travel_the_map(player)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
