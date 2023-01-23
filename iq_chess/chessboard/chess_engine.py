#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chess engine functions.
"""

import os
import chess
import termcolor
import random
import time
import simple_term_menu
import pynput.keyboard

try:
    from . import chess_figures
except ImportError:
    import chess_figures

__version__ = (0, 0, 0, 1)

FIGURE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30, 
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900,
}

PAWN_EVAL_WHITE = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

PAWN_EVAL_BLACK = list(reversed(PAWN_EVAL_WHITE))

KNIGHT_EVAL = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

BISHOP_EVAL_WHITE = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

BISHOP_EVAL_BLACK = list(reversed(BISHOP_EVAL_WHITE))

ROOK_EVAL_WHITE = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

ROOK_EVAL_BLACK = list(reversed(ROOK_EVAL_WHITE))

QUEEN_EVAL = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

KING_EVAL_WHITE = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
    [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
]

KING_EVAL_BLACK = list(reversed(KING_EVAL_WHITE))

POSITION_COUNT = 0
DEFAULT_DEPTH = 3

PLAYER_COLOR = chess.WHITE
BOARD = None

START_POSITION = None
STOP_POSITION = None
CURSOR_POSITION = ('e', '2')


def getStrBoard(board):
    """
    Get string unicode board in color.
    
    :param board: Board object.
    :return: String board.
    """
    global PLAYER_COLOR
    global CURSOR_POSITION
    global START_POSITION

    result = ''
    board_lines = str(board).replace(' ', '').split(os.linesep)
    if PLAYER_COLOR == chess.BLACK:
        board_lines.reverse()
    rank_names = reversed(chess.RANK_NAMES) if PLAYER_COLOR == chess.WHITE else chess.RANK_NAMES
    for i_rank, rank_name in enumerate(rank_names):
        result += rank_name
        for i_file, file_name in enumerate(chess.FILE_NAMES):
            i = i_rank * len(chess.FILE_NAMES) + i_file
            square_color = bool((i if (i_rank % 2) else (i + 1)) % 2)
            figure_symbol = board_lines[i_rank][i_file]
            figure = chess.UNICODE_PIECE_SYMBOLS.get(figure_symbol, ' ')
            figure_color = chess_figures.WHITE_FIGURE_COLOR if figure_symbol.isupper() else chess_figures.BLACK_FIGURE_COLOR

            cur_square_color = 'on_white' if square_color else 'on_grey'
            if CURSOR_POSITION == (file_name, rank_name):
                cur_square_color = 'on_cyan'
            elif START_POSITION and START_POSITION == (file_name, rank_name):
                cur_square_color = 'on_blue'

            result += termcolor.colored(figure, figure_color, cur_square_color)
            result += termcolor.colored(' ', figure_color, cur_square_color)
        result += os.linesep
    for file_name in chess.FILE_NAMES:
        result += ' ' + file_name
    result += os.linesep
    return result


def printStrBoard(board):
    """
    Get string unicode board in color.

    :param board: Board object.
    :return: String board.
    """
    str_board = getStrBoard(board)
    print(str_board)


def getStrBigBoard(board):
    """
    Get string big board in color.

    :param board: Board object.
    :return: True/False.
    """
    global PLAYER_COLOR
    global START_POSITION
    global CURSOR_POSITION
    result = ''

    board_lines = str(board).replace(' ', '').split(os.linesep)
    if PLAYER_COLOR == chess.BLACK:
        board_lines.reverse()

    rank_names = reversed(chess.RANK_NAMES) if PLAYER_COLOR == chess.WHITE else chess.RANK_NAMES
    for i_rank, rank_name in enumerate(rank_names):
        for i_row in range(chess_figures.SQUARE_HEIGHT):
            result += rank_name if i_row == int(chess_figures.SQUARE_HEIGHT / 2) else ' '
            for i_file, file_name in enumerate(chess.FILE_NAMES):
                i = (i_rank * len(chess.FILE_NAMES)) + i_file
                square_color = bool((i if (i_rank % 2) else (i + 1)) % 2)
                figure_symbol = board_lines[i_rank][i_file]
                figure = chess_figures.FIGURES_ASCII.get(figure_symbol, '')
                figure_lines = figure.split(os.linesep)[1:] if figure else None
                figure_color = chess_figures.WHITE_FIGURE_COLOR if figure_symbol.isupper() else chess_figures.BLACK_FIGURE_COLOR

                square_line = ''
                for i_col in range(chess_figures.SQUARE_WIDTH):
                    symbol = ' '
                    if figure_lines and i_row < len(figure_lines) and i_col < len(figure_lines[i_row]):
                        symbol = figure_lines[i_row][i_col]
                    square_line += symbol

                cur_square_color = 'on_white' if square_color else 'on_grey'
                if CURSOR_POSITION == (file_name, rank_name):
                    cur_square_color = 'on_cyan'
                elif START_POSITION and START_POSITION == (file_name, rank_name):
                    cur_square_color = 'on_blue'

                result += termcolor.colored(square_line, figure_color, cur_square_color)
            result += os.linesep

    for file_name in chess.FILE_NAMES:
        result += '    %s     ' % file_name
    result += os.linesep
    # print(board)
    return result


def printBigBoard(board, show_small_board=True, auto_clear=True):
    """
    Print big board in color.

    :param board: Board object.
    :param show_small_board: Show small board?
    :param auto_clear: Auto clear screen?
    :return: True/False.
    """
    if auto_clear:
        clear()

    str_big_board = getStrBigBoard(board)
    if show_small_board:
        str_board = getStrBoard(board)
        str_board_lines = str_board.split(os.linesep)
        str_board_line_count = len(str_board_lines)
        str_big_board_lines = str_big_board.split(os.linesep)
        for i, str_board_line in enumerate(str_board_lines):
            str_big_board_lines[-(str_board_line_count - i)] += '\t' + str_board_line
        str_big_board = os.linesep.join(str_big_board_lines)
    print(str_big_board)


def getBestMove(board):
    """
    """
    if board.is_game_over():
        print('Game over')

    global POSITION_COUNT
    POSITION_COUNT = 0
    depth = DEFAULT_DEPTH

    time_player1 = time.time()
    best_move = getMinimaxRoot(depth, board, True)
    time_player2 = time.time()
    move_time = time_player2 - time_player1
    positions_per_second = POSITION_COUNT * 1000 / move_time
    
    print('Position count:', POSITION_COUNT)
    print('Time:', str(move_time / 1000) + 's')
    print('Position per second', positions_per_second)
    return best_move


def getMinimaxRoot(depth, board, is_maximising_player):
    """
    """
    new_game_moves = list(board.legal_moves)
    best_move = -9999
    best_move_found = None

    for i, new_game_move in enumerate(new_game_moves):
        board.push(new_game_move)
        value = getMinimax(depth - 1, board, -10000, 10000, not is_maximising_player)
        board.pop()

        if value >= best_move:
            best_move = value
            best_move_found = new_game_move
    if best_move_found is None:
        print('Not found best move')
    return best_move_found


def getMinimax(depth, board, alpha, beta, is_maximising_player):
    """
    """
    global POSITION_COUNT
    POSITION_COUNT += 1

    if depth == 0:
        return -evaluateBoard(board)

    new_game_moves = list(board.legal_moves)

    best_move = -9999
    if is_maximising_player:
        for i, new_game_move in enumerate(new_game_moves):
            board.push(new_game_move)
            best_move = max(best_move, getMinimax(depth - 1, board, alpha, beta, not is_maximising_player))
            board.pop()

            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        for i, new_game_move in enumerate(new_game_moves):
            board.push(new_game_move)
            best_move = min(best_move, getMinimax(depth - 1, board, alpha, beta, not is_maximising_player))
            board.pop()

            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move


def evaluateBoard(board):
    """
    """
    total_evaluation = 0
    for i_rank in range(len(chess.RANK_NAMES)):
        for i_file in range(len(chess.FILE_NAMES)):
            piece_idx = i_rank * len(chess.RANK_NAMES) + i_file
            piece = board.piece_map().get(piece_idx, None)
            total_evaluation += getPieceValue(piece, i_rank, i_file)
    return total_evaluation


def getPieceValue(piece, x, y):
    """
    """
    if piece is None:
        return 0

    absolute_value = getAbsoluteValue(piece, piece.color == chess.WHITE, x ,y);
    return absolute_value if piece.color == chess.WHITE else -absolute_value


def getAbsoluteValue(piece, is_white, x, y):
    """
    """
    if piece.piece_type == chess.PAWN:
        return FIGURE_VALUES[piece.piece_type] + (PAWN_EVAL_WHITE[y][x] if is_white else PAWN_EVAL_BLACK[y][x])
    elif piece.piece_type == chess.ROOK:
        return FIGURE_VALUES[piece.piece_type] + (ROOK_EVAL_WHITE[y][x] if is_white else ROOK_EVAL_BLACK[y][x])
    elif piece.piece_type == chess.KNIGHT:
        return FIGURE_VALUES[piece.piece_type] + KNIGHT_EVAL[y][x]
    elif piece.piece_type == chess.BISHOP:
        return FIGURE_VALUES[piece.piece_type] + (BISHOP_EVAL_WHITE[y][x] if is_white else BISHOP_EVAL_BLACK[y][x])
    elif piece.piece_type == chess.QUEEN:
        return FIGURE_VALUES[piece.piece_type] + QUEEN_EVAL[y][x]
    elif piece.piece_type == chess.KING:
        return FIGURE_VALUES[piece.piece_type] + (KING_EVAL_WHITE[y][x] if is_white else KING_EVAL_BLACK[y][x])

    print('Unknown piece type <%s>' % piece.type)


def clear():
    """

    :return:
    """
    os.system('clear' if os.name == 'posix' else 'cls')


def onKeyPress(key):
    """

    :param key:
    :return:
    """
    global CURSOR_POSITION
    global BOARD
    global START_POSITION
    global STOP_POSITION

    if key == pynput.keyboard.Key.left:
        cur_file_idx = chess.FILE_NAMES.index(CURSOR_POSITION[0])
        file_name = chess.FILE_NAMES[cur_file_idx - 1] if cur_file_idx else chess.FILE_NAMES[0]
        CURSOR_POSITION = (file_name, CURSOR_POSITION[1])
    elif key == pynput.keyboard.Key.right:
        cur_file_idx = chess.FILE_NAMES.index(CURSOR_POSITION[0])
        file_name = chess.FILE_NAMES[cur_file_idx + 1] if cur_file_idx < (len(chess.FILE_NAMES) - 1) else chess.FILE_NAMES[-1]
        CURSOR_POSITION = (file_name, CURSOR_POSITION[1])
    elif key == pynput.keyboard.Key.up:
        cur_rank_idx = chess.RANK_NAMES.index(CURSOR_POSITION[1])
        rank_name = chess.RANK_NAMES[cur_rank_idx + 1] if cur_rank_idx < (len(chess.RANK_NAMES) - 1) else chess.RANK_NAMES[-1]
        CURSOR_POSITION = (CURSOR_POSITION[0], rank_name)
    elif key == pynput.keyboard.Key.down:
        cur_rank_idx = chess.RANK_NAMES.index(CURSOR_POSITION[1])
        rank_name = chess.RANK_NAMES[cur_rank_idx - 1] if cur_rank_idx else chess.RANK_NAMES[0]
        CURSOR_POSITION = (CURSOR_POSITION[0], rank_name)
    elif key == pynput.keyboard.Key.space:
        if START_POSITION is None:
            START_POSITION = CURSOR_POSITION
        elif STOP_POSITION is None:
            STOP_POSITION = CURSOR_POSITION
        if (STOP_POSITION and STOP_POSITION) and (START_POSITION != STOP_POSITION):
            move_adr = ''.join(START_POSITION) + ''.join(STOP_POSITION)
            move = chess.Move.from_uci(move_adr)
            if move in BOARD.legal_moves:
                print(termcolor.colored('Move %s' % move_adr, 'green'))
                BOARD.push(move)
                printBigBoard(BOARD)
                print('I\'m pondering a move')
                START_POSITION = None
                STOP_POSITION = None

                move = getBestMove(BOARD)
                if move:
                    BOARD.push(move)
            else:
                from_adr = '%s%s' % START_POSITION
                to_adr = '%s%s' % STOP_POSITION
                print(termcolor.colored('Illegal move %s -> %s' % (from_adr, to_adr), 'red'))
                STOP_POSITION = None
                return
        elif (STOP_POSITION and STOP_POSITION) and (START_POSITION == STOP_POSITION):
            print(termcolor.colored('Not move %s -> %s' % (START_POSITION, STOP_POSITION), 'red'))
            START_POSITION = None
            STOP_POSITION = None
            return

    printBigBoard(BOARD)


def onKeyRelease(key):
    """

    :param key:
    :return:
    """
    global BOARD

    if key == pynput.keyboard.Key.esc:
        print('Exit')
        # Stop listener
        return False
    if BOARD.is_checkmate():
        print('Checkmate!!!')
        return False
    elif BOARD.is_game_over():
        print('Game over!!!')
        return False
    elif BOARD.is_stalemate():
        print('Stalemate!!!')
        return False


def moveCursor(board):
    """

    :param board:
    :return:
    """
    # Collect events until released
    with pynput.keyboard.Listener(on_press=onKeyPress,
                                  on_release=onKeyRelease) as listener:
        listener.join()
        # printBigBoard(board)


def game():
    global BOARD
    global PLAYER_COLOR

    # Show logo
    clear()
    print(termcolor.colored(chess_figures.CHESS_LOGO_ASCII, chess_figures.LOGO_COLOR))
    print('Player')

    choice_player_color_menu = simple_term_menu.TerminalMenu(['WHITE', 'BLACK'])
    idx = choice_player_color_menu.show()
    PLAYER_COLOR = not bool(idx)

    BOARD = board = chess.Board()
    if PLAYER_COLOR == chess.BLACK:
        legal_moves = list(board.legal_moves)
        move = legal_moves[int(random.random() * len(legal_moves))]
        board.push(move)
    printBigBoard(board)

    moveCursor(board=board)
