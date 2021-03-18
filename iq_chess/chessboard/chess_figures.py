#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chess figures.
"""

import chess

PAWN_FIGURE_ASCII = '''


    () 
    )( 
   /__\\
'''

ROOK_FIGURE_ASCII = '''

    II 
    )( 
    )( 
   /__\\
'''

KNIGHT_FIGURE_ASCII = '''

   _,, 
  "-=\\~
    )( 
   /__\\
'''

BISHOP_FIGURE_ASCII = '''

    () 
    )( 
    )( 
   /__\\
'''

QUEEN_FIGURE_ASCII = '''
    oo 
    () 
    )( 
    )( 
   /__\\
'''

KING_FIGURE_ASCII = '''
    ++ 
    () 
    )( 
    )( 
   /__\\
'''


CHESS_LOGO_ASCII = '''
         ,....,
      ,::::::<
     ,::/^\\"``.
    ,::/, `   e`.
   ,::; |        '.
   ,::|  \\___,-.  c)
   ;::|     \\   '-'
   ;::|      \\
   ;::|   _.=`\\
   `;:|.=` _.=`\\
     '|_.=`   __\\
     `\\_..==`` /
      .'.___.-'.
     /          \\
    ('--........._                   
    /'--.....___| |__   ___  ___ ___
    `"--..../ __| '_ \\ / _ \\/ __/ __|
           | (__| | | |  __/\\__ \\__ \\
            \\___|_| |_|\\___||___/___/
'''

FIGURES_ASCII = {
    chess.PAWN: PAWN_FIGURE_ASCII,
    chess.ROOK: ROOK_FIGURE_ASCII,
    chess.KNIGHT: KNIGHT_FIGURE_ASCII,
    chess.BISHOP: BISHOP_FIGURE_ASCII,
    chess.QUEEN: QUEEN_FIGURE_ASCII,
    chess.KING: KING_FIGURE_ASCII,

    chess.piece_symbol(chess.PAWN): PAWN_FIGURE_ASCII,
    chess.piece_symbol(chess.ROOK): ROOK_FIGURE_ASCII,
    chess.piece_symbol(chess.KNIGHT): KNIGHT_FIGURE_ASCII,
    chess.piece_symbol(chess.BISHOP): BISHOP_FIGURE_ASCII,
    chess.piece_symbol(chess.QUEEN): QUEEN_FIGURE_ASCII,
    chess.piece_symbol(chess.KING): KING_FIGURE_ASCII,

    chess.piece_symbol(chess.PAWN).upper(): PAWN_FIGURE_ASCII,
    chess.piece_symbol(chess.ROOK).upper(): ROOK_FIGURE_ASCII,
    chess.piece_symbol(chess.KNIGHT).upper(): KNIGHT_FIGURE_ASCII,
    chess.piece_symbol(chess.BISHOP).upper(): BISHOP_FIGURE_ASCII,
    chess.piece_symbol(chess.QUEEN).upper(): QUEEN_FIGURE_ASCII,
    chess.piece_symbol(chess.KING).upper(): KING_FIGURE_ASCII,
}

SQUARE_WIDTH = 10
SQUARE_HEIGHT = 5

WHITE_FIGURE_COLOR = 'yellow'
BLACK_FIGURE_COLOR = 'magenta'

LOGO_COLOR = 'magenta'
