import pyglet
from pyglet.window import mouse
import Pieces as p


class Chess(pyglet.window.Window):
    chessboard = pyglet.resource.image('resources/chessboard.png')
    validImg = pyglet.resource.image('resources/validmove.png')
    # hoverImg = pyglet.resource.image('resources/hoversquare.png')
    promoImg = pyglet.resource.image('resources/promotion.png')
    currentPos = (-1, -1)
    move = True  # White if true, Black if false
    promotion = False
    spriteimage = pyglet.resource.image('resources/spritesheet.png')
    spritesheet = pyglet.image.ImageGrid(spriteimage, 2, 6)

    def __init__(self):
        # Board is initialized with its screen size.
        super(Chess, self).__init__(600, 600,
                                    resizable=False,
                                    caption='Chess',
                                    config=pyglet.gl.Config(double_buffer=True),  # Configuration graphique
                                    vsync=False)  # FPS
        self.wKing = p.King(4, 0)  # Placement is made from right to left and from bottom to top
        self.bKing = p.King(4, 7, False)  # Type is False is piece is black
        # Pieces are placed on the board, starting from white, then 4 empty lines and black
        self.board = [[p.Rook(0, 0), p.Knight(1, 0), p.Bishop(2, 0), p.Queen(3, 0), self.wKing, p.Bishop(5, 0),
                       p.Knight(6, 0), p.Rook(7, 0)],
                      [p.Pawn(i, 1) for i in range(8)],
                      [None for i in range(8)],
                      [None for i in range(8)],
                      [None for i in range(8)],
                      [None for i in range(8)],
                      [p.Pawn(i, 6, False) for i in range(8)],
                      [p.Rook(0, 7, False), p.Knight(1, 7, False), p.Bishop(2, 7, False), p.Queen(3, 7, False),
                       self.bKing, p.Bishop(5, 7, False), p.Knight(6, 7, False), p.Rook(7, 7, False)]]
        # List containing images of the dot when it's possible to move
        self.validsprites = []
        for i in range(8):
            rowsprites = []
            for j in range(8):
                sprite = pyglet.sprite.Sprite(self.validImg, 75 * j, 75 * i)
                sprite.visible = False
                rowsprites.append(sprite)
            self.validsprites.append(rowsprites)
        # Used during promotion of the pawn to display promotion choices
        self.wQueen = pyglet.sprite.Sprite(self.spritesheet[7], 131.25, 225)
        self.wRook = pyglet.sprite.Sprite(self.spritesheet[10], 218.75, 225)
        self.wBishop = pyglet.sprite.Sprite(self.spritesheet[8], 306.25, 225)
        self.wKnight = pyglet.sprite.Sprite(self.spritesheet[9], 393.75, 225)
        self.bQueen = pyglet.sprite.Sprite(self.spritesheet[1], 131.25, 225)
        self.bRook = pyglet.sprite.Sprite(self.spritesheet[4], 218.75, 225)
        self.bBishop = pyglet.sprite.Sprite(self.spritesheet[2], 306.25, 225)
        self.bKnight = pyglet.sprite.Sprite(self.spritesheet[3], 393.75, 225)


    def on_draw(self):
        # Board initialization
        self.clear()
        self.chessboard.blit(0, 0)
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None: self.board[i][j].Draw()
                self.validsprites[i][j].draw()
        # Display of the promotion rectangle
        if self.promotion:
            self.promoImg.blit(100, 200)
            if self.move:
                self.bQueen.draw()
                self.bRook.draw()
                self.bBishop.draw()
                self.bKnight.draw()
            else:
                self.wQueen.draw()
                self.wRook.draw()
                self.wBishop.draw()
                self.wKnight.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.promotion:  # If there is a promotion
            if button == mouse.LEFT:
                if 225 < y < 300:
                    # A piece is chosen in fonction of where the player clicks
                    if 131.25 < x < 206.25:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = p.Queen(self.promoPawn[1], self.promoPawn[0], not self.move)
                    elif 218.75 < x < 293.75:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = p.Rook(self.promoPawn[1], self.promoPawn[0], not self.move)
                    elif 306.25 < x < 381.25:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = p.Bishop(self.promoPawn[1], self.promoPawn[0], not self.move)
                    elif 393.75 < x < 468.75:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = p.Knight(self.promoPawn[1], self.promoPawn[0], not self.move)
                self.promoPawn = (-1, -1)
                self.promotion = False  # Promotion is done so it gets back to False
                # Checkmate verification after a promotion
                if not self.move:  # If it's black's turn
                    if self.bKing.NoValidMoves(self.board) and not self.bKing.InCheck(self.board):  # If black king can't move but his not in check, there's a stalemate
                        print('Stalemate!')
                    if self.bKing.InCheck(self.board):  # If black king is in check
                        self.bKing.danger.visible = True
                        if self.bKing.NoValidMoves(self.board):  # If black king is in check with no valid moves
                            print("Checkmate! White wins.")
                    if self.wKing.danger.visible:  # If white king danger image is visible
                        if not self.wKing.InCheck(self.board):  # If white king is not in check
                            self.wKing.danger.visible = False  # Danger is not display anymore
                else:  # If it's white's turn
                    if self.wKing.NoValidMoves(self.board) and not self.wKing.InCheck(self.board):  # If white king can't move but his not in check, there's a stalemate
                        print('Stalemate!')
                    if self.wKing.InCheck(self.board):  # If white king is in check
                        self.wKing.danger.visible = True
                        if self.wKing.NoValidMoves(self.board):  # If white king is in check with no valid moves
                            print("Checkmate! Black wins.")
                    if self.bKing.danger.visible:  # If black king danger image is visible
                        if not self.bKing.InCheck(self.board):  # If black king is not in check
                            self.bKing.danger.visible = False  # Danger is not display anymore
        else:  # If there is not promotion
            if button == mouse.LEFT:
                boardX = x//75
                boardY = y//75
                if self.currentPos[0] < 0 and self.currentPos[1] < 0:  # Goes inside because it's initialized with -1, -1
                    if self.board[boardY][boardX] is not None and self.move == self.board[boardY][boardX].white:  # If there's a click from your side
                        self.currentPos = (boardY, boardX)  # Current position becomes the clicked one
                        if self.move:  # If white
                            ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.wKing)  # Put the white's valid move inside the variable
                        else:  # If black
                            ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.bKing)  # Put the blacks's valid move inside the variable
                        if len(ValidMoves) == 0:  # If there's no valid move
                            self.currentPos = (-1, -1)  # Nothing to show, position is reset
                        else:  # If there are possible moves
                            for move in ValidMoves:  # For each move inside the variable
                                self.validsprites[move[0]][move[1]].visible = True  # Display possible moves
                elif self.board[boardY][boardX] is not None and self.move == self.board[boardY][boardX].white:  # If you have a piece selected and you wanna select another one
                    # Remove past move posibilities
                    for row in self.validsprites:
                        for sprite in row:
                            sprite.visible = False
                    self.currentPos = (boardY, boardX)
                    if self.move:  # If it's white
                        ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.wKing)  # Put the white's valid move inside the variable
                    else:  # If it's black
                        ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.bKing)  # Put the blacks's valid move inside the variable
                    if len(ValidMoves) == 0:  # If there's no valid move
                        self.currentPos = (-1, -1)  # Nothing to show, position is reset
                    else:  # If there are possible moves
                        for move in ValidMoves:  # For each move inside the variable
                            self.validsprites[move[0]][move[1]].visible = True  # Display possible moves
                else:  # Making the move
                    if self.validsprites[boardY][boardX].visible:  # If possible moves visible
                        self.board[boardY][boardX] = self.board[self.currentPos[0]][self.currentPos[1]]
                        self.board[self.currentPos[0]][self.currentPos[1]].ChangeLocation(boardX, boardY, self.board)  # Board takes the current position
                        if type(self.board[self.currentPos[0]][self.currentPos[1]]) is p.Pawn and (boardY == 0 or boardY == 7): # Check if there's a pawn at top or bottom
                            self.promotion = True  # Makes the promotion
                            self.promoPawn = (boardY, boardX)
                        self.board[self.currentPos[0]][self.currentPos[1]] = None
                        self.currentPos = (-1, -1)  # Goes back to -1, -1 to go back to the if statement
                        # Checkmate verification
                        if self.move:
                            if self.bKing.NoValidMoves(self.board) and not self.bKing.InCheck(self.board):
                                print('Stalemate!')
                            if self.bKing.InCheck(self.board):
                                self.bKing.danger.visible = True
                                if self.bKing.NoValidMoves(self.board):
                                    print("Checkmate! White wins.")
                            if self.wKing.danger.visible:
                                if not self.wKing.InCheck(self.board):
                                    self.wKing.danger.visible = False
                        else:
                            if self.wKing.NoValidMoves(self.board) and not self.wKing.InCheck(self.board):
                                print('Stalemate!')
                            if self.wKing.InCheck(self.board):
                                self.wKing.danger.visible = True
                                if self.wKing.NoValidMoves(self.board):
                                    print("Checkmate! Black wins.")
                            if self.bKing.danger.visible:
                                if not self.bKing.InCheck(self.board):
                                    self.bKing.danger.visible = False
                        self.move = not self.move  # Change turn from black to white and white to black
                        for row in self.validsprites:
                            for sprite in row:
                                sprite.visible = False  # Removes the move possibilities

    def update(self, dt):
        self.on_draw()