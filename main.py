import glooey

from gui_chess import Chess, pyglet
from scrollbox import WesnothScrollBox

_my_game = Chess()
_gui = glooey.Gui(_my_game, batch=_my_game.get_batch())

_scrollbox = WesnothScrollBox()
_gui.add(_scrollbox)


def _add_last_move_to_scrollbox():
    _scrollbox.update_label_text(_my_game.get_history().format_move())


def _delete_last_move():
    _scrollbox.delete_label_last_line()
    _my_game.get_history().delete_move()


_my_game.get_publisher().register(_my_game.EVENT_PIECE_MOVED, "main", _add_last_move_to_scrollbox)
_my_game.get_publisher().register(_my_game.EVENT_MOVE_UNDONE, "main", _delete_last_move)

pyglet.clock.schedule_interval(_my_game.update, 1 / 60)
pyglet.app.run()
