import numpy as np
import random


class Piece:
    shapes = {
        "O": [[4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5]],
        "I": [[4, 14, 24, 34], [3, 4, 5, 6], [4, 14, 24, 34], [3, 4, 5, 6]],
        "S": [[5, 4, 14, 13], [4, 14, 15, 25], [5, 4, 14, 13], [4, 14, 15, 25]],
        "Z": [[4, 5, 15, 16], [5, 15, 14, 24], [4, 5, 15, 16], [5, 15, 14, 24]],
        "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
        "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
        "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
    }

    def __init__(self, letter: str, board_width=10, board_height=20):
        self.letter = letter
        self.shape_index = 0
        self.shapes_of_piece = Piece.shapes[letter]
        self.current_state = Piece.shapes[letter][0].copy()
        self.board_width = board_width
        self.board_height = board_height

    def get_current_state(self):
        return self.current_state.copy()

    def update_shape_index(self):
        self.shape_index = self.next_shape_index()

    def next_shape_index(self):
        if self.shape_index + 1 == len(self.shapes_of_piece):
            return 0
        else:
            return self.shape_index + 1

    def rotate(self):
        if self.at_down():
            return
        s1 = np.array(self.shapes_of_piece[self.shape_index])
        s2 = np.array(self.shapes_of_piece[self.next_shape_index()])
        dif = np.subtract(s2, s1)
        result = np.add(np.array(self.current_state), dif)
        result = result + self.board_width  # move pieces down by one row
        self.current_state = list(result)
        self.update_shape_index()

    def move_right(self):
        if self.emtpy_piece():
            return
        for index, value in enumerate(self.current_state):
            self.current_state[index] = value + self.board_width
        if self.at_right_border():
            return
        for index, value in enumerate(self.current_state):
            if (value + 1) % self.board_width == 0:
                self.current_state[index] = int(
                    (((value + 1) / self.board_width) - 1) * self.board_width)
            else:
                self.current_state[index] = value + 1
        if self.at_down() or self.touches():
            self.update_board_state()

    def at_right_border(self):
        mod_of_width = [num % self.board_width for num in self.current_state]
        if (self.board_width - 1) in mod_of_width:
            return True
        else:
            return False

    def move_left(self):
        if self.emtpy_piece():
            return
        for index, value in enumerate(self.current_state):
            self.current_state[index] = value + self.board_width
        if self.at_left_border():
            return
        for index, value in enumerate(self.current_state):
            if value % self.board_width == 0:
                self.current_state[index] = value + self.board_width - 1
            else:
                self.current_state[index] = value - 1
        if self.at_down() or self.touches():
            self.update_board_state()

    def at_left_border(self):
        mod_of_width = [num % self.board_width for num in self.current_state]
        if 0 in mod_of_width:
            return True
        else:
            return False

    def move_down(self):
        if self.emtpy_piece():
            return
        for index, value in enumerate(self.current_state):
            self.current_state[index] = value + self.board_width
        if self.at_down() or self.touches():
            self.update_board_state()

    def at_down(self):
        min_value_down = (self.board_height - 1) * self.board_width
        max_value_down = max(self.current_state)
        if max_value_down >= min_value_down:
            return True
        else:
            return False

    def touches(self):
        one_down_positon = np.array(self.get_current_state()) + self.board_width
        return any(np.isin(board_state, one_down_positon))

    def update_board_state(self):
        global board_state
        board_state = np.append(board_state, np.array(self.get_current_state()))
        self.current_state = []

    def emtpy_piece(self):
        return not (self.current_state)


def firs_row_occupied():
    first_row = np.array(range(0, x - 1))
    if any(np.isin(board_state, first_row)):
        return True
    else:
        return False


shapes = {
    "O": [[4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5]],
    "I": [[4, 14, 24, 34], [3, 4, 5, 6], [4, 14, 24, 34], [3, 4, 5, 6]],
    "S": [[5, 4, 14, 13], [4, 14, 15, 25], [5, 4, 14, 13], [4, 14, 15, 25]],
    "Z": [[4, 5, 15, 16], [5, 15, 14, 24], [4, 5, 15, 16], [5, 15, 14, 24]],
    "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
    "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
    "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
}


def print_array(array, x1, y1):
    [print(" ".join(array[x: x + x1])) for x in range(0, x1 * y1, x1)]


def calc_position_down(shape: list, area_with: int):
    return [x + area_with for x in shape]


(x, y) = input().split(" ")
x = int(x)
y = int(y)

empty_array = list("-" * x * y)
# board_state = np.array([60, 61, 62, 63, 64, 65, 66, 67, 68, 69,70, 71, 72, 73, 74, 75, 76, 77, 78, 79], int)
board_state = np.array([], int)


def create_shape(shape_list):
    copy = empty_array.copy()
    for index in shape_list:
        copy[index] = "0"
    for index in board_state.tolist():
        copy[index] = "0"
    return copy


def print_shape(piece: Piece):
    created_shape = create_shape(piece.get_current_state())
    print_array(created_shape, x, y)
    print()


def break_score():
    global board_state
    for first_in_line in range(0, 10 * 20, 10):
        full_line = np.array(range(first_in_line, first_in_line + x))
        if all(np.isin(full_line, board_state)):
            board_state = np.setdiff1d(board_state, full_line)
            above = np.extract(board_state < first_in_line, board_state)
            above = above + x
            below = np.extract(board_state > first_in_line + x - 1, board_state)
            board_state = np.append(above, below)
            #return


print_array(empty_array, x, y)
print()
continue_game = True
piece = None


def create_new_piece():
    global piece
    char = input()
    print()
    return Piece(char, board_width=x, board_height=y)


while continue_game:
    command = input()
    if piece and piece.current_state == [] and firs_row_occupied():
        print_shape(piece)
        print("Game Over!")
        continue_game = False
        continue
    if command == "piece":
        piece = create_new_piece()
        print_shape(piece)
        if piece.touches():
            piece.update_board_state()
    elif command == "break":
        break_score()
        print_shape(piece)
    elif command == "rotate":
        piece.rotate()
        print_shape(piece)
    elif command == "left":
        piece.move_left()
        print_shape(piece)
    elif command == "right":
        piece.move_right()
        print_shape(piece)
    elif command == "down":
        piece.move_down()
        print_shape(piece)
    elif command == "exit":
        continue_game = False
