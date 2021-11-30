import glooey
import pyglet
from pyglet import shapes
from pyglet.window import mouse

import resources
from history import History
from lib.publisher import Publisher
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.queen import Queen
from pieces.rook import Rook
from scrollbox import WesnothScrollBox


class Chess(pyglet.window.Window):
    # Events
    EVENT_PIECE_MOVED = "EVENT_PIECE_MOVED"
    EVENT_MOVE_UNDONE = "EVENT_MOVE_UNDONE"
    EVENT_NEW_GAME = 'EVENT_NEW_GAME'
    EVENT_ABOUT_GAME = 'EVENT_ABOUT_GAME'
    EVENT_RULES_GAME = 'EVENT_RULES_GAME'

    chessboard = resources.chessboard
    valid_img = resources.valid_img
    promo_img = resources.promo_img
    sprite_image = resources.sprite_image
    sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)
    menu_bar = shapes.Rectangle
    # Buttons
    undo_state = resources.undo_button_black
    add_state = resources.add_button_black
    rules_state = resources.rules_button_black
    stop_state = resources.stop_button_hover
    about_state = resources.about_button_black
    save_state = resources.save_button_black
    add_x = 650
    add_y = 90
    undo_x = 775
    undo_y = 90
    stop_x = 900
    stop_y = 90
    save_x = 650
    save_y = 25
    rules_x = 775
    rules_y = 25
    about_x = 900
    about_y = 25

    window_x = 1000
    window_y = 600

    def __init__(self):
        # Board is initialized with its screen size.
        super(Chess, self).__init__(self.window_x, self.window_y,
                                    resizable=False,
                                    caption='Chess',
                                    config=pyglet.gl.Config(double_buffer=True),  # Configuration graphique
                                    vsync=False)  # FPS
        self.reset()
        self._block_screen = False
        # Used during promotion of the pawn to display promotion choices
        self.menu_bar = shapes.Rectangle(self.chessboard.width, 0, width=(self.window_x - self.chessboard.width),
                                         height=150, color=(200, 200, 200))
        self.set_icon(self.sprite_sheet[1])
        self._publisher = Publisher([self.EVENT_PIECE_MOVED, self.EVENT_MOVE_UNDONE, self.EVENT_NEW_GAME, self.EVENT_ABOUT_GAME, self.EVENT_RULES_GAME])

    def on_draw(self):
        # Board initialization
        self.clear()
        self._batch.draw()
        # self.chessboard.blit(0, 0)
        self.menu_bar.draw()
        self.undo_state.blit(self.undo_x, self.undo_y)
        self.add_state.blit(self.add_x, self.add_y)
        self.rules_state.blit(self.rules_x, self.rules_y)
        self.stop_state.blit(self.stop_x, self.stop_y)
        self.about_state.blit(self.about_x, self.about_y)
        self.save_state.blit(self.save_x, self.save_y)

        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None: self.board[i][j].draw()
                self.valid_sprites[i][j].draw()
        # Display of the promotion rectangle
        if self.promotion:
            self.promo_img.blit(100, 200)
            if self._move:
                self.black_queen.draw()
                self.black_rook.draw()
                self.black_bishop.draw()
                self.black_knight.draw()
            else:
                self.white_queen.draw()
                self.white_rook.draw()
                self.white_bishop.draw()
                self.white_knight.draw()

    def reset(self, color=True):
        self.current_pos = (-1, -1)
        self.promotion = False
        self._history = History()
        self._can_cancel_last_move = True

        self._batch = pyglet.graphics.Batch()
        self._foreground = pyglet.graphics.OrderedGroup(0)
        self._hud = pyglet.graphics.OrderedGroup(1)
        self.chessboard = pyglet.sprite.Sprite(img=resources.chessboard, x=0, y=0, batch=self._batch,
                                               group=self._foreground)
        self._gui = glooey.Gui(self, batch=self._batch, group=self._hud)
        self._scrollbox = WesnothScrollBox()
        self._gui.add(self._scrollbox)
        if color:
            self._move = True
            self.white_king = King(4, 0)  # Placement is made from right to left and from bottom to top
            self.black_king = King(4, 7, False, False)  # If type is False, piece is black

            # Pieces are placed on the board, starting from white, then 4 empty lines and black
            self.board = [[Rook(0, 0), Knight(1, 0), Bishop(2, 0), Queen(3, 0), self.white_king, Bishop(5, 0),
                           Knight(6, 0), Rook(7, 0)],
                          [Pawn(i, 1) for i in range(8)],
                          [None for i in range(8)],
                          [None for i in range(8)],
                          [None for i in range(8)],
                          [None for i in range(8)],
                          [Pawn(i, 6, False, False) for i in range(8)],
                          [Rook(0, 7, False, False), Knight(1, 7, False, False), Bishop(2, 7, False, False),
                           Queen(3, 7, False, False),
                           self.black_king, Bishop(5, 7, False, False), Knight(6, 7, False, False),
                           Rook(7, 7, False, False)]]

            self.white_queen = pyglet.sprite.Sprite(self.sprite_sheet[7], 131.25, 225, group=self._foreground)
            self.white_rook = pyglet.sprite.Sprite(self.sprite_sheet[10], 218.75, 225, group=self._foreground)
            self.white_bishop = pyglet.sprite.Sprite(self.sprite_sheet[8], 306.25, 225, group=self._foreground)
            self.white_knight = pyglet.sprite.Sprite(self.sprite_sheet[9], 393.75, 225, group=self._foreground)
            self.black_queen = pyglet.sprite.Sprite(self.sprite_sheet[1], 131.25, 225, group=self._foreground)
            self.black_rook = pyglet.sprite.Sprite(self.sprite_sheet[4], 218.75, 225, group=self._foreground)
            self.black_bishop = pyglet.sprite.Sprite(self.sprite_sheet[2], 306.25, 225, group=self._foreground)
            self.black_knight = pyglet.sprite.Sprite(self.sprite_sheet[3], 393.75, 225, group=self._foreground)
        else:
            self._move = False
            self.white_king = King(4, 0, True, False)  # Placement is made from right to left and from bottom to top
            self.black_king = King(4, 7, False, True)  # If type is False, piece is black
            # Pieces are placed on the board, starting from white, then 4 empty lines and black
            self.board = [[Rook(0, 0, True, False), Knight(1, 0, True, False), Bishop(2, 0, True, False),
                           Queen(3, 0, True, False), self.white_king, Bishop(5, 0, True, False),
                           Knight(6, 0, True, False), Rook(7, 0, True, False)],
                          [Pawn(i, 1, True, False) for i in range(8)],
                          [None for i in range(8)],
                          [None for i in range(8)],
                          [None for i in range(8)],
                          [None for i in range(8)],
                          [Pawn(i, 6, False, True) for i in range(8)],
                          [Rook(0, 7, False, True), Knight(1, 7, False, True), Bishop(2, 7, False, True),
                           Queen(3, 7, False, True),
                           self.black_king, Bishop(5, 7, False, True), Knight(6, 7, False, True),
                           Rook(7, 7, False, True)]]

            self.white_queen = pyglet.sprite.Sprite(self.sprite_sheet[1], 131.25, 225, group=self._foreground)
            self.white_rook = pyglet.sprite.Sprite(self.sprite_sheet[4], 218.75, 225, group=self._foreground)
            self.white_bishop = pyglet.sprite.Sprite(self.sprite_sheet[2], 306.25, 225, group=self._foreground)
            self.white_knight = pyglet.sprite.Sprite(self.sprite_sheet[3], 393.75, 225, group=self._foreground)
            self.black_queen = pyglet.sprite.Sprite(self.sprite_sheet[7], 131.25, 225, group=self._foreground)
            self.black_rook = pyglet.sprite.Sprite(self.sprite_sheet[10], 218.75, 225, group=self._foreground)
            self.black_bishop = pyglet.sprite.Sprite(self.sprite_sheet[8], 306.25, 225, group=self._foreground)
            self.black_knight = pyglet.sprite.Sprite(self.sprite_sheet[9], 393.75, 225, group=self._foreground)

        # List containing images of the dot when it's possible to move
        self.valid_sprites = []
        for i in range(8):
            row_sprites = []
            for j in range(8):
                sprite = pyglet.sprite.Sprite(self.valid_img, 75 * j, 75 * i, group=self._foreground)
                sprite.visible = False
                row_sprites.append(sprite)
            self.valid_sprites.append(row_sprites)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self._block_screen:

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
                                                                                           not self._move)
                            elif 218.75 < x < 293.75:
                                self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Rook(self.promo_pawn[1],
                                                                                          self.promo_pawn[0],
                                                                                          not self._move)
                            elif 306.25 < x < 381.25:
                                self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Bishop(self.promo_Pawn[1],
                                                                                            self.promo_pawn[0],
                                                                                            not self._move)
                            elif 393.75 < x < 468.75:
                                self.board[self.promo_pawn[0]][self.promo_pawn[1]] = Knight(self.promo_pawn[1],
                                                                                            self.promo_pawn[0],
                                                                                            not self._move)

                            _promoted_pawn = self.board[self.promo_pawn[0]][self.promo_pawn[1]]
                        self.promo_pawn = (-1, -1)
                        self.promotion = False  # Promotion is done so it gets back to False
                        # Checkmate verification after a promotion
                        if not self._move:  # If it's black's turn
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
                            if self.board[board_y][board_x] is not None and self._move == self.board[board_y][
                                board_x].white:  # If there's a click from your side
                                self.current_pos = (board_y, board_x)  # Current position becomes the clicked one
                                if self._move:  # If white
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
                        elif self.board[board_y][board_x] is not None and self._move == self.board[board_y][
                            board_x].white:  # If you have a piece selected and you wanna select another one
                            # Remove past move posibilities
                            for row in self.valid_sprites:
                                for sprite in row:
                                    sprite.visible = False
                            self.current_pos = (board_y, board_x)
                            if self._move:  # If it's white
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
                                _castling = self.board[self.current_pos[0]][self.current_pos[1]].change_location(
                                    board_x,
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
                                if self._move:
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
                                self._move = not self._move  # Change turn from black to white and white to black
                                for row in self.valid_sprites:
                                    for sprite in row:
                                        sprite.visible = False  # Removes the move possibilities

                                # Adds previous move to history
                                self._history.add_move_to_history(not self._move, _moved_piece, _captured_piece,
                                                                  _start_position_x, _start_position_y, board_x,
                                                                  board_y,
                                                                  _promoted_pawn, _castling,
                                                                  self.white_king.danger.visible if self._move else self.black_king.danger.visible,
                                                                  _checkmate)
                                self._can_cancel_last_move = True
                                if not self.promotion:
                                    self._publisher.dispatch(self.EVENT_PIECE_MOVED)
            except IndexError:
                if button == mouse.LEFT:
                    # if undo button is clicked
                    if self._can_cancel_last_move:
                        if self.undo_y < y < (self.undo_y + self.undo_state.height):
                            if self.undo_x < x < (self.undo_x + self.undo_state.width):
                                if History.get_move(self._history):
                                    self.change_color_press_undo()
                                    history_data = History.get_move(self._history)
                                    # msgbox(f"Start position: {data['start_position_x']}, {data['start_position_y']}\nEnd position: {data['end_position_x']}, {data['end_position_y']}")
                                    Piece.change_location(history_data['piece'],
                                                          history_data['start_position_x'],
                                                          history_data['start_position_y'],
                                                          self.board)
                                    self.cancel_last_move(history_data["color"],
                                                          history_data['piece'],
                                                          history_data['captured_piece'],
                                                          history_data['start_position_x'],
                                                          history_data['start_position_y'],
                                                          history_data['end_position_x'],
                                                          history_data['end_position_y'],
                                                          history_data['castling'],
                                                          history_data['check'],
                                                          self.board)
                                    if self._move:
                                        self._move = False
                                    elif not self._move:
                                        self._move = True
                                    self._publisher.dispatch(self.EVENT_MOVE_UNDONE)

                    # if add button is clicked
                    if self.add_y < y < (self.add_y + self.add_state.height):
                        if self.add_x < x < (self.add_x + self.add_state.width):
                            self.change_color_press_add()
                            self._publisher.dispatch(self.EVENT_NEW_GAME)

                        # if rules button is clicked
                        if self.rules_y < y < (self.rules_y + self.rules_state.height):
                            if self.rules_x < x < (self.rules_x + self.rules_state.width):
                                self.change_color_press_rules()
                                self._publisher.dispatch(self.EVENT_RULES_GAME)

                    # if stop button is clicked
                    if self.stop_y < y < (self.stop_y + self.stop_state.height):
                        if self.stop_x < x < (self.stop_x + self.stop_state.width):
                            self.change_color_press_stop()
                            self.reset()

                    # if about button is clicked
                    if self.about_y < y < (self.about_y + self.about_state.height):
                        if self.about_x < x < (self.about_x + self.about_state.width):
                            self.change_color_press_about()
                            self._publisher.dispatch(self.EVENT_ABOUT_GAME)

                    # if save button is clicked
                    if self.save_y < y < (self.save_y + self.save_state.height):
                        if self.save_x < x < (self.save_x + self.save_state.width):
                            self.save_state = resources.save_button_press
                            pyglet.clock.schedule_once(self.update_save_hover, 0.17)
                            self._history.save_history()
                else:
                    pass

    def get_hud_group(self):
        return self._hud

    def get_gui(self):
        return self._gui

    # fonction pour changer l'image du button. nécessaire pour le schedule_once
    def get_history(self):
        return self._history

    def get_batch(self):
        return self._batch

    def get_publisher(self):
        return self._publisher

    def get_scrollbox(self):
        return self._scrollbox

    def set_move(self, turn):
        self._move = turn

    def set_block_screen(self, block_screen):
        self._block_screen = block_screen

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

    def update_save_hover(self, dt):
        self.save_state = resources.save_button_hover

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

    def cancel_last_move(self, color, piece, captured_piece, start_x, start_y, end_x, end_y, castling, check,
                         board):
        self._can_cancel_last_move = False
        if castling is not None:
            if castling == [castling[0], 7]:  # kingside
                _rook = self.board[castling[0]][5]
                self.board[castling[0]][5] = None
                self.board[castling[0]][castling[1]] = _rook
                _rook.change_location(castling[1], castling[0], board)
                _rook.moved = False
            else:  # queenside
                _rook = self.board[castling[0]][3]
                self.board[castling[0]][3] = None
                self.board[castling[0]][castling[1]] = _rook
                _rook.change_location(castling[1], castling[0], board)
                _rook.moved = False
            if color:
                self.white_king.moved = False
            else:
                self.black_king.moved = False

        if check:
            if color:  # white
                self.black_king.danger.visible = False
            else:  # black
                self.white_king.danger.visible = False

        board[end_y][end_x] = captured_piece
        board[start_y][start_x] = piece

    # fonction pour détecter si la souris est au dessus d'un boutton
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

        # button save
        if self.save_x + self.save_state.width > x > self.save_x \
            and self.save_y + self.save_state.height > y > self.save_y:
            self.save_state = resources.save_button_hover
        else:
            self.save_state = resources.save_button_black

    def update(self, dt):
        self.on_draw()
