import random

def ai_select_move(board, player):
    valid_ai_moves = valid_move_list(board, player)
    if valid_ai_moves:
        return random.choice(valid_ai_moves)
    return None

BLACK = "●"
WHITE = "○"
BOARD_SIZE = 8 

def initialize_board():
    board = [[' ' for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    board[3][3], board[3][4] = WHITE, BLACK
    board[4][3], board[4][4] = BLACK, WHITE
    return board

def print_board(board):
    print("    " + "   ".join([f"{num}" for num in range(BOARD_SIZE)]))
    print("  ┌───" + "───".join(["┬" for _ in range(BOARD_SIZE-1)]) + "───┐")
    for row in range(BOARD_SIZE):
        print(f"{row} │ " + " │ ".join([board[row][col] for col in range(BOARD_SIZE)]) + " │")
        if(row != BOARD_SIZE-1):
            print("  ├─" +  "─┼─".join(["─" for _ in range(BOARD_SIZE)]) + "─┤")
        else:
            print("  └─" +  "─┴─".join(["─" for _ in range(BOARD_SIZE)]) + "─┘")

def valid_move(board, row, col, player):
    directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
    for (dir_r, dir_c) in directions:
        (next_r, next_c) = (row + dir_r, col + dir_c)
        if (0 <= next_r < BOARD_SIZE and 0 <= next_c < BOARD_SIZE) and (board[next_r][next_c] != ' ' and board[next_r][next_c] != player):
            (next_r, next_c) = (next_r + dir_r, next_c + dir_c)
            while 0 <= next_r < BOARD_SIZE and 0 <= next_c < BOARD_SIZE:
                if board[next_r][next_c] == player:
                    return True
                elif board[next_r][next_c] == ' ':
                    break
                (next_r, next_c) = (next_r + dir_r, next_c + dir_c)
    return False


def place_move(board, row, col, player):
    board[row][col] = player
    directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1),
                  (0, 1), (1, 1), (1, 0), (1, -1)]
    opponent = BLACK if player == WHITE else WHITE

    for dir_r, dir_c in directions:
        reverse = []
        next_r, next_c = row + dir_r, col + dir_c

        while 0 <= next_r < BOARD_SIZE and 0 <= next_c < BOARD_SIZE:
            current = board[next_r][next_c]
            if current == opponent:
                reverse.append((next_r, next_c))
            elif current == player:
                for re_r, re_c in reverse:
                    board[re_r][re_c] = player
                break
            else:
                break
            next_r += dir_r
            next_c += dir_c
    return board


def valid_move_list(board, player):
    flip = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == ' ' and valid_move(board, row, col, player):
                flip.append((row, col))
    return flip

def print_winner(board):
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    print(f"{BLACK}{black_count} - {WHITE}{white_count}")
    if black_count>white_count:
        print("Black Win!")
    elif white_count>black_count:
        print("White Win!")
    else:
        print("Draw")

def othello():
    while True:
        choice = input("Do you want to go first (●) or second (○)? Enter 'b' or 'w': ").strip().lower()
        if choice == 'b':
            human_player = BLACK
            ai_player = WHITE
            player = BLACK
            break
        elif choice == 'w':
            human_player = WHITE
            ai_player = BLACK
            player = BLACK
            break
        else:
            print("Invalid Input")

    board = initialize_board()
    last_player_pass = False

    print_board(board)

    while True:
        valid_moves = valid_move_list(board, player)

        if not valid_moves:
            if last_player_pass:
                break

            print(f"{player} has no valid moves. Turn passed.")
            if player == human_player:
                print("You have no valid moves. Your turn is skipped.")
            else:
                print("AI has no valid moves. Its turn is skipped.")

            last_player_pass = True
            player = WHITE if player == BLACK else BLACK
            continue
        else:
            last_player_pass = False

        
        if player == human_player:
            while True:
                try:
                    user_input = input("Enter your move or 'q' to quit: ").strip().lower()
                    if user_input in ('q', 'quit'):
                        print("Game aborted by player.")
                        return
                    col, row = map(int, user_input.split())
                    if (row, col) in valid_moves:
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input")
        else:
            row, col = ai_select_move(board, ai_player)
            print(f"AI ({ai_player}) placed at col {col}, row {row}")

        place_move(board, row, col, player)
        print_board(board)
        player = WHITE if player == BLACK else BLACK

    print_winner(board)

if __name__ == "__main__":
    othello()
