import pyglet

import resources
from pieces.piece import Piece, WHITE_KING, BLACK_KING
from pieces.rook import Rook


class King(Piece):
    def __init__(self, x, y, type=True):
        super(King, self).__init__(type)
        if self.white:
            self.piece_image = resources.sprite_sheet[WHITE_KING]
        else:
            self.piece_image = resources.sprite_sheet[BLACK_KING]
        self.piece_sprite = pyglet.sprite.Sprite(self.piece_image, x * 75, y * 75)
        self.danger = pyglet.sprite.Sprite(resources.danger_img, x * 75, y * 75)
        self.danger.visible = False  # Add check effect
        self.moved = False

    # Castling
    def change_location(self, x, y, board):
        _castling = None
        if x == self.piece_sprite.x // 75 + 2:  # castling kingside
            board[y][7].change_location(5, y, board)
            board[y][5] = board[y][7]
            board[y][7] = None
            board[y][6] = self
            board[y][4] = None
            _castling = "kingside"
        elif x == self.piece_sprite.x // 75 - 2:  # castling queenside
            board[y][0].change_location(3, y, board)
            board[y][3] = board[y][0]
            board[y][0] = None
            board[y][2] = self
            board[y][4] = None
            _castling = "queenside"
        self.piece_sprite.x = x * 75
        self.piece_sprite.y = y * 75
        self.danger.x = x * 75
        self.danger.y = y * 75
        self.moved = True

        return _castling

    # Check castling
    def check_castling(self, board, right=True):
        y = self.piece_sprite.y // 75
        if right:
            for row in board:
                for piece in row:
                    if piece is not None and piece.white != self.white:
                        valid_moves = piece.get_threat_squares(board)
                        if (y, 5) in valid_moves or (y, 6) in valid_moves or (y, 4) in valid_moves:
                            return False
        else:
            for row in board:
                for piece in row:
                    if piece is not None and piece.white != self.white:
                        valid_moves = piece.get_threat_squares(board)
                        if (y, 4) in valid_moves or (y, 3) in valid_moves or (y, 2) in valid_moves:
                            return False
        return True

    # All possible moves
    def get_threat_squares(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        list_of_moves = []
        try:
            if x > 0 and (board[y + 1][x - 1] is None or self.white != board[y + 1][x - 1].white):
                list_of_moves.append((y + 1, x - 1))
        except IndexError:
            pass
        try:
            if board[y + 1][x] is None or self.white != board[y + 1][x].white:
                list_of_moves.append((y + 1, x))
        except IndexError:
            pass
        try:
            if board[y + 1][x + 1] is None or self.white != board[y + 1][x + 1].white:
                list_of_moves.append((y + 1, x + 1))
        except IndexError:
            pass
        try:
            if board[y][x + 1] is None or self.white != board[y][x + 1].white:
                list_of_moves.append((y, x + 1))
        except IndexError:
            pass
        try:
            if y > 0 and (board[y - 1][x + 1] is None or self.white != board[y - 1][x + 1].white):
                list_of_moves.append((y - 1, x + 1))
        except IndexError:
            pass
        if y > 0 and (board[y - 1][x] is None or self.white != board[y - 1][x].white):
            list_of_moves.append((y - 1, x))
        if y > 0 and x > 0 and (board[y - 1][x - 1] is None or self.white != board[y - 1][x - 1].white):
            list_of_moves.append((y - 1, x - 1))
        if x > 0 and (board[y][x - 1] is None or self.white != board[y][x - 1].white):
            list_of_moves.append((y, x - 1))
        return list_of_moves

    def draw(self):
        self.piece_sprite.draw()
        self.danger.draw()

    # Check if king is in check
    def in_check(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        for row in board:
            for piece in row:
                if piece is not None and piece.white != self.white:
                    valid_moves = piece.get_threat_squares(board)
                    if (y, x) in valid_moves:
                        return True
        return False

    def get_valid_moves(self, board, king):
        y = self.piece_sprite.y // 75
        list_of_moves = self.get_threat_squares(board)  # All possible moves
        valid_moves = []  # All valid moves
        for move in list_of_moves:
            if not self.make_move(board, move, king):
                valid_moves.append(move)
        if not self.moved:
            if type(board[y][7]) is Rook and not board[y][7].moved and board[y][5] is None and board[y][6] is None:
                if self.check_castling(board):
                    valid_moves.append((y, 6))
            if type(board[y][0]) is Rook and not board[y][0].moved and board[y][3] is None and board[y][2] is None and \
                    board[y][1] is None:
                if self.check_castling(board, False):
                    valid_moves.append((y, 2))
        return valid_moves

    # Check if there's possible moves.
    def no_valid_moves(self, board):
        x = self.piece_sprite.x // 75
        y = self.piece_sprite.y // 75
        for row in board:
            for piece in row:
                if piece is not None and piece.white == self.white:
                    valid_moves = piece.get_valid_moves(board, self)
                    if len(valid_moves) > 0:
                        return False
        return True
