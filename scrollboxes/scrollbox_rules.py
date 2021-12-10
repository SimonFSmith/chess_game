import glooey

import resources


class ScrollboxRules(glooey.ScrollBox):
    custom_alignment = 'right'
    custom_height_hint = 400
    custom_width_hint = 370



    def __init__(self):
        super(ScrollboxRules, self).__init__()
        self._text = '                      General rules \n \n' + \
                     'The aim in the chess game is \n' +\
                     'delivering a checkmate – trapping \n' +\
                     'your opponent´s king. White is \n' +\
                     'always first to move, and players \n'+ \
                     'take turns alternately moving one \n' +\
                     'piece  at a time. Movement is \n' +\
                     'required.If a player´s turn is \n' +\
                     'to move, he is not in check but has \n' +\
                     'no legal moves, this situation\n' +\
                     'is called “Stalemate” and it ends \n' +\
                     'the game in a draw. Each type of \n' +\
                     'piece has its own method of  \n' +\
                     'movement.A piece may be moved \n' +\
                     'to another position or may capture\n' +\
                     'an opponent´s piece, replacing on \n' +\
                     'its square. Except for the knight,\n' +\
                     'a piece may not move over or\n' +\
                     'through any of the other pieces.\n \n' +\
                     'When a king is threatened with \n' +\
                     'capture(but can protect himself or \n' +\
                     'escape), it´s called check. If a \n' +\
                     'king is in check, then the player\n'+ \
                     'must make a move that eliminates \n' +\
                     'the threat of capture and cannot \n' +\
                     'leave the king in check. Checkmate \n' +\
                     'happens when a king is placed in \n' +\
                     'check and there is no legal move  \n'+ \
                     'to escape. Checkmate ends the game \n' +\
                     'and the side whose king was \n'+\
                     'checkmated looses. \n \n' +\
                     '                  Chess moves \n \n' +\
                     'King can move exactly one square \n' +\
                     'horizontally, vertically, or diagonally. \n' +\
                     'At most once in every game, each king \n' +\
                     'is allowed to make a special move, known \n' +\
                     'as castling. \n' +\
                     'Queen can move any number of vacant \n' +\
                     'squares diagonally, horizontally, or \n' +\
                     'vertically. \n' +\
                     'Rook can move any number of vacant  \n' +\
                     'squares vertically or horizontally. \n' +\
                     'It also is moved while castling. \n' +\
                     'Bishop can move any number of vacant \n' +\
                     'squares in any diagonal direction. \n' +\
                     'Knight can move one square along \n' +\
                     'any rank or file and then at an \n' +\
                     'angle. The knight´s movement can also \n' +\
                     'be viewed as an “L” laid out at any \n' +\
                     'horizontal or vertical angle. \n' +\
                     'Pawns can move forward one square, \n' +\
                     'if that square is unoccupied. If it \n' +\
                     'has not yet moved, the pawn has \n' +\
                     'the option of moving two squares\n' +\
                     'forward provided both squares in \n' +\
                     'front of the pawn are unoccupied. \n' +\
                     'A pawn cannot move backward. Pawns \n' +\
                     'are the only pieces that capture \n' +\
                     'differently from how they move. \n' +\
                     'They can capture an enemy piece \n' +\
                     'on either of the two squares \n' +\
                     'diagonally in front of them but \n' +\
                     'cannot move to these spaces if \n' +\
                     'they are vacant. The pawn is also \n' +\
                     'involved in the two special moves \n' +\
                     'en passant and promotion. \n \n' +\
                     '            Castling \n \n' \
                     'Castling is the only time in the \n' +\
                     'chess game when more than one piece \n' +\
                     'moves during a turn. During the \n' +\
                     'castling, the king moves two squares \n' +\
                     'towards the rook he intends to \n' +\
                     'castle with, and the rook moves \n' +\
                     'to the square through which the \n' +\
                     'king passed. Castling is only \n' +\
                     'permissible if all the following \n' +\
                     'conditions hold: \n' +\
                     'Neither king nor rook involved in \n' +\
                     'castling may have moved from the \n' +\
                     'original position.\n' +\
                     'There must be no pieces between \n' +\
                     'the king and the rook. \n' +\
                     'The king may not currently be in \n' +\
                     'check nor may the king pass  \n' +\
                     'through or end up in a square that \n' +\
                     'is under attack by an enemy piece \n' +\
                     '(though the rook is permitted to \n' +\
                     'be under attack and to pass over \n' +\
                     'an attacked square.) \n \n' +\
                     '             En Passant \n' +\
                     'En Passant may only occur when \n' +\
                     'a pawn is moved two squares on its \n' +\
                     'initial movement. When this \n' +\
                     'happens, the opposing player has \n' +\
                     'the opposing player has the option \n' +\
                     'to take the moved pawn “en passant” \n' +\
                     'as if it had only moved one square \n' +\
                     'This option, though, only stays open \n' +\
                     'for one move \n \n' +\
                     '                Pawn promotion \n' +\
                     'If a pawn reaches the opponent´s edge \n' +\
                     'of the table, it will be promoted \n' +\
                     '– the pawn may be converted to a \n' +\
                     'queen, rook, bishop or knight, as \n' +\
                     'the player desires. The choice is not \n' +\
                     'limited to previously captured pieces.'



        self._label = glooey.Label(self._text)
        self._label.set_color("#000000")
        self._label.set_bold(True)
        self.add(self._label)

    class Frame(glooey.Frame):
        class Decoration(glooey.Background):
            custom_center = resources.custom_center

        class Box(glooey.Bin):
            custom_horz_padding = 2

    class VBar(glooey.VScrollBar):
        custom_scale_grip = True

        class Decoration(glooey.Background):
            custom_top = resources.custom_top
            custom_center = resources.bar_custom_center
            custom_bottom = resources.custom_bottom
            custom_vert_padding = 25

        class Forward(glooey.Button):
            custom_base_image = resources.custom_base_image
            custom_over_image = resources.custom_over_image
            custom_down_image = resources.custom_down_image

        class Backward(glooey.Button):
            custom_base_image = resources.back_custom_base_image
            custom_over_image = resources.back_custom_over_image
            custom_down_image = resources.back_custom_down_image

        class Grip(glooey.Button):
            custom_height_hint = 20
            custom_alignment = 'fill'

            custom_base_top = resources.custom_base_top
            custom_base_center = resources.custom_base_center
            custom_base_bottom = resources.custom_base_bottom

            custom_over_top = resources.custom_over_top
            custom_over_center = resources.custom_over_center
            custom_over_bottom = resources.custom_over_bottom

            custom_down_top = resources.custom_down_top
            custom_down_center = resources.custom_down_center
            custom_down_bottom = resources.custom_down_bottom
