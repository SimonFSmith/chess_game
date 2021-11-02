import pyglet
from pyglet.window import mouse
from pyglet import shapes

import resources
from history import History
from lib.publisher import Publisher
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.piece import Piece


class Chess(pyglet.window.Window):
    # Events
    EVENT_PIECE_MOVED = "EVENT_PIECE_MOVED"
    EVENT_MOVE_UNDONE = "EVENT_MOVE_UNDONE"

    chessboard = resources.chessboard
    valid_img = resources.valid_img
    promo_img = resources.promo_img
    current_pos = (-1, -1)
    move = True  # White if true, Black if false
    promotion = False
    sprite_image = resources.sprite_image
    sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)
    menu_bar = shapes.Rectangle
    # Buttons
    undo_state = resources.undo_button_black
    add_state = resources.add_button_black
    rules_state = resources.rules_button_black
    stop_state = resources.stop_button_hover
    about_state = resources.about_button_black
    undo_x = 605
    undo_y = 90
    add_x = 690
    add_y = 90
    rules_x = 775
    rules_y = 90
    stop_x = 860
    stop_y = 90
    about_x = 945
    about_y = 90

    window_x = 1000
    window_y = 600

    # History
    _history = History()

    def __init__(self):
        # Board is initialized with its screen size.
        super(Chess, self).__init__(self.window_x, self.window_y,
                                    resizable=False,
                                    caption='Chess',
                                    config=pyglet.gl.Config(double_buffer=True),  # Configuration graphique
                                    vsync=False)  # FPS
        self._batch = pyglet.graphics.Batch()
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
        self.menu_bar = shapes.Rectangle(self.chessboard.width, 0, width=(self.window_x - self.chessboard.width), height=150, color=(200, 200, 200))
        self.set_icon(self.sprite_sheet[1])
        self._publisher = Publisher([self.EVENT_PIECE_MOVED, self.EVENT_MOVE_UNDONE])

    def on_draw(self):
        # Board initialization
        self.clear()
        self._batch.draw()
        self.chessboard.blit(0, 0)
        self.menu_bar.draw()
        self.undo_state.blit(self.undo_x, self.undo_y)
        self.add_state.blit(self.add_x, self.add_y)
        self.rules_state.blit(self.rules_x, self.rules_y)
        self.stop_state.blit(self.stop_x, self.stop_y)
        self.about_state.blit(self.about_x, self.about_y)
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
        # Declaring variables for the history
        _start_position_x = -1
        _start_position_y = -1
        _moved_piece = None
        _captured_piece = None
        _end_position_x = 0
        _end_position_y = 0
        _promoted_pawn = None
        _castling = False
        _checkmate = False
        try:
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
                                                                                        self.promo_pawn[0],
                                                                                        not self.move)
                        elif 393.75 < x < 468.75:
                            self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Knight(self.promo_pawn[1],
                                                                                        self.promo_pawn[0],
                                                                                        not self.move)

                        _promoted_pawn = self.board[self.promo_pawn[0]][self.promo_pawn[1]]
                    self.promo_pawn = (-1, -1)
                    self.promotion = False  # Promotion is done so it gets back to False
                    # Checkmate verification after a promotion
                    if not self.move:  # If it's black's turn
                        if self.black_king.no_valid_moves(self.board) and not self.black_king.in_check(
                                self.board):  # If black king can't move but his not in check, there's a stalemate
                            print('Stalemate!')
                        if self.black_king.in_check(self.board):  # If black king is in check
                            self.black_king.danger.visible = True
                            if self.black_king.no_valid_moves(
                                    self.board):  # If black king is in check with no valid moves
                                _checkmate = True
                                print("1-0")
                        if self.white_king.danger.visible:  # If white king danger image is visible
                            if not self.white_king.in_check(self.board):  # If white king is not in check
                                self.white_king.danger.visible = False  # Danger is not display anymore
                    else:  # If it's white's turn
                        if self.white_king.no_valid_moves(self.board) and not self.white_king.in_check(
                                self.board):  # If white king can't move but his not in check, there's a stalemate
                            print('Stalemate!')
                        if self.white_king.in_check(self.board):  # If white king is in check
                            self.white_king.danger.visible = True
                            if self.white_king.no_valid_moves(
                                    self.board):  # If white king is in check with no valid moves
                                _checkmate = True
                                print("0-1")
                        if self.black_king.danger.visible:  # If black king danger image is visible
                            if not self.black_king.in_check(self.board):  # If black king is not in check
                                self.black_king.danger.visible = False  # Danger is not display anymore

                _last_move = self._history.get_move()
                _last_move["promotion"] = _promoted_pawn
                self._history.update_move(_last_move)
                self._publisher.dispatch(self.EVENT_PIECE_MOVED)

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
                            # Saves the captured piece if there is
                            if self.board[board_y][board_x] is not None:
                                _captured_piece = self.board[board_y][board_x]

                            _start_position_x = self.current_pos[1]
                            _start_position_y = self.current_pos[0]
                            self.board[board_y][board_x] = self.board[self.current_pos[0]][self.current_pos[1]]
                            _castling = self.board[self.current_pos[0]][self.current_pos[1]].change_location(board_x,
                                                                                                             board_y,
                                                                                                             self.board)  # Board takes the current position
                            _moved_piece = self.board[board_y][board_x]

                            if type(self.board[self.current_pos[0]][self.current_pos[1]]) is Pawn and (
                                    board_y == 0 or board_y == 7):  # Check if there's a pawn at top or bottom
                                self.promotion = True  # Makes the promotion
                                self.promo_pawn = (board_y, board_x)
                            self.board[self.current_pos[0]][self.current_pos[1]] = None
                            self.current_pos = (-1, -1)  # Goes back to -1, -1 to go back to the if statement
                            # Checkmate verification
                            if self.move:
                                if self.black_king.no_valid_moves(self.board) and not self.black_king.in_check(
                                        self.board):
                                    print('Stalemate!')
                                if self.black_king.in_check(self.board):
                                    self.black_king.danger.visible = True
                                    if self.black_king.no_valid_moves(self.board):
                                        _checkmate = True
                                        print("1-0")
                                if self.white_king.danger.visible:
                                    if not self.white_king.in_check(self.board):
                                        self.white_king.danger.visible = False
                            else:
                                if self.white_king.no_valid_moves(self.board) and not self.white_king.in_check(
                                        self.board):
                                    print('Stalemate!')
                                if self.white_king.in_check(self.board):
                                    self.white_king.danger.visible = True
                                    if self.white_king.no_valid_moves(self.board):
                                        _checkmate = True
                                        print("0-1")
                                if self.black_king.danger.visible:
                                    if not self.black_king.in_check(self.board):
                                        self.black_king.danger.visible = False
                            self.move = not self.move  # Change turn from black to white and white to black
                            for row in self.valid_sprites:
                                for sprite in row:
                                    sprite.visible = False  # Removes the move possibilities

                            # Adds previous move to history
                            self._history.add_move_to_history(not self.move, _moved_piece, _captured_piece,
                                                              _start_position_x, _start_position_y, board_x, board_y,
                                                              _promoted_pawn, _castling,
                                                              self.white_king.danger.visible if self.move else self.black_king.danger.visible,
                                                              _checkmate)
                            if not self.promotion:
                                self._publisher.dispatch(self.EVENT_PIECE_MOVED)
        except IndexError:
            if button == mouse.LEFT:
                # si le button undo est appuyé
                if self.undo_y < y < (self.undo_y + self.undo_state.height):
                    if self.undo_x < x < (self.undo_x + self.undo_state.width):
                        self.change_color_press_undo()
                        self._publisher.dispatch(self.EVENT_MOVE_UNDONE)
                        history_data = History.get_move(self._history)
                        #msgbox(f"Start position: {data['start_position_x']}, {data['start_position_y']}\nEnd position: {data['end_position_x']}, {data['end_position_y']}")
                        Piece.change_location(history_data['piece'],
                                              history_data['start_position_x'],
                                              history_data['start_position_y'],
                                              self.board)
                        #TODO: Remettre le tour à la couleur qui a annulé un déplacement.
                        Piece.make_move(history_data['piece'],
                                        self.board,
                                        self.move,
                                        King.in_check(history_data['piece'], self.board))

                # si le button add est appuyé
                if self.add_y < y < (self.add_y + self.add_state.height):
                    if self.add_x < x < (self.add_x + self.add_state.width):
                        self.change_color_press_add()

                # si le button add est appuyé
                if self.rules_y < y < (self.rules_y + self.rules_state.height):
                    if self.rules_x < x < (self.rules_x + self.rules_state.width):
                        self.change_color_press_rules()

                # si le button stop est appuyé
                if self.stop_y < y < (self.stop_y + self.stop_state.height):
                    if self.stop_x < x < (self.stop_x + self.stop_state.width):
                        self.change_color_press_stop()

                # si le button about est appuyé
                if self.about_y < y < (self.about_y + self.about_state.height):
                    if self.about_x < x < (self.about_x + self.about_state.width):
                        self.change_color_press_about()

    #fonction pour changer l'image du button. nécessaire pour le schedule_once
    def get_history(self):
        return self._history

    def get_batch(self):
        return self._batch

    def get_publisher(self):
        return self._publisher

    # fonction pour changer l'image du button. nécessaire pour le schedule_once
    def update_undo_hover(self, dt):
        self.undo_state = resources.undo_button_hover

    def update_add_hover(self, dt):
        self.add_state = resources.add_button_hover

    def update_rules_hover(self, dt):
        self.rules_state = resources.rules_button_hover
    def update_stop_hover(self, dt):
        self.stop_state = resources.stop_button_hover
    def update_about_hover(self, dt):
        self.about_state = resources.about_button_hover

    # fonction pour changer la couleur du boutton lors d'un clique
    def change_color_press_undo(self):
        self.undo_state = resources.undo_button_press
        pyglet.clock.schedule_once(self.update_undo_hover, 0.17)

    def change_color_press_add(self):
        self.add_state = resources.add_button_press
        pyglet.clock.schedule_once(self.update_add_hover, 0.17)

    def change_color_press_rules(self):
        self.rules_state = resources.rules_button_press
        pyglet.clock.schedule_once(self.update_rules_hover, 0.17)

    # fonction pour détecter si la souris est au dessus d'un boutton
    def change_color_press_stop(self):
        self.stop_state = resources.stop_button_press
        pyglet.clock.schedule_once(self.update_stop_hover, 0.17)

    def change_color_press_about(self):
        self.about_state = resources.about_button_press
        pyglet.clock.schedule_once(self.update_about_hover, 0.17)

    #fonction pour détecter si la souris est au dessus d'un boutton
    def on_mouse_motion(self, x, y, dx, dy):
        # print(x, y, dx, dy)
        # button undo
        if self.undo_x + self.undo_state.width > x > self.undo_x \
                and self.undo_y + self.undo_state.height > y > self.undo_y:
            self.undo_state = resources.undo_button_hover
        else:
            self.undo_state = resources.undo_button_black

        # button add
        if self.add_x + self.add_state.width > x > self.add_x \
                and self.add_y + self.add_state.height > y > self.add_y:
            self.add_state = resources.add_button_hover
        else:
            self.add_state = resources.add_button_black

        # button rules
        if self.rules_x + self.rules_state.width > x > self.rules_x \
                and self.rules_y + self.rules_state.height > y > self.rules_y:
            self.rules_state = resources.rules_button_hover
        else:
            self.rules_state = resources.rules_button_black

        # button stop
        if self.stop_x + self.stop_state.width > x > self.stop_x \
                and self.stop_y + self.stop_state.height > y > self.stop_y:
            self.stop_state = resources.stop_button_hover
        else:
            self.stop_state = resources.stop_button_black

        # button about
        if self.about_x + self.about_state.width > x > self.about_x \
                and self.about_y + self.about_state.height > y > self.about_y:
            self.about_state = resources.about_button_hover
        else:
            self.about_state = resources.about_button_black

    def update(self, dt):
        self.on_draw()
