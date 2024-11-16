"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] != " "):
                return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):

    closed_ends = 0

    back_end = (y_end + d_y, x_end + d_x)
    front_end = (y_end - (length * d_y), x_end - (length * d_x))

    if(back_end[0] > (len(board) - 1) or back_end[1] > (len(board) - 1)):
        closed_ends += 1
    elif(back_end[0] < 0 or back_end[1] < 0):
        closed_ends += 1
    else: # back end has valid coordinate
        
        if(board[back_end[0]][back_end[1]] != " "): # if board is blocked
            closed_ends += 1

    if(front_end[0] < 0 or front_end[1] < 0):
        closed_ends += 1
    elif(front_end[0] > (len(board) - 1) or front_end[1] > (len(board) - 1)):
        closed_ends += 1
    else: # front end has valid coordinate
        
        if(board[front_end[0]][front_end[1]] != " "): # if board is blocked
            closed_ends += 1

    if(closed_ends == 0):
        return "OPEN"
    elif(closed_ends == 1):
        return "SEMIOPEN"

    return "CLOSED" # closed_ends == 2


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0

    current_y = y_start
    current_x = x_start

    next_y = 0
    next_x = 0

    current_length = 0 # length of potential sequence

    seq_ends = [] # array of sequence endings with length length

    while((current_y > -1 and current_y < len(board)) and (current_x > -1 and current_x < len(board))):
        # while current_y is between 0 and 7, and current_x is between 0 and 7
        # aka while both coordinates are legal

        if(board[current_y][current_x] == col):
            current_length += 1
        else:
            if(current_length == length): # checking if the previous sequence had length
                seq_ends.append((current_y - d_y, current_x - d_x))
            current_length = 0

        next_y = current_y + d_y
        next_x = current_x + d_x

        if(next_y < 0 or next_y > (len(board) - 1) or next_x < 0 or next_x > (len(board) - 1)): # if we've hit the end
            if(current_length == length): # and if the current length is right
                seq_ends.append((current_y, current_x))


        # updating current location
        current_y += d_y
        current_x += d_x


    for end in seq_ends: # for each sequence end, find their states
        state = is_bounded(board, end[0], end[1], length, d_y, d_x)
        if(state == "OPEN"):
            open_seq_count += 1
        if(state == "SEMIOPEN"):
            semi_open_seq_count += 1


    return open_seq_count, semi_open_seq_count



def detect_rows(board, col, length):
    ####CHANGE ME
    open_seq_count, semi_open_seq_count = 0, 0

    seq_each_row = (0, 0)

    for i in range(8): # using directions (0, 1) and (1, 0)

        # for horizontal direction (0, 1) all rows
        seq_each_row = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += seq_each_row[0]
        semi_open_seq_count += seq_each_row[1]

        # do the same thing for columns (1, 0) direction
        seq_each_row = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += seq_each_row[0]
        semi_open_seq_count += seq_each_row[1]

        # doing all start values in dir (1, 1) for top row
        seq_each_row = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += seq_each_row[0]
        semi_open_seq_count += seq_each_row[1]

        # dir (1, 1) for first col
        seq_each_row = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += seq_each_row[0]
        semi_open_seq_count += seq_each_row[1]

        # doing all start values in dir (1, -1) for top row
        seq_each_row = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += seq_each_row[0]
        semi_open_seq_count += seq_each_row[1]

        # dir (1, -1) for last col
        seq_each_row = detect_row(board, col, i, (len(board) - 1), length, 1, -1)
        open_seq_count += seq_each_row[0]
        semi_open_seq_count += seq_each_row[1]


    # positions (0, 0) and (0, 7) - subtract these because they overlap
    seq_each_row = detect_row(board, col, 0, 0, length, 1, 1)
    open_seq_count -= seq_each_row[0]
    semi_open_seq_count -= seq_each_row[1]

    seq_each_row = detect_row(board, col, 0, (len(board) - 1), length, 1, -1)
    open_seq_count -= seq_each_row[0]
    semi_open_seq_count -= seq_each_row[1]

    return open_seq_count, semi_open_seq_count

def search_max(board):
    move_y, move_x = 0, 0
    
    highest_score = -100000
    curr_score = 0
    
    board_copy = [] # deep copy of the board
    for sublist in board:
        board_copy.append(sublist[:])
    
    # create a copy of the board, iterate through the empty spots and try to put
    # 'b' in each empty spot and compute the score
    # if that score > highest_score, then highest_score = score
    # and move_y, move_x = those moves
    
    for i in range(len(board)):
        for j in range(len(board)):
            if(board_copy[i][j] == ' '): # if the space is empty
    
                board_copy[i][j] = 'b'
                curr_score = score(board_copy)
    
                if(curr_score > highest_score):
                    highest_score = curr_score
                    move_y = i
                    move_x = j
    
                board_copy[i][j] = ' ' # return to original state

    return move_y, move_x



def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def closed_5s(board, col):
    '''
    Returns
    -------
    True if there is a closed 5 for color col
    False if there is not
    '''
    curr_len = 0
    
    # horizontal rows
    for i in range(len(board)):
        curr_len = 0
        for j in range(len(board)):
            
            if(board[i][j] != col): # going through the horizontal rows
                curr_len = 0
            else:
                curr_len += 1
                if(curr_len == 5):
                    return True
                
    # vertical columns
    for i in range(len(board)):
        curr_len = 0 # resetting
        for j in range(len(board)):
            
            if(board[j][i] != col): # going through the vertical cols
                curr_len = 0
            else:
                curr_len += 1
                if(curr_len == 5):
                    return True
    
    # going through diagonals in the (1, 1) direction
    # only need to go up to index 3
    d_y = 1
    d_x = 1
    curr_y = 0
    curr_x = 0
    next_y = 0
    next_x = 0
    for i in range(len(board)):
        # going through top row
        curr_len = 0
        curr_y = 0
        curr_x = i
        
        # carries until end of the row
        while(curr_y >= 0 and curr_x >= 0 and curr_y < 8 and curr_x < 8):
            next_y = curr_y + d_y
            next_x = curr_x + d_x
            
            if(board[curr_y][curr_x] != col): 
                curr_len = 0
            else:
                curr_len += 1
                if(curr_len == 5):
                    if(next_x >= 0 and next_y >= 0 and next_x < 8 and next_y < 8):
                        if(board[next_y][next_x] != col):
                            curr_len == 0 # mess it up
                if(curr_len == 5): # if it still equals 5 (if it is not the edge case)
                    return True
            
            curr_y += d_y
            curr_x += d_x
            
        # going through the first col
        curr_len = 0
        curr_y = i
        curr_x = 0
        
        # carries until end of the row
        while(curr_y >= 0 and curr_x >= 0 and curr_y < 8 and curr_x < 8):
            next_y = curr_y + d_y
            next_x = curr_x + d_x
            
            if(board[curr_y][curr_x] != col): 
                curr_len = 0
            else:
                curr_len += 1
                if(curr_len == 5):
                    if(next_x >= 0 and next_y >= 0 and next_x < 8 and next_y < 8):
                        if(board[next_y][next_x] != col):
                            curr_len == 0 # mess it up
                if(curr_len == 5): # if it still equals 5 (if it is not the edge case)
                    return True
            
            curr_y += d_y
            curr_x += d_x
            
    d_y = 1
    d_x = -1
    curr_y = 0
    curr_x = 0
    next_y = 0
    next_x = 0
    for i in range(len(board)):
        curr_len = 0
        curr_y = i
        curr_x = 7
        # going through last col
        
        # carries until end of the row
        while(curr_y >= 0 and curr_x >= 0 and curr_y < 8 and curr_x < 8): 
            next_y = curr_y + d_y
            next_x = curr_x + d_x
            
            if(board[curr_y][curr_x] != col): 
                curr_len = 0
            else:
                curr_len += 1
                if(curr_len == 5):
                    if(next_x >= 0 and next_y >= 0 and next_x < 8 and next_y < 8):
                        if(board[next_y][next_x] != col):
                            curr_len == 0 # mess it up
                if(curr_len == 5): # if it still equals 5 (if it is not the edge case)
                    return True
            
            curr_y += d_y
            curr_x += d_x
            
        curr_len = 0
        curr_y = 0
        curr_x = i
        # going through the top row
        
        # carries until end of the row
        while(curr_y >= 0 and curr_x >= 0 and curr_y < 8 and curr_x < 8):
            next_y = curr_y + d_y
            next_x = curr_x + d_x
            
            if(board[curr_y][curr_x] != col): 
                curr_len = 0
            else:
                curr_len += 1
                if(curr_len == 5):
                    if(next_x >= 0 and next_y >= 0 and next_x < 8 and next_y < 8):
                        if(board[next_y][next_x] != col):
                            curr_len == 0 # mess it up
                if(curr_len == 5): # if it still equals 5 (if it is not the edge case)
                    return True
            
            curr_y += d_y
            curr_x += d_x
    
    return False


def is_win(board):
    # does score function check closed sequences of 5? i don't think so...

    board_full = True
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                board_full = False
    if(board_full == True):
        return "Draw"
    
    if(score(board) == 100000):
        return "Black won"
    
    if(score(board) == -100000):
        return "White won"
    
    # check for closed sequences of 5
    # located at startpoints ()
    
    if(closed_5s(board, 'w')):
        return "White won"
    
    if(closed_5s(board, 'b')):
        return "Black won"
    
    
    return "Continue playing"
    


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))




def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)
    # test_search_max()
    # test_is_bounded()
    # some_tests()