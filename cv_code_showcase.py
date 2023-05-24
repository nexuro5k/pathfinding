# Example dungeon generated list
class HallwayGenerator:
    hallway_marker = 1
    door_marker = 2
    dungeon = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 4, 4, 4, 0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 4, 4, 4, 0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0],
        [0, 0, 0, 0, 7, 7, 7, 0, 0, 6, 6, 6, 0, 0],
        [0, 0, 0, 0, 7, 7, 7, 0, 0, 6, 6, 6, 0, 0],
        [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    original_room_centers = [(3, 6), (7, 2), (10, 10), (10, 5), (5,11)]

    def generate_hallways(self):
        current_depth = 0
        room_centers = list(self.original_room_centers)
        start_room = room_centers[0]
        room_centers.pop(0)
        room_centers_count = len(room_centers)
        while current_depth < room_centers_count:
            entrance_door = True
            exit_door = True
            end_room = self.find_nearest_room(start_room, room_centers)
            self.generate_next_hallway(start_room, end_room, entrance_door, exit_door)
            start_room = end_room
            current_depth += 1
        print("Finished all hallways, exiting...")


    def generate_next_hallway(self, start, end, entrance_door, exit_door):
        possible_routes = []
        direct_neighbors = [neighbor for neighbor in self.get_neighbors(start[0], start[1], 1)[:4]]

        possible_routes_count = 0
        distance = 0
        previous_node_distance = 0

        next_row = 0
        next_column = 0

        # Direct neighbors and check out of range.
        for neighbor in direct_neighbors:
            row, col = neighbor
            try:
                range_check = self.dungeon[row][col]
                possible_routes.append(neighbor)
            except IndexError:
                continue
            # Connected hallway, continue with next room.
            if (row, col) == end:
                if self.dungeon[row][col] > self.door_marker and self.dungeon[start[0]][start[1]] < self.door_marker:
                    self.dungeon[start[0]][start[1]] = self.door_marker
                return True

        possible_routes_count = len(possible_routes)
        if possible_routes_count == 0:
            return True
        closest_node = start
        previous_node_distance = self.manhattan_distance(start[0], start[1], end[0], end[1])
        for j in range(possible_routes_count):
            row0, col0 = possible_routes[j]
            distance = self.manhattan_distance(row0, col0, end[0], end[1])
            if distance < previous_node_distance:
                closest_node = possible_routes[j]
                previous_node_distance = self.manhattan_distance(closest_node[0], closest_node[1], end[0], end[1])

        next_row = closest_node[0]
        next_column = closest_node[1]
        # Door mechanic
        # Next node is a hallway node
        if self.dungeon[next_row][next_column] < self.door_marker:
            if entrance_door:
                self.dungeon[next_row][next_column] = self.door_marker
                # Disable entrance door, enable exit door
                entrance_door = False
            else:
                # Entrance door is disabled, still on path to the next room
                self.dungeon[next_row][next_column] = self.hallway_marker
        # Next node is a room node, entrance door disabled and exit door enabled, we reached the end of the hallway
        if self.dungeon[next_row][next_column] > self.door_marker and not entrance_door and exit_door:
            self.dungeon[start[0]][start[1]] = self.door_marker
            return True
        self.generate_next_hallway((next_row, next_column), end, entrance_door, exit_door)

    # helper methods
    def find_nearest_room(self, start, room_centers):
        previous_distance = float("inf")
        closest_room = (0, 0)
        for room_center in room_centers:
            row, col = room_center
            distance = self.manhattan_distance(start[0], start[1], row, col)
            if distance < previous_distance:
                closest_room = room_center
                previous_distance = distance
        room_centers.remove(closest_room)
        return closest_room

    def manhattan_distance(self, x, y, end_x, end_y):
        return abs(x - end_x) + abs(y - end_y)
    # (11, 8)
    # (2, 5)

    def get_neighbors(self, row, column, size):
        cells = (
            (row - size, column),   # top
            (row + size, column),   # bot
            (row, column - size),   # left
            (row, column + size),   # right
            (row - size, column - size),    # topLeft
            (row - size, column + size),    # topRight
            (row + size, column - size),    # bottomLeft
            (row + size, column + size),    # bottomRight
        )
        return cells

    def print_dungeon_array(self):
        output = ""
        for row in self.dungeon:
            output += " ".join(f"{val}" for val in row) + "\n"
        print(output)

hallway_generator = HallwayGenerator()
hallway_generator.print_dungeon_array()
hallway_generator.generate_hallways()
hallway_generator.print_dungeon_array()