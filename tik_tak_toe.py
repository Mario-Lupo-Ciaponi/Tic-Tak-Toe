from time import sleep
from math import ceil

SIZE = 3  # The size of the board


class PositionOccupiedError(Exception):
    pass


class InvalidPositionError(Exception):
    pass


def selecting_signs(name):
    """
    It will ask for the first player's choice of sign.
    If he types something different then 'X' or 'O', it will ask again
    """
    while True:
        player_one_sign = input(f"{name}, would you like to play with 'X' or 'O': ").upper()

        if player_one_sign not in ("X", "O"):
            print("Wrong sign. Choose again!")
        else:
            break

    player_two_sign = "O" if player_one_sign == "X" else "X"  # If the first player's sign is 'X', then the second's is 'O'.

    return player_one_sign, player_two_sign


def game_setup():
    """
    Setting up the game. This process includes naming the players,
    calling a function for signs and returning two tuples with the name of the player and his/her sign.
    """
    player_one_name = input("Player 1, please, type your name: ")

    while True:
        player_two_name = input("Player 2, please, type your name: ")

        if player_two_name == player_one_name:
            print("The second player's name must be different from the fist player's name")
        else:
            break

    player_one_sign, player_two_sign = selecting_signs(player_one_name)

    return (player_one_name, player_one_sign), (player_two_name, player_two_sign)


def print_board(board):
    """
    Printing the board
    """
    for row in board:
        print(f"|  {'  |  '.join(row)}  |")


def parsing_into_int(command) -> int:
    """
    It parses the command into an integer number
    """
    return int(command)


def check_position(position):
    """
    Checks if the position is valid, otherwise it raises a custom exception
    """
    if 0 > position or position > 9:
        raise InvalidPositionError


def getting_indexes(position):
    """
    Gets the indexes
    """
    row = ceil(position / 3) - 1
    col = position % 3 - 1

    return row, col


def check_if_position_is_occupied(row, index, board):
    """
    Checks if the position is occupied , otherwise it raises a custom exception
    """
    if board[row][index] != " ":
        raise PositionOccupiedError


def check_if_command_is_valid(command, board):
    """
    Checks if the command is valid, by calling functions and if an exception is raised it will print a message
    """
    try:
        position = parsing_into_int(command)

        check_position(position)
        row, index = getting_indexes(position)

        check_if_position_is_occupied(row, index, board)
    except ValueError:
        print("The position must be an integer number!")
    except InvalidPositionError:
        print("Invalid position! The position must be in the range of [1-9]!")
    except PositionOccupiedError:
        print("Position is already occupied!")
    else:
        return True, [row, index]

    return False, None


def row_checking(board):
    """
    Checks if the current play won with on the rows
    """
    for row in board:
        row_as_set = set(row)
        if len(row_as_set) == 1 and row_as_set != {" "}:
            return True

    return False


def col_checking(board):
    """
    Checks if the current play won with on the cols
    """
    for col_index in range(SIZE):
        col_list = []
        for row_index in range(SIZE):
            col_list.append(board[row_index][col_index])

        col_as_set = set(col_list)

        if len(col_as_set) == 1 and col_as_set != {" "}:
            return True

    return False


def diagonal_checking_board(board):
    """
    Checks if the current play won with on the diagonals
    """
    first_diagonal = []
    second_diagonal = []

    for index in range(SIZE):
        first_diagonal.append(board[index][index])

    for index in range(SIZE):
        second_diagonal.append(board[index][SIZE - index - 1])

    first_diagonal_as_set = set(first_diagonal)
    second_diagonal_as_set = set(second_diagonal)

    if len(first_diagonal_as_set) == 1 and first_diagonal_as_set != {" "} or \
            len(second_diagonal_as_set) == 1 and second_diagonal_as_set != {" "}:
        return True

    return False


def check_if_player_won(board):
    """
    Checks if the current player won by calling functions
    """
    if row_checking(board) or col_checking(board) or diagonal_checking_board(board):
        return True

    return False


def tik_tak_toe_game(player_one, player_two):
    """
    This is the function that will execute the game
    """
    print("\nHere is the numerical representation of the board:")

    numeric_board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    board = [[el for el in "   "] for _ in range(3)]
    print_board(numeric_board)

    sleep(2)

    print(f"\n{player_one[0]} starts first!")

    turns = 1
    is_draw = True

    while True:
        if turns % 2 != 0:
            current_player = player_one
        else:
            current_player = player_two

        command = input(f"{current_player[0]}, choose a free position in [1-9]: ")

        result_of_checking = check_if_command_is_valid(command, board)
        if not result_of_checking[0]:
            continue

        row, col = result_of_checking[1]

        board[row][col] = current_player[1]

        print_board(board)

        turns += 1
        print()

        if turns >= 6:
            if check_if_player_won(board):
                print(f"{current_player[0]} won!")
                is_draw = False
                break
        if turns >= 10:
            break

    if is_draw:
        print("Draw")


def main():
    player_one, player_two = game_setup()

    tik_tak_toe_game(player_one, player_two)


if __name__ == "__main__":
    main()
