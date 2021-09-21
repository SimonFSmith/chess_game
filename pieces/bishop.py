import pyglet

import resources
from pieces.piece import Piece, WHITE_BISHOP, BLACK_BISHOP


class Bishop(Piece):
    def __init__(self, x, y, type=True):
        super(Bishop, self).__init__(type)
        if self.white:
            self.pieceimage = resources.spritesheet[WHITE_BISHOP]
        else:
            self.pieceimage = resources.spritesheet[BLACK_BISHOP]
        self.piecesprite = pyglet.sprite.Sprite(self.pieceimage, x * 75, y * 75)

    def GetThreatSquares(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        ListOfMoves = []
        for i in range(1, 8):
            if y - i < 0 or x - i < 0:
                break
            if board[y - i][x - i] is not None:
                if board[y - i][x - i].white != self.white:
                    ListOfMoves.append((y - i, x - i))
                break
            ListOfMoves.append((y - i, x - i))
        for i in range(1, 8):
            try:
                if board[y + i][x + i] is not None:
                    if board[y + i][x + i].white != self.white:
                        ListOfMoves.append((y + i, x + i))
                    break
                ListOfMoves.append((y + i, x + i))
            except IndexError:
                break
        for i in range(1, 8):
            try:
                if x - i < 0:
                    break
                if board[y + i][x - i] is not None:
                    if board[y + i][x - i].white != self.white:
                        ListOfMoves.append((y + i, x - i))
                    break
                ListOfMoves.append((y + i, x - i))
            except IndexError:
                break
        for i in range(1, 8):
            try:
                if y - i < 0:
                    break
                if board[y - i][x + i] is not None:
                    if board[y - i][x + i].white != self.white:
                        ListOfMoves.append((y - i, x + i))
                    break
                ListOfMoves.append((y - i, x + i))
            except IndexError:
                break
        return ListOfMoves
