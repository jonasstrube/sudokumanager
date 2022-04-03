from array import array
from copy import deepcopy
from turtle import position

def __position_is_already_taken(line: int, row: int, sudoku_or_quadrant: array) -> bool:
    if sudoku_or_quadrant[line][row][0] == None:
        return False
    else:
        return True

def __get_quadrant_index_of_position(line: int, row: int) -> int:
    quadrant_line = int(line / 3)
    quadrant_row = int(row / 3)
    quadrant_index = quadrant_row + (quadrant_line * 3)
    return quadrant_index

def __position_is_in_quadrant(line: int, row: int, quadrant_index_of_position: int) -> bool:
    quadrant_index = __get_quadrant_index_of_position(line, row)
    if quadrant_index == quadrant_index_of_position:
        return True
    else:
        return False

def __position_has_blocking_number(number: int, line: int, row: int, sudoku_to_work_on: array) -> bool:
    blocking_number_list: array = sudoku_to_work_on[line][row][1]
    for blocking_number in blocking_number_list:
        if blocking_number == number:
            return True
    return False

def __quadrantline_is_blocked_by_blocking_numbers(number: int, line_quadrantrelative: int, current_quadrant: array) -> bool:
    possible_positions = []
    for line in range(0, 3):
        for row in range(0, 3):
            if not __position_is_already_taken(line, row, current_quadrant):
                possible_numbers_list = current_quadrant[line][row][1]
                for possible_number in possible_numbers_list:
                    if possible_number == number:
                        possible_positions.append([line, row])

    if len(possible_positions) == 0:
        return False
    for position in possible_positions:
        if not line_quadrantrelative == position[0]:
            return False
    return True

def __quadrantrow_is_blocked_by_blocking_numbers(number: int, row_quadrantrelative: int, current_quadrant: array) -> bool:
    possible_positions = []
    for line in range(0, 3):
        for row in range(0, 3):
            if not __position_is_already_taken(line, row, current_quadrant):
                possible_numbers_list = current_quadrant[line][row][1]
                for possible_number in possible_numbers_list:
                    if possible_number == number:
                        possible_positions.append([line, row])
    return False

def __blocking_numbers_in_line_or_row(number: int, line: int, row: int, sudoku_to_work_on: array) -> bool:
    quadrant_index_of_position: int = __get_quadrant_index_of_position(line, row)
    line_quadrantrelative = line % 3
    row_quadrantrelative = row % 3
    for current_row in range(0, 9):
        if not __position_is_in_quadrant(line, current_row, quadrant_index_of_position) and sudoku_to_work_on[line][current_row][0] == None:
            if __position_has_blocking_number(number, line, current_row, sudoku_to_work_on):
                current_quadrant_index = __get_quadrant_index_of_position(line, current_row)
                current_quadrant = __get_quadrant(current_quadrant_index, sudoku_to_work_on)
                if __quadrantline_is_blocked_by_blocking_numbers(number, line_quadrantrelative, current_quadrant):
                    return True

    for current_line in range(0, 9):
        if not __position_is_in_quadrant(current_line, row, quadrant_index_of_position) and sudoku_to_work_on[current_line][row][0] == None:
            if __position_has_blocking_number(number, current_line, row, sudoku_to_work_on):
                current_quadrant_index = __get_quadrant_index_of_position(current_line, row)
                current_quadrant = __get_quadrant(current_quadrant_index, sudoku_to_work_on)
                if __quadrantrow_is_blocked_by_blocking_numbers(number, row_quadrantrelative, current_quadrant):
                    return True
    
    return False

def __get_quadrant(quadrant_index: int, sudoku_to_work_on: array) -> array:
    line_upper_left_field = quadrant_index - (quadrant_index % 3)
    field_upper_left_field = (quadrant_index % 3) * 3
    upper_left_field = [line_upper_left_field, field_upper_left_field]

    quadrant: array = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    for line in range(0, 3):
        for row in range(0, 3):
            sudoku_line = upper_left_field[0] + line
            sudoku_row = upper_left_field[1] + row
            quadrant[line][row] = deepcopy(sudoku_to_work_on[sudoku_line][sudoku_row])
    
    return quadrant

def __same_number_in_line_or_row(number: int, line: int, row: int, sudoku_to_work_on: array) -> bool:
    for current_row in range(0, 9):
        if sudoku_to_work_on[line][current_row][0] == number:
            return True
    
    for current_line in range(0, 9):
        if sudoku_to_work_on[current_line][row][0] == number:
            return True
    
    return False

def __number_fits_in_position(number: int, line: int, row: int, sudoku_to_work_on: array) -> bool:
    if (    __same_number_in_line_or_row(number, line, row, sudoku_to_work_on) 
        or __blocking_numbers_in_line_or_row(number, line, row, sudoku_to_work_on)):
        return False
    else:
        return True

def __get_positions_inside_of_quadrant(quadrant_index: int, sudoku: array) -> array:
    quadrant_positions: array = []

    upper_line = quadrant_index - (quadrant_index % 3)
    left_row = (quadrant_index % 3) * 3
    upper_left_position = [upper_line, left_row]

    for current_line in range(0, 3):
        for current_row in range(0, 3):
            position_line = upper_left_position[0] + current_line
            position_row = upper_left_position[1] + current_row
            quadrant_positions.append([position_line, position_row])
    return quadrant_positions

def print_sudoku(sudoku: array):
    for line in sudoku:
        line_str: str = ''
        for box in line:
            if box[0]:
                line_str += str(box[0]) + ' '
            else:
                line_str += '  '
        print(line_str)

def positions_are_in_line(positions: array) -> bool:
    possible_positions_local = deepcopy(positions)

    line_candidate = possible_positions_local[0][0]
    row_candidate = possible_positions_local[0][1]
    del(possible_positions_local[0])
    for position in possible_positions_local:
        if line_candidate or row_candidate:
            if not line_candidate == position[0]:
                line_candidate = None
            if not row_candidate == position[1]:
                row_candidate = None
    
    if line_candidate or row_candidate:
        return True
    else:
        return False 

def block_line_or_row(number: int, blocking_positions: array, sudoku: array) -> None:
    for position in blocking_positions:
        blocking_numbers = sudoku[position[0]][position[1]][1]
        for blocking_number in blocking_numbers:
            if number == blocking_number:
                return None
    for position in blocking_positions:
        sudoku[position[0]][position[1]][1].append(number)

def number_is_already_in_quadrant(number: int, quadrant_index: int, sudoku_to_work_on: array) -> bool:
    quadrant = __get_quadrant(quadrant_index, sudoku_to_work_on)

    for line in quadrant:
        for field in line:
            if field[0] == number:
                return True
    return False

def get_possible_positions_of_number(number: int, quadrant_index: int, sudoku_to_work_on: array) -> array:
    possible_positions: array = []
    for line_quadrantrelative in range(0, 3):
        line = line_quadrantrelative + quadrant_index - (quadrant_index % 3)
        for row_quadrantrelative in range(0, 3):
            row = row_quadrantrelative + (quadrant_index % 3) * 3
            if __position_is_already_taken(line, row, sudoku_to_work_on):
                pass
            elif __number_fits_in_position(number, line, row, sudoku_to_work_on):
                possible_positions.append([line, row])
            else:
                # number does not fit the position
                pass
    
    return possible_positions

def erase_possible_positions_at_position(line: int, row: int, sudoku: array) -> None:
    sudoku[line][row][1] = []

def erase_possible_positions_of_number(number: int, quadrant_index: int, sudoku: array) -> None:
    quadrant_position_list = __get_positions_inside_of_quadrant(quadrant_index, sudoku)
    
    for quadrant_position in quadrant_position_list:
        possible_positions = sudoku[quadrant_position[0]][quadrant_position[1]][1]
        for index in range(len(possible_positions)):
            if possible_positions[index] == number:
                del(possible_positions[index])
                break

def work_sudoku(sudoku: array) -> None:
    for number in range(1, 10): # 1 to 9
        for quadrant_index in range(9): # 9 quadrants, 0 to 8 
            if not number_is_already_in_quadrant(number, quadrant_index, sudoku):
                # fill in number if it only has one possible position 
                possible_positions = get_possible_positions_of_number(number, quadrant_index, sudoku)
                
                if len(possible_positions) == 1:
                    line = possible_positions[0][0]
                    row = possible_positions[0][1]
                    sudoku[line][row][0] = number
                    erase_possible_positions_at_position(line, row, sudoku)
                    erase_possible_positions_of_number(number, quadrant_index, sudoku)
                elif len(possible_positions) > 1:
                    block_possible = positions_are_in_line(possible_positions)
                    if block_possible:
                        block_line_or_row(number, possible_positions, sudoku)
                else:
                    # Exception: there is no possible position in the given quadrant for the number
                    raise Exception
            else:
                # number is already in quadrant
                pass

def get_input() -> str:

    # TODO get sudoku from user input

    # return [
    #     [None, None, 6, 5, None, 7, 4, None, None],
    #     [None, 8, None, 9, None, 3, None, 6, None],
    #     [3, None, None, None, None, None, None, None, 5],
    #     [7, 6, None, None, 4, None, None, 8, 2],
    #     [None, None, None, 6, None, 8, None, None, None],
    #     [8, 5, None, None, 9, None, None, 1, 3],
    #     [5, None, None, None, None, None, None, None, 8],
    #     [None, 1, None, 2, None, 9, None, 7, None],
    #     [None, None, 7, 8, None, 4, 1, None, None]
    # ]
    return [
        [3, None, None, 8, None, None, 4, 1, None],
        [None, None, None, 2, 3, None, None, None, 5],
        [None, None, 8, None, None, 1, None, None, 3],
        [6, None, 4, None, None, None, 2, None, None],
        [1, None, 9, 6, None, None, None, 5, None],
        [None, None, None, None, 8, None, None, 3, 6],
        [8, None, None, None, 2, 7, 3, None, None],
        [None, 9, None, None, None, None, None, 6, None],
        [7, None, 1, None, 6, 9, None, 4, 8]
    ]

def main():

    sudoku_input = get_input()

    for line in range(9):
        for row in range(9):
            sudoku_input[line][row] = [sudoku_input[line][row], []]

    print()
    print('Start:')
    print_sudoku(sudoku_input)

    sudoku_to_work_on = deepcopy(sudoku_input)
    sudoku_last_state = None
    iterations = 0
    while(not sudoku_last_state == sudoku_to_work_on): # while something is changing
        iterations += 1
        sudoku_last_state = deepcopy(sudoku_to_work_on)

        work_sudoku(sudoku_to_work_on)

    print('End:')    
    print_sudoku(sudoku_to_work_on)
    print()
    print("Iterations: " + str(iterations))

if __name__== '__main__':
    main()