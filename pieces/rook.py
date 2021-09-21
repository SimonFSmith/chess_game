import pyglet

import resources
from pieces.piece import Piece, WHITE_ROOK, BLACK_ROOK


class Rook(Piece):
    def __init__(self, x, y, type=True):
        super(Rook, self).__init__(type)
        if self.white:
            self.pieceimage = resources.spritesheet[WHITE_ROOK]
        else:
            self.pieceimage = resources.spritesheet[BLACK_ROOK]
        self.piecesprite = pyglet.sprite.Sprite(self.pieceimage, x * 75, y * 75)
        self.moved = False

    def ChangeLocation(self, x, y, board):
        self.piecesprite.x = x * 75
        self.piecesprite.y = y * 75
        self.moved = True

    def GetThreatSquares(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        ListOfMoves = []
        if y > 0:
            for i in range(y - 1, -1, -1):
                if board[i][x] is not None:
                    if board[i][x].white != self.white:
                        ListOfMoves.append((i, x))
                    break
                ListOfMoves.append((i, x))
        if y < 7:
            for i in range(y + 1, 8):
                if board[i][x] is not None:
                    if board[i][x].white != self.white:
                        ListOfMoves.append((i, x))
                    break
                ListOfMoves.append((i, x))
        if x > 0:
            for i in range(x - 1, -1, -1):
                if board[y][i] is not None:
                    if board[y][i].white != self.white:
                        ListOfMoves.append((y, i))
                    break
                ListOfMoves.append((y, i))
        if x < 7:
            for i in range(x + 1, 8):
                if board[y][i] is not None:
                    if board[y][i].white != self.white:
                        ListOfMoves.append((y, i))
                    break
                ListOfMoves.append((y, i))
        return ListOfMoves
