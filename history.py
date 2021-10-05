from pieces.knight import Knight


class History:
    def __init__(self):
        self._history = []
        self._squares_name = {'00': 'a1', '01': 'a2', '02': 'a3', '03': 'a4', '04': 'a5', '05': 'a6', '06': 'a7',
                              '07': 'a8', '10': 'b1', '11': 'b2', '12': 'b3', '13': 'b4', '14': 'b5', '15': 'b6',
                              '16': 'b7', '17': 'b8', '20': 'c1', '21': 'c2', '22': 'c3', '23': 'c4', '24': 'c5',
                              '25': 'c6', '26': 'c7', '27': 'c8', '30': 'd1', '31': 'd2', '32': 'd3', '33': 'd4',
                              '34': 'd5', '35': 'd6', '36': 'd7', '37': 'd8', '40': 'e1', '41': 'e2', '42': 'e3',
                              '43': 'e4', '44': 'e5', '45': 'e6', '46': 'e7', '47': 'e8', '50': 'f1', '51': 'f2',
                              '52': 'f3', '53': 'f4', '54': 'f5', '55': 'f6', '56': 'f7', '57': 'f8', '60': 'g1',
                              '61': 'g2', '62': 'g3', '63': 'g4', '64': 'g5', '65': 'g6', '66': 'g7', '67': 'g8',
                              '70': 'h1', '71': 'h2', '72': 'h3', '73': 'h4', '74': 'h5', '75': 'h6', '76': 'h7',
                              '77': 'h8'}

    # Adds move to history
    def add_move_to_history(self, _color, _piece, _captured_piece, _start_position_x, _start_position_y,
                            _end_position_x, _end_position_y, _promotion, _castling, _check, _checkmate):
        self._history.append(
            {"color": _color, "piece": _piece, "captured_piece": _captured_piece, "start_position_x": _start_position_x,
             "start_position_y": _start_position_y, "end_position_x": _end_position_x,
             "end_position_y": _end_position_y, "promotion": _promotion, "castling": _castling, "check": _check,
             "checkmate": _checkmate})

    # Gets move from history
    def get_move(self, _index: int = -1):
        return self._history[_index]

    # Updates move
    def update_move(self, _updated_move, _index: int = -1):
        self._history[_index] = _updated_move

    # Formats move to respect algebraic notation
    def format_move(self, _index: int = -1):
        _move = self._history[_index]
        _str = ""

        if _move["castling"] is not None:  # If castling
            _str += "0-0" if _move["castling"] == "kingside" else "0-0-0"
        else:  # If not
            if _move["promotion"] is None:
                _str += _move["piece"].__class__.__name__[1].upper() if isinstance(_move["piece"], Knight) else \
                    _move["piece"].__class__.__name__[0]  # Moved piece

            if _move["captured_piece"] is not None:
                _str += "x"  # Captures notation

            _str += self._squares_name[str(_move["end_position_x"]) + str(_move["end_position_y"])]  # End position

            if _move["promotion"] is not None:
                _str += _move["promotion"].__class__.__name__[1].upper() if isinstance(_move["promotion"], Knight) else \
                    _move["promotion"].__class__.__name__[0]  # Promoted piece

            if _move["check"] and not _move["checkmate"]:
                _str += "+"  # Check notation

            if _move["checkmate"]:
                _str += "#"  # Checkmate notation

        return _str
