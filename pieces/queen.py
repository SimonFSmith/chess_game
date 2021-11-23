import pyglet

import resources
from pieces.piece import Piece, WHITE_QUEEN, BLACK_QUEEN


class Queen(Piece):
    def __init__(self, x, y, type=True, visually_white=True):
        super(Queen, self).__init__(type, visually_white)
        if self.visually_white:
            self.piece_image = resources.sprite_sheet[WHITE_QUEEN]
        else:
            self.piece_image = resources.sprite_sheet[BLACK_QUEEN]
        self.piece_sprite = pyglet.sprite.Sprite(self.piece_image, x * 75, y * 75)

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
