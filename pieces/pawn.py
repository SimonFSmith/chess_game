import pyglet

import resources
from pieces.piece import Piece, WHITE_PAWN, BLACK_PAWN


# Pawn class
class Pawn(Piece):
    # Initialize pawn's image
    def __init__(self, x, y, type=True):
        super(Pawn, self).__init__(type)
        if self.white:
            self.pieceimage = resources.spritesheet[WHITE_PAWN]
        else:
            self.pieceimage = resources.spritesheet[BLACK_PAWN]
        self.piecesprite = pyglet.sprite.Sprite(self.pieceimage, x * 75, y * 75)

    # Calculate possible moves
    def GetThreatSquares(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        ListOfMoves = []
        if self.white and y < 7:
            if board[y + 1][x] is None:
                ListOfMoves.append((y + 1, x))
                if y == 1 and board[y + 2][x] is None:
                    ListOfMoves.append((y + 2, x))
            if x < 7 and board[y + 1][x + 1] is not None and not board[y + 1][x + 1].white:
                ListOfMoves.append((y + 1, x + 1))
            if x > 0 and board[y + 1][x - 1] is not None and not board[y + 1][x - 1].white:
                ListOfMoves.append((y + 1, x - 1))
        elif not self.white and y > 0:
            if board[y - 1][x] is None:
                ListOfMoves.append((y - 1, x))
                if y == 6 and board[y - 2][x] is None:
                    ListOfMoves.append((y - 2, x))
            if x < 7 and board[y - 1][x + 1] is not None and board[y - 1][x + 1].white:
                ListOfMoves.append((y - 1, x + 1))
            if x > 0 and board[y - 1][x - 1] is not None and board[y - 1][x - 1].white:
                ListOfMoves.append((y - 1, x - 1))
        return ListOfMoves
