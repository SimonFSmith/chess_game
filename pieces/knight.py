import pyglet

import resources
from pieces.piece import Piece, WHITE_KNIGHT, BLACK_KNIGHT


class Knight(Piece):
    def __init__(self, x, y, type=True):
        super(Knight, self).__init__(type)
        if self.white:
            self.pieceimage = resources.spritesheet[WHITE_KNIGHT]
        else:
            self.pieceimage = resources.spritesheet[BLACK_KNIGHT]
        self.piecesprite = pyglet.sprite.Sprite(self.pieceimage, x * 75, y * 75)

    def GetThreatSquares(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        ListOfMoves = []
        try:
            if board[y + 2][x + 1] is None or self.white != board[y + 2][x + 1].white:
                ListOfMoves.append((y + 2, x + 1))
        except IndexError:
            pass
        try:
            if x > 0 and (board[y + 2][x - 1] is None or self.white != board[y + 2][x - 1].white):
                ListOfMoves.append((y + 2, x - 1))
        except IndexError:
            pass
        try:
            if board[y + 1][x + 2] is None or self.white != board[y + 1][x + 2].white:
                ListOfMoves.append((y + 1, x + 2))
        except IndexError:
            pass
        try:
            if x > 1 and (board[y + 1][x - 2] is None or self.white != board[y + 1][x - 2].white):
                ListOfMoves.append((y + 1, x - 2))
        except IndexError:
            pass
        try:
            if y > 0 and (board[y - 1][x + 2] is None or self.white != board[y - 1][x + 2].white):
                ListOfMoves.append((y - 1, x + 2))
        except IndexError:
            pass
        try:
            if y > 1 and (board[y - 2][x + 1] is None or self.white != board[y - 2][x + 1].white):
                ListOfMoves.append((y - 2, x + 1))
        except IndexError:
            pass
        if x > 1 and y > 0 and (board[y - 1][x - 2] is None or self.white != board[y - 1][x - 2].white):
            ListOfMoves.append((y - 1, x - 2))
        if x > 0 and y > 1 and (board[y - 2][x - 1] is None or self.white != board[y - 2][x - 1].white):
            ListOfMoves.append((y - 2, x - 1))
        return ListOfMoves
