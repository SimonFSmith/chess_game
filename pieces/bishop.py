import pyglet

import resources
from pieces.piece import Piece, WHITE_BISHOP, BLACK_BISHOP


class Bishop(Piece):
    def __init__(self, x, y, type=True):
        super(Bishop, self).__init__(type)
        if self.white:
            self.piece_image = resources.sprite_sheet[WHITE_BISHOP]
        else:
            self.piece_image = resources.sprite_sheet[BLACK_BISHOP]
        self.piece_sprite = pyglet.sprite.Sprite(self.piece_image, x * 75, y * 75)

    def get_threat_squares(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        list_of_moves = []
        for i in range(1, 8):
            if y - i < 0 or x - i < 0:
                break
            if board[y - i][x - i] is not None:
                if board[y - i][x - i].white != self.white:
                    list_of_moves.append((y - i, x - i))
                break
            list_of_moves.append((y - i, x - i))
        for i in range(1, 8):
            try:
                if board[y + i][x + i] is not None:
                    if board[y + i][x + i].white != self.white:
                        list_of_moves.append((y + i, x + i))
                    break
                list_of_moves.append((y + i, x + i))
            except IndexError:
                break
        for i in range(1, 8):
            try:
                if x - i < 0:
                    break
                if board[y + i][x - i] is not None:
                    if board[y + i][x - i].white != self.white:
                        list_of_moves.append((y + i, x - i))
                    break
                list_of_moves.append((y + i, x - i))
            except IndexError:
                break
        for i in range(1, 8):
            try:
                if y - i < 0:
                    break
                if board[y - i][x + i] is not None:
                    if board[y - i][x + i].white != self.white:
                        list_of_moves.append((y - i, x + i))
                    break
                list_of_moves.append((y - i, x + i))
            except IndexError:
                break
        return list_of_moves
