#!/usr/bin/env python3

import random

# Simple chess board representation and basic move generation

def create_board():
    return [
        list("rnbqkbnr"),
        list("pppppppp"),
        list("........"),
        list("........"),
        list("........"),
        list("........"),
        list("PPPPPPPP"),
        list("RNBQKBNR"),
    ]

def print_board(board):
    print()
    for row in range(8):
        rank = 8 - row
        print(rank, end=" ")
        for col in range(8):
            print(board[row][col], end=" ")
        print()
    print("  a b c d e f g h")
    print()

def get_piece_color(piece):
    if piece == '.':
        return None
    return 'white' if piece.isupper() else 'black'

file_map = 'abcdefgh'

def parse_move(move):
    """Parse moves like e2e4 into coordinates"""
    if len(move) != 4:
        return None
    try:
        x1 = file_map.index(move[0])
        y1 = 8 - int(move[1])
        x2 = file_map.index(move[2])
        y2 = 8 - int(move[3])
        return (x1, y1, x2, y2)
    except Exception:
        return None


def move_to_str(m):
    x1, y1, x2, y2 = m
    return f"{file_map[x1]}{8-y1}{file_map[x2]}{8-y2}"


def inside_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def is_opponent(board, x, y, color):
    p = board[y][x]
    c = get_piece_color(p)
    return c is not None and c != color


def generate_moves(board, x, y):
    piece = board[y][x]
    color = get_piece_color(piece)
    moves = []
    if color is None:
        return moves
    dir_sign = -1 if color == 'white' else 1
    start_row = 6 if color == 'white' else 1

    def add_slide(dx, dy):
        nx, ny = x + dx, y + dy
        while inside_board(nx, ny):
            target = board[ny][nx]
            if target == '.':
                moves.append((x, y, nx, ny))
            elif is_opponent(board, nx, ny, color):
                moves.append((x, y, nx, ny))
                break
            else:
                break
            nx += dx
            ny += dy

    if piece.lower() == 'p':
        ny = y + dir_sign
        if inside_board(x, ny) and board[ny][x] == '.':
            moves.append((x, y, x, ny))
            if y == start_row:
                ny2 = y + 2 * dir_sign
                if board[ny2][x] == '.':
                    moves.append((x, y, x, ny2))
        for dx in (-1, 1):
            nx = x + dx
            ny = y + dir_sign
            if inside_board(nx, ny) and is_opponent(board, nx, ny, color):
                moves.append((x, y, nx, ny))
    elif piece.lower() == 'n':
        for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            nx, ny = x + dx, y + dy
            if inside_board(nx, ny):
                if board[ny][nx] == '.' or is_opponent(board, nx, ny, color):
                    moves.append((x, y, nx, ny))
    elif piece.lower() == 'b':
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            add_slide(dx, dy)
    elif piece.lower() == 'r':
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            add_slide(dx, dy)
    elif piece.lower() == 'q':
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            add_slide(dx, dy)
    elif piece.lower() == 'k':
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if inside_board(nx, ny):
                    if board[ny][nx] == '.' or is_opponent(board, nx, ny, color):
                        moves.append((x, y, nx, ny))
    return moves


def all_moves(board, color):
    moves = []
    for y in range(8):
        for x in range(8):
            if get_piece_color(board[y][x]) == color:
                moves.extend(generate_moves(board, x, y))
    return moves


def apply_move(board, move):
    x1, y1, x2, y2 = move
    piece = board[y1][x1]
    board[y1][x1] = '.'
    board[y2][x2] = piece


def clone_board(board):
    """Return a deep copy of the board."""
    return [row[:] for row in board]


piece_values = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9,
    'k': 0,
}


def evaluate_board(board):
    """Return a material score from white's perspective."""
    score = 0
    for row in board:
        for p in row:
            if p == '.':
                continue
            value = piece_values.get(p.lower(), 0)
            score += value if p.isupper() else -value
    return score


def minimax(board, depth, color):
    """Simple minimax search using material evaluation."""
    if depth == 0:
        return evaluate_board(board)

    moves = all_moves(board, color)
    if not moves:
        return evaluate_board(board)

    next_color = 'black' if color == 'white' else 'white'
    if color == 'white':
        best = float('-inf')
        for mv in moves:
            b2 = clone_board(board)
            apply_move(b2, mv)
            best = max(best, minimax(b2, depth - 1, next_color))
        return best
    else:
        best = float('inf')
        for mv in moves:
            b2 = clone_board(board)
            apply_move(b2, mv)
            best = min(best, minimax(b2, depth - 1, next_color))
        return best


def best_move(board, color, depth=2):
    """Return the best move for the given color using minimax."""
    moves = all_moves(board, color)
    if not moves:
        return None

    next_color = 'black' if color == 'white' else 'white'
    if color == 'white':
        best_val = float('-inf')
        chosen = None
        for mv in moves:
            b2 = clone_board(board)
            apply_move(b2, mv)
            val = minimax(b2, depth - 1, next_color)
            if val > best_val:
                best_val = val
                chosen = mv
        return chosen
    else:
        best_val = float('inf')
        chosen = None
        for mv in moves:
            b2 = clone_board(board)
            apply_move(b2, mv)
            val = minimax(b2, depth - 1, next_color)
            if val < best_val:
                best_val = val
                chosen = mv
        return chosen


def main():
    board = create_board()
    player_color = 'white'
    computer_color = 'black'
    current = 'white'

    while True:
        print_board(board)
        if current == player_color:
            move_str = input('Jouw zet (bijv. e2e4): ').strip()
            parsed = parse_move(move_str)
            if not parsed:
                print('Ongeldige invoer. Probeer opnieuw.')
                continue
            if parsed not in all_moves(board, player_color):
                print('Ongeldige zet. Probeer opnieuw.')
                continue
            apply_move(board, parsed)
        else:
            move = best_move(board, computer_color)
            if move is None:
                print('Geen zetten meer voor de computer. Spel afgelopen.')
                break
            print('Computer zet:', move_to_str(move))
            apply_move(board, move)

        # Check of koning geslagen is
        pieces = sum(board, [])
        if 'k' not in pieces:
            print('Wit wint!')
            break
        if 'K' not in pieces:
            print('Zwart wint!')
            break

        current = computer_color if current == player_color else player_color

if __name__ == '__main__':
    main()
