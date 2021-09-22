import pyglet

import resources
from pieces.piece import Piece, WHITE_PAWN, BLACK_PAWN


# Pawn class
class Pawn(Piece):
    # Initialize pawn's image
    def __init__(self, x, y, type=True):
        super(Pawn, self).__init__(type)
        if self.white:
            self.piece_image = resources.sprite_sheet[WHITE_PAWN]
        else:
            self.piece_image = resources.sprite_sheet[BLACK_PAWN]
        self.piece_sprite = pyglet.sprite.Sprite(self.piece_image, x * 75, y * 75)

    # Calculate possible moves
    def get_threat_squares(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        list_of_moves = []
        if self.white and y < 7:
            if board[y + 1][x] is None:
                list_of_moves.append((y + 1, x))
                if y == 1 and board[y + 2][x] is None:
                    list_of_moves.append((y + 2, x))
            if x < 7 and board[y + 1][x + 1] is not None and not board[y + 1][x + 1].white:
                list_of_moves.append((y + 1, x + 1))
            if x > 0 and board[y + 1][x - 1] is not None and not board[y + 1][x - 1].white:
                list_of_moves.append((y + 1, x - 1))
        elif not self.white and y > 0:
            if board[y - 1][x] is None:
                list_of_moves.append((y - 1, x))
                if y == 6 and board[y - 2][x] is None:
                    list_of_moves.append((y - 2, x))
            if x < 7 and board[y - 1][x + 1] is not None and board[y - 1][x + 1].white:
                list_of_moves.append((y - 1, x + 1))
            if x > 0 and board[y - 1][x - 1] is not None and board[y - 1][x - 1].white:
                list_of_moves.append((y - 1, x - 1))
        return list_of_moves
