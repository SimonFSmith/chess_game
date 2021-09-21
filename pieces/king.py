import pyglet

import resources
from pieces.piece import Piece, WHITE_KING, BLACK_KING
from pieces.rook import Rook


class King(Piece):
    def __init__(self, x, y, type=True):
        super(King, self).__init__(type)
        if self.white:
            self.pieceimage = resources.spritesheet[WHITE_KING]
        else:
            self.pieceimage = resources.spritesheet[BLACK_KING]
        self.piecesprite = pyglet.sprite.Sprite(self.pieceimage, x * 75, y * 75)
        self.danger = pyglet.sprite.Sprite(resources.dangerImg, x * 75, y * 75)
        self.danger.visible = False  # Add check effect
        self.moved = False

    def ChangeLocation(self, x, y, board):
        if x == self.piecesprite.x // 75 + 2:
            board[y][7].ChangeLocation(5, y, board)
            board[y][5] = board[y][7]
            board[y][7] = None
            board[y][6] = self
            board[y][4] = None
        elif x == self.piecesprite.x // 75 - 2:
            board[y][0].ChangeLocation(3, y, board)
            board[y][3] = board[y][0]
            board[y][0] = None
            board[y][2] = self
            board[y][4] = None
        self.piecesprite.x = x * 75
        self.piecesprite.y = y * 75
        self.danger.x = x * 75
        self.danger.y = y * 75
        self.moved = True

    # Check castling
    def CheckCastling(self, board, right=True):
        y = self.piecesprite.y // 75
        if right:
            for row in board:
                for piece in row:
                    if piece is not None and piece.white != self.white:
                        ValidMoves = piece.GetThreatSquares(board)
                        if (y, 5) in ValidMoves or (y, 6) in ValidMoves or (y, 4) in ValidMoves:
                            return False
        else:
            for row in board:
                for piece in row:
                    if piece is not None and piece.white != self.white:
                        ValidMoves = piece.GetThreatSquares(board)
                        if (y, 4) in ValidMoves or (y, 3) in ValidMoves or (y, 2) in ValidMoves:
                            return False
        return True

    # All possible moves
    def GetThreatSquares(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        ListOfMoves = []
        try:
            if x > 0 and (board[y + 1][x - 1] is None or self.white != board[y + 1][x - 1].white):
                ListOfMoves.append((y + 1, x - 1))
        except IndexError:
            pass
        try:
            if board[y + 1][x] is None or self.white != board[y + 1][x].white:
                ListOfMoves.append((y + 1, x))
        except IndexError:
            pass
        try:
            if board[y + 1][x + 1] is None or self.white != board[y + 1][x + 1].white:
                ListOfMoves.append((y + 1, x + 1))
        except IndexError:
            pass
        try:
            if board[y][x + 1] is None or self.white != board[y][x + 1].white:
                ListOfMoves.append((y, x + 1))
        except IndexError:
            pass
        try:
            if y > 0 and (board[y - 1][x + 1] is None or self.white != board[y - 1][x + 1].white):
                ListOfMoves.append((y - 1, x + 1))
        except IndexError:
            pass
        if y > 0 and (board[y - 1][x] is None or self.white != board[y - 1][x].white):
            ListOfMoves.append((y - 1, x))
        if y > 0 and x > 0 and (board[y - 1][x - 1] is None or self.white != board[y - 1][x - 1].white):
            ListOfMoves.append((y - 1, x - 1))
        if x > 0 and (board[y][x - 1] is None or self.white != board[y][x - 1].white):
            ListOfMoves.append((y, x - 1))
        return ListOfMoves

    def Draw(self):
        self.piecesprite.draw()
        self.danger.draw()

    # Check if king is in check
    def InCheck(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        for row in board:
            for piece in row:
                if piece is not None and piece.white != self.white:
                    validmoves = piece.GetThreatSquares(board)
                    if (y, x) in validmoves:
                        return True
        return False

    def GetValidMoves(self, board, king):
        y = self.piecesprite.y // 75
        ListOfMoves = self.GetThreatSquares(board)  # All possible moves
        ValidMoves = []  # All valid moves
        for move in ListOfMoves:
            if not self.MakeMove(board, move, king):
                ValidMoves.append(move)
        if not self.moved:
            if type(board[y][7]) is Rook and not board[y][7].moved and board[y][5] is None and board[y][6] is None:
                if self.CheckCastling(board):
                    ValidMoves.append((y, 6))
            if type(board[y][0]) is Rook and not board[y][0].moved and board[y][3] is None and board[y][2] is None and \
                    board[y][1] is None:
                if self.CheckCastling(board, False):
                    ValidMoves.append((y, 2))
        return ValidMoves

    # Check if there's possible moves.
    def NoValidMoves(self, board):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        for row in board:
            for piece in row:
                if piece is not None and piece.white == self.white:
                    validmoves = piece.GetValidMoves(board, self)
                    if len(validmoves) > 0:
                        return False
        return True
