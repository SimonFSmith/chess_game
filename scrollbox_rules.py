import glooey

import resources


class ScrollboxRules(glooey.ScrollBox):
    custom_alignment = 'right'
    custom_height_hint = 200

    def __init__(self):
        super(ScrollboxRules, self).__init__()
        self._text = '                                                                    General rules \n \n' + \
                     'The aim in the chess game is delivering a checkmate – trapping your opponent´s king.\n \n' + \
                     'White is always first to move, and players take turns alternately moving one piece at a\n' + \
                     'time. Movement is required. If a player´s turn is to move, he is not in check but has no\n' + \
                     'legal moves, this situation is called “ Stalemate ” and it ends the game in a draw. Each \n' + \
                     'type of piece has its own method of movement. A piece may be moved to another \n' + \
                     'position or may capture an opponent´s  piece, replacing on its square. Except for the \n' + \
                     'knight, a piece may not move over or through any of the other pieces. \n \n' + \
                     'When a king is threatened with capture (but can protect himself or escape), it´s called  \n' + \
                     'check. If a king is in check, then the player must make a move that eliminates the threat\n' + \
                     'of capture and cannot leave the king in check. Checkmate happens when a king is placed \n' + \
                     'in check and there is no legal move to escape. Checkmate ends the game and the side    \n ' + \
                     'whose king was checkmated looses. \n \n' + \
                     '                                                                     Chess moves \n \n' + \
                     'King can move exactly one square horizontally, vertically, or diagonally. At most once in \n' + \
                     'every game, each king is allowed to make a special move, known as castling. \n \n' + \
                     'Queen can move any number of vacant squares diagonally, horizontally, or vertically.\n \n' + \
                     'Bishop can move any number of vacant squares in any diagonal direction. \n \n' + \
                     'Knight can move one square along any rank or file and then at an angle.The knight´s \n' \
                     'movement can also be viewed as an “L” laid out at any horizontal or vertical angle. \n \n' + \
                     'Pawns can move forward one square, if that square is unoccupied. If it has not yet \n' + \
                     'moved, the pawn has the option of moving two squares forward provided both squares \n' + \
                     'in front of the pawn are unoccupied. A pawn cannot move backward. Pawns are the    \n' + \
                     'only pieces that capture differently from how they move. They can capture an enemy  \n' + \
                     'piece on either of the two squares diagonally in front of them but cannot move to  \n' + \
                     'these spaces if they are vacant. The pawn is also involved in the two special moves     \n' + \
                     'en passant and promotion. \n \n ' + \
                     '                                                                       Castling \n \n' + \
                     'Castling is the only time in the chess game when more than one piece moves during \n' + \
                     'a turn. During the castling, the king moves two squares towards the rook he intends\n' + \
                     'to castle with, and the rook moves to the square through which the king passed. \n' + \
                     'Castling is only permissible if all the following conditions hold: \n \n' + \
                     'Neither king nor rook involved in castling may have moved from the original position. \n' + \
                     'There must be no pieces between the king and the rook. The king may not currently   \n' + \
                     'be in check, nor may the king pass through or end up in a square that is under attack    \n ' + \
                     'by an enemy piece (though the rook is permitted to be under attack and to pass over   \n ' + \
                     'an attacked square) \n \n' + \
                     '                                                                       En Passant \n \n' + \
                     'En Passant may only occur when a pawn is moved two squares on its initial movement. \n' + \
                     'When this happens, the opposing player has the option to take the moved pawn “en \n' + \
                     'passant” as if it had only moved one square. This option, though, only stays open for  \n' + \
                     'one move. \n \n' + \
                     '                                                                      Pawn promotion \n \n ' + \
                     'If a pawn reaches the opponent´s edge of the table, it will be promoted – the pawn may be converted \n' + \
                     'to a queen,  rook, bishop or knight, as the player desires. The choice is not limited to previously \n' + \
                     'captured pieces.'

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
