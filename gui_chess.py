import pyglet
from pyglet.window import mouse

import resources
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook


def position_notation(self):
    position_notation = {"Position": [], "Notation": []}
    for i in range(8):
        for j in range(8):
            position_notation["Position"].append(f"{i}{j}")
            lettre = ""
            if i == 0: lettre = "a"
            elif i == 1: lettre = "b"
            elif i == 2: lettre = "c"
            elif i == 3: lettre = "d"
            elif i == 4: lettre = "e"
            elif i == 5: lettre = "f"
            elif i == 6: lettre = "g"
            elif i == 7: lettre = "h"
            position_notation["Notation"].append(f"{lettre}{j + 1}")
    return position_notation

class Chess(pyglet.window.Window):
    chessboard = resources.chessboard
    valid_img = resources.valid_img
    promo_img = resources.promo_img
    current_pos = (-1, -1)
    move = True  # White if true, Black if false
    promotion = False
    _history = []
    _position_notation = position_notation()

    sprite_image = resources.sprite_image
    sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)

    def __init__(self):
        # Board is initialized with its screen size.
        super(Chess, self).__init__(600, 600,
                                    resizable=False,
                                    caption='Chess',
                                    config=pyglet.gl.Config(double_buffer=True),  # Configuration graphique
                                    vsync=False)  # FPS
        self.white_king = King(4, 0)  # Placement is made from right to left and from bottom to top
        self.black_king = King(4, 7, False)  # Type is False is piece is black
        # Pieces are placed on the board, starting from white, then 4 empty lines and black
        self.board = [[Rook(0, 0), Knight(1, 0), Bishop(2, 0), Queen(3, 0), self.white_king, Bishop(5, 0),
                       Knight(6, 0), Rook(7, 0)],
                      [Pawn(i, 1) for i in range(8)],
                      [None for i in range(8)],
                      [None for i in range(8)],
                      [None for i in range(8)],
                      [None for i in range(8)],
                      [Pawn(i, 6, False) for i in range(8)],
                      [Rook(0, 7, False), Knight(1, 7, False), Bishop(2, 7, False), Queen(3, 7, False),
                       self.black_king, Bishop(5, 7, False), Knight(6, 7, False), Rook(7, 7, False)]]
        # List containing images of the dot when it's possible to move
        self.valid_sprites = []
        for i in range(8):
            row_sprites = []
            for j in range(8):
                sprite = pyglet.sprite.Sprite(self.valid_img, 75 * j, 75 * i)
                sprite.visible = False
                row_sprites.append(sprite)
            self.valid_sprites.append(row_sprites)
        # Used during promotion of the pawn to display promotion choices
        self.white_queen = pyglet.sprite.Sprite(self.sprite_sheet[7], 131.25, 225)
        self.white_rook = pyglet.sprite.Sprite(self.sprite_sheet[10], 218.75, 225)
        self.white_bishop = pyglet.sprite.Sprite(self.sprite_sheet[8], 306.25, 225)
        self.white_knight = pyglet.sprite.Sprite(self.sprite_sheet[9], 393.75, 225)
        self.black_queen = pyglet.sprite.Sprite(self.sprite_sheet[1], 131.25, 225)
        self.black_rook = pyglet.sprite.Sprite(self.sprite_sheet[4], 218.75, 225)
        self.black_bishop = pyglet.sprite.Sprite(self.sprite_sheet[2], 306.25, 225)
        self.black_knight = pyglet.sprite.Sprite(self.sprite_sheet[3], 393.75, 225)

    def on_draw(self):
        # Board initialization
        self.clear()
        self.chessboard.blit(0, 0)
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None: self.board[i][j].draw()
                self.valid_sprites[i][j].draw()
        # Display of the promotion rectangle
        if self.promotion:
            self.promo_img.blit(100, 200)
            if self.move:
                self.black_queen.draw()
                self.black_rook.draw()
                self.black_bishop.draw()
                self.black_knight.draw()
            else:
                self.white_queen.draw()
                self.white_rook.draw()
                self.white_bishop.draw()
                self.white_knight.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.promotion:  # If there is a promotion
            if button == mouse.LEFT:
                if 225 < y < 300:
                    # A piece is chosen in fonction of where the player clicks
                    if 131.25 < x < 206.25:
                        self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Queen(self.promo_pawn[1],
                                                                                   self.promo_pawn[0],
                                                                                   not self.move)
                    elif 218.75 < x < 293.75:
                        self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Rook(self.promo_pawn[1],
                                                                                  self.promo_pawn[0],
                                                                                  not self.move)
                    elif 306.25 < x < 381.25:
                        self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Bishop(self.promo_Pawn[1],
                                                                                    self.promo_pawn[0], not self.move)
                    elif 393.75 < x < 468.75:
                        self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Knight(self.promo_pawn[1],
                                                                                    self.promo_pawn[0], not self.move)
                self.promo_pawn = (-1, -1)
                self.promotion = False  # Promotion is done so it gets back to False
                # Checkmate verification after a promotion
                if not self.move:  # If it's black's turn
                    if self.black_king.no_valid_moves(self.board) and not self.black_king.in_check(
                            self.board):  # If black king can't move but his not in check, there's a stalemate
                        print('Stalemate!')
                    if self.black_king.in_check(self.board):  # If black king is in check
                        self.black_king.danger.visible = True
                        if self.black_king.no_valid_moves(self.board):  # If black king is in check with no valid moves
                            print("Checkmate! White wins.")
                    if self.white_king.danger.visible:  # If white king danger image is visible
                        if not self.white_king.in_check(self.board):  # If white king is not in check
                            self.white_king.danger.visible = False  # Danger is not display anymore
                else:  # If it's white's turn
                    if self.white_king.no_valid_moves(self.board) and not self.white_king.in_check(
                            self.board):  # If white king can't move but his not in check, there's a stalemate
                        print('Stalemate!')
                    if self.white_king.in_check(self.board):  # If white king is in check
                        self.white_king.danger.visible = True
                        if self.white_king.no_valid_moves(self.board):  # If white king is in check with no valid moves
                            print("Checkmate! Black wins.")
                    if self.black_king.danger.visible:  # If black king danger image is visible
                        if not self.black_king.in_check(self.board):  # If black king is not in check
                            self.black_king.danger.visible = False  # Danger is not display anymore
        else:  # If there is not promotion
            if button == mouse.LEFT:
                board_x = x // 75
                board_y = y // 75
                if self.current_pos[0] < 0 and self.current_pos[
                    1] < 0:  # Goes inside because it's initialized with -1, -1
                    if self.board[board_y][board_x] is not None and self.move == self.board[board_y][
                        board_x].white:  # If there's a click from your side
                        self.current_pos = (board_y, board_x)  # Current position becomes the clicked one
                        if self.move:  # If white
                            valid_moves = self.board[board_y][board_x].get_valid_moves(self.board,
                                                                                       self.white_king)  # Put the white's valid move inside the variable
                        else:  # If black
                            valid_moves = self.board[board_y][board_x].get_valid_moves(self.board,
                                                                                       self.black_king)  # Put the blacks's valid move inside the variable
                        if len(valid_moves) == 0:  # If there's no valid move
                            self.current_pos = (-1, -1)  # Nothing to show, position is reset
                        else:  # If there are possible moves
                            for move in valid_moves:  # For each move inside the variable
                                self.valid_sprites[move[0]][move[1]].visible = True  # Display possible moves
                elif self.board[board_y][board_x] is not None and self.move == self.board[board_y][
                    board_x].white:  # If you have a piece selected and you wanna select another one
                    # Remove past move posibilities
                    for row in self.valid_sprites:
                        for sprite in row:
                            sprite.visible = False
                    self.current_pos = (board_y, board_x)
                    if self.move:  # If it's white
                        valid_moves = self.board[board_y][board_x].get_valid_moves(self.board,
                                                                                   self.white_king)  # Put the white's valid move inside the variable
                    else:  # If it's black
                        valid_moves = self.board[board_y][board_x].get_valid_moves(self.board,
                                                                                   self.black_king)  # Put the blacks's valid move inside the variable
                    if len(valid_moves) == 0:  # If there's no valid move
                        self.current_pos = (-1, -1)  # Nothing to show, position is reset
                    else:  # If there are possible moves
                        for move in valid_moves:  # For each move inside the variable
                            self.valid_sprites[move[0]][move[1]].visible = True  # Display possible moves
                else:  # Making the move
                    if self.valid_sprites[board_y][board_x].visible:  # If possible moves visible
                        self.board[board_y][board_x] = self.board[self.current_pos[0]][self.current_pos[1]]
                        self.board[self.current_pos[0]][self.current_pos[1]].change_location(board_x, board_y,
                                                                                             self.board)  # Board takes the current position
                        if type(self.board[self.current_pos[0]][self.current_pos[1]]) is Pawn and (
                                board_y == 0 or board_y == 7):  # Check if there's a pawn at top or bottom
                            self.promotion = True  # Makes the promotion
                            self.promo_pawn = (board_y, board_x)
                        self.board[self.current_pos[0]][self.current_pos[1]] = None
                        self.current_pos = (-1, -1)  # Goes back to -1, -1 to go back to the if statement
                        # Checkmate verification
                        if self.move:
                            if self.black_king.no_valid_moves(self.board) and not self.black_king.in_check(self.board):
                                print('Stalemate!')
                            if self.black_king.in_check(self.board):
                                self.black_king.danger.visible = True
                                if self.black_king.no_valid_moves(self.board):
                                    print("Checkmate! White wins.")
                            if self.white_king.danger.visible:
                                if not self.white_king.in_check(self.board):
                                    self.white_king.danger.visible = False
                        else:
                            if self.white_king.no_valid_moves(self.board) and not self.white_king.in_check(self.board):
                                print('Stalemate!')
                            if self.white_king.in_check(self.board):
                                self.white_king.danger.visible = True
                                if self.white_king.no_valid_moves(self.board):
                                    print("Checkmate! Black wins.")
                            if self.black_king.danger.visible:
                                if not self.black_king.in_check(self.board):
                                    self.black_king.danger.visible = False
                        self.move = not self.move  # Change turn from black to white and white to black
                        for row in self.valid_sprites:
                            for sprite in row:
                                sprite.visible = False  # Removes the move possibilities

                    # Adds previous move to history
                    self.add_move_to_history(self.move,  # Player's turn
                                             self.board[self.current_pos[0]][self.current_pos[1]],  # Piece
                                             board_x, board_y)  # End position
                    print(self.format_move())

    def update(self, dt):
        self.on_draw()

    # Adds move to history
    def add_move_to_history(self, _color, _piece, _position_x, _position_y):
        self._history.append({"color": _color, "piece": _piece, "position_x": _position_x, "position_y": _position_y})

    # Formats move to respect chess notation
    def format_move(self, _index: int = -1):
        _move = self._history[_index]
        _color = "B" if _move["color"] else "W"
        _piece = _move["piece"].__class__.__name__[0]
        _position_x = _move["position_x"]
        _position_y = _move["position_y"]

        return _color + _piece + str(_position_x) + str(_position_y)
