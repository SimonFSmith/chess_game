import pyglet

import resources
from pieces.piece import Piece, WHITE_KNIGHT, BLACK_KNIGHT


class Knight(Piece):
    def __init__(self, x, y, type=True):
        super(Knight, self).__init__(type)
        if self.white:
            self.piece_image = resources.spritesheet[WHITE_KNIGHT]
        else:
            self.piece_image = resources.spritesheet[BLACK_KNIGHT]
        self.piece_sprite = pyglet.sprite.Sprite(self.piece_image, x * 75, y * 75)

    def get_threat_squares(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        list_of_moves = []
        try:
            if board[y + 2][x + 1] is None or self.white != board[y + 2][x + 1].white:
                list_of_moves.append((y + 2, x + 1))
        except IndexError:
            pass
        try:
            if x > 0 and (board[y + 2][x - 1] is None or self.white != board[y + 2][x - 1].white):
                list_of_moves.append((y + 2, x - 1))
        except IndexError:
            pass
        try:
            if board[y + 1][x + 2] is None or self.white != board[y + 1][x + 2].white:
                list_of_moves.append((y + 1, x + 2))
        except IndexError:
            pass
        try:
            if x > 1 and (board[y + 1][x - 2] is None or self.white != board[y + 1][x - 2].white):
                list_of_moves.append((y + 1, x - 2))
        except IndexError:
            pass
        try:
            if y > 0 and (board[y - 1][x + 2] is None or self.white != board[y - 1][x + 2].white):
                list_of_moves.append((y - 1, x + 2))
        except IndexError:
            pass
        try:
            if y > 1 and (board[y - 2][x + 1] is None or self.white != board[y - 2][x + 1].white):
                list_of_moves.append((y - 2, x + 1))
        except IndexError:
            pass
        if x > 1 and y > 0 and (board[y - 1][x - 2] is None or self.white != board[y - 1][x - 2].white):
            list_of_moves.append((y - 1, x - 2))
        if x > 0 and y > 1 and (board[y - 2][x - 1] is None or self.white != board[y - 2][x - 1].white):
            list_of_moves.append((y - 2, x - 1))
        return list_of_moves
