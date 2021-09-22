import pyglet

import resources
from pieces.piece import Piece, WHITE_ROOK, BLACK_ROOK


class Rook(Piece):
    def __init__(self, x, y, type=True):
        super(Rook, self).__init__(type)
        if self.white:
            self.piece_image = resources.sprite_sheet[WHITE_ROOK]
        else:
            self.piece_image = resources.sprite_sheet[BLACK_ROOK]
        self.piece_sprite = pyglet.sprite.Sprite(self.piece_image, x * 75, y * 75)
        self.moved = False

    def change_location(self, x, y, board):
        self.piece_sprite.x = x * 75
        self.piece_sprite.y = y * 75
        self.moved = True

    def get_threat_squares(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        list_of_moves = []
        if y > 0:
            for i in range(y - 1, -1, -1):
                if board[i][x] is not None:
                    if board[i][x].white != self.white:
                        list_of_moves.append((i, x))
                    break
                list_of_moves.append((i, x))
        if y < 7:
            for i in range(y + 1, 8):
                if board[i][x] is not None:
                    if board[i][x].white != self.white:
                        list_of_moves.append((i, x))
                    break
                list_of_moves.append((i, x))
        if x > 0:
            for i in range(x - 1, -1, -1):
                if board[y][i] is not None:
                    if board[y][i].white != self.white:
                        list_of_moves.append((y, i))
                    break
                list_of_moves.append((y, i))
        if x < 7:
            for i in range(x + 1, 8):
                if board[y][i] is not None:
                    if board[y][i].white != self.white:
                        list_of_moves.append((y, i))
                    break
                list_of_moves.append((y, i))
        return list_of_moves
