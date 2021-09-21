# Add id to piece
BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, \
WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN = range(12)


class Piece(object):
    # Attributes
    white = True
    piecesprite = None
    captured = False

    # Constructor
    def __init__(self, type):
        self.white = type
        self.captured = False

    # Manage pieces' moves
    def MakeMove(self, board, move, king):
        x = self.piecesprite.x // 75
        y = self.piecesprite.y // 75
        temp = board[y][x]
        temp2 = board[move[0]][move[1]]
        board[move[0]][move[1]] = board[y][x]
        board[y][x] = None
        self.piecesprite.x = move[1] * 75
        self.piecesprite.y = move[0] * 75
        check = king.InCheck(board)
        board[move[0]][move[1]] = temp2
        board[y][x] = temp
        self.piecesprite.x = x * 75
        self.piecesprite.y = y * 75
        return check

    def GetValidMoves(self, board, king):
        ListOfMoves = self.GetThreatSquares(board)  # All moves possible
        ValidMoves = []  # All valid moves
        for move in ListOfMoves:
            # tempboard = deepcopy(board) Can be optimized. Edit MakeMove function to simply revert any changes
            if not self.MakeMove(board, move, king):
                ValidMoves.append(move)  # Add possible move to list
        return ValidMoves

    # Change piece's graphical position
    def ChangeLocation(self, x, y, board):
        self.piecesprite.x = x * 75
        self.piecesprite.y = y * 75

    # Draw piece on initialization
    def Draw(self):
        self.piecesprite.draw()
