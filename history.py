from pieces.knight import Knight
import datetime
import os

class History:
    def __init__(self):
        self._history = []
        self._keys = []
        self._values = []
        self._squares_name = self.create_notations(self._keys, self._values)

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
        try:
            return self._history[_index]
        except IndexError:
            return ""

    # Updates move
    def update_move(self, _updated_move, _index: int = -1):
        self._history[_index] = _updated_move

    def delete_move(self, _index: int = -1):
        self._history.pop(_index)

    # Formats move to respect algebraic notation
    def format_move(self, _index: int = -1):
        _move = self._history[_index]
        _str = ""

        if _move["castling"] is not None:  # If castling
            _str += "0-0" if _move["castling"][1] == 7 else "0-0-0"
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

    def save_history(self):
        dt = datetime.datetime.now()
        if not os.path.exists('game_history'):
            os.makedirs('game_history')
        with open(f"game_history/{dt.today().strftime('%b-%d-%Y-%H-%M-%S')}.txt", "w") as stream:
            for i in range(len(self._history)):
                stream.write(self.format_move(i) + ("\n" if i != len(self._history) - 1 else ""))


    def clear_history(self):
        self._history.clear()

    # Creates a dictionary of squares name
    def create_notations(self, keys, values):
        for i in range(10):
            for j in range(8):
                keys.append(f'{i}{j}')

        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            for j in range(1, 9):
                values.append(f'{i}{j}')

        _position_notation = dict(zip(keys, values))
        return _position_notation
