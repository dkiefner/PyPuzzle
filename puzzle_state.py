# The puzzle
from itertools import chain


class PuzzleState(object):
    def __init__(self, state_array):
        self.state_array = state_array
        self.position_map = PuzzleState.get_position_map(state_array)

    def get_len(self):
        return len(self.state_array)

    def to_one_dimension(self):
        return list(chain.from_iterable(self.state_array))

    def get_position(self, tile):
        return self.position_map.get(tile, None)

    def get_tile(self, lookup_pos):
        for tile, pos in self.position_map.items():
            if pos == lookup_pos:
                return tile

    # format: {tile: column, row}
    @staticmethod
    def get_position_map(state_array):
        out = {}

        for y, row in enumerate(state_array):
            for x, tile in enumerate(row):
                out[tile] = x, y

        return out

    def get_possible_movements(self, tile):
        movements = []
        tile_pos = self.get_position(tile)
        puzzle_len = self.get_len()

        if tile_pos[0] - 1 >= 0:
            movements.append(Move(Move.LEFT))
        if tile_pos[0] + 1 < puzzle_len:
            movements.append(Move(Move.RIGHT))
        if tile_pos[1] - 1 >= 0:
            movements.append(Move(Move.UP))
        if tile_pos[1] + 1 < puzzle_len:
            movements.append(Move(Move.DOWN))

        return movements

    def move(self, moving_tile, move):
        old_pos = self.get_position(moving_tile)
        new_pos = (old_pos[0] + move.current_move[0], old_pos[1] + move.current_move[1])
        blocking_tile = self.get_tile(new_pos)

        self.state_array[new_pos[1]][new_pos[0]] = moving_tile
        self.state_array[old_pos[1]][old_pos[0]] = blocking_tile
        self.position_map[moving_tile] = new_pos
        self.position_map[blocking_tile] = old_pos

    def get_inversion_count(self):
        inversion_count = 0
        empty_tile_row = self.get_position(None)[1]
        one_dimen_array = self.to_one_dimension()

        # count successor tiles which are smaller than i
        for i in range(len(one_dimen_array)):
            for j in range(i + 1, len(one_dimen_array)):
                if one_dimen_array[j] is not None \
                        and one_dimen_array[i] is not None \
                        and one_dimen_array[j] < one_dimen_array[i]:
                    inversion_count += 1

        if empty_tile_row % 2 == 0:
            inversion_count += 1

        return inversion_count

    def pretty_print(self):
        out = "\n"
        for index, row in enumerate(self.state_array):
            out += " " * 2
            for tile in row:
                if len(str(tile)) == 1:
                    out += " "

                if tile is None:
                    out += " " * 2
                else:
                    out += str(tile)

                out += " " * 2

            if index < len(self.state_array) - 1:
                out += "\n" * 2
            else:
                out += "\n"

        print(out)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.state_array == other.state_array)


class Move:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, current_move):
        self.current_move = current_move