# Add id to piece
BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, \
WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN = range(12)


class Piece(object):
    # Attributes
    white = True
    piece_sprite = None
    captured = False

    # Constructor
    def __init__(self, type):
        self.white = type
        self.captured = False

    # Manage pieces' moves
    def make_move(self, board, move, king):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        temp = board[y][x]
        temp2 = board[move[0]][move[1]]
        board[move[0]][move[1]] = board[y][x]
        board[y][x] = None
        self.piece_sprite.x = move[1] * 75
        self.piece_sprite.y = move[0] * 75
        check = king.in_check(board)
        board[move[0]][move[1]] = temp2
        board[y][x] = temp
        self.piece_sprite.x = x * 75
        self.piece_sprite.y = y * 75
        return check

    def get_valid_moves(self, board, king):
        list_of_moves = self.get_threat_squares(board)  # All moves possible
        valid_moves = []  # All valid moves
        for move in list_of_moves:
            # tempboard = deepcopy(board) Can be optimized. Edit make_move function to simply revert any changes
            if not self.make_move(board, move, king):
                valid_moves.append(move)  # Add possible move to list
        return valid_moves

    # Change piece's graphical position
    def change_location(self, start_x, start_y, board):
        self.piece_sprite.x = start_x * 75
        self.piece_sprite.y = start_y * 75

    # Draw piece on initialization
    def draw(self):
        self.piece_sprite.draw()
