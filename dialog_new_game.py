import glooey

import resources
from lib.publisher import Publisher


class LabelButtonNewGameDialog(glooey.Label):
    custom_font_size = 10
    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True


class TitleNewGameDialog(glooey.Label):
    custom_text = 'Create new game'
    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True


class ButtonNewGameDialog(glooey.Button):
    Foreground = LabelButtonNewGameDialog
    Background = glooey.Image
    custom_base_image = resources.custom_base_image_dialog
    custom_over_image = resources.custom_over_image_dialog
    custom_down_image = resources.custom_down_image_dialog


class DialogNewGame(glooey.ButtonDialog):
    EVENT_BLACK_BUTTON_CLICKED = 'EVENT_BLACK_BUTTON_CLICKED'
    EVENT_WHITE_BUTTON_CLICKED = 'EVENT_WHITE_BUTTON_CLICKED'
    EVENT_DIALOG_CLOSED = 'EVENT_DIALOG_CLOSED'

    def __init__(self, *args, **kwargs):
        super(DialogNewGame, self).__init__(*args, **kwargs)
        self._black_button = self.BlackButtonNewGameDialog()
        self._black_button.push_handlers(on_click=self.on_black_button_click)
        self._white_button = self.WhiteButtonNewGameDialog()
        self._white_button.push_handlers(on_click=self.on_white_button_click)
        self._cancel_button = self.CancelButtonNewGameDialog()
        self._cancel_button.push_handlers(on_click=self.on_cancel_button_click)
        self.get_buttons().add(self._black_button)
        self.get_buttons().add(self._white_button)
        self.get_buttons().add(self._cancel_button)
        self._publisher = Publisher([self.EVENT_BLACK_BUTTON_CLICKED, self.EVENT_WHITE_BUTTON_CLICKED,
                                     self.EVENT_DIALOG_CLOSED])

    def on_black_button_click(self, widget):
        self._publisher.dispatch(self.EVENT_BLACK_BUTTON_CLICKED)
        self.close()

    def on_white_button_click(self, widget):
        self._publisher.dispatch(self.EVENT_WHITE_BUTTON_CLICKED)
        self.close()

    def on_cancel_button_click(self, widget):
        self._publisher.dispatch(self.EVENT_DIALOG_CLOSED)
        self.close()

    def get_publisher(self):
        return self._publisher

    class Decoration(glooey.Background):
        custom_center = resources.custom_center_image_dialog
        custom_top = resources.custom_top_image_dialog
        custom_bottom = resources.custom_bottom_image_dialog
        custom_left = resources.custom_left_image_dialog
        custom_right = resources.custom_right_image_dialog
        custom_top_left = resources.custom_top_left_image_dialog
        custom_top_right = resources.custom_top_right_image_dialog
        custom_bottom_left = resources.custom_bottom_left_image_dialog
        custom_bottom_right = resources.custom_bottom_right_image_dialog

    class Box(glooey.Grid):
        custom_right_padding = 14
        custom_top_padding = 14
        custom_left_padding = 17
        custom_bottom_padding = 17
        custom_cell_padding = 9

    class Button(glooey.HBox):
        custom_cell_padding = 3
        custom_alignment = 'right'

    class BlackButtonNewGameDialog(ButtonNewGameDialog):
        custom_text = 'Black'

    class WhiteButtonNewGameDialog(ButtonNewGameDialog):
        custom_text = 'White'

    class CancelButtonNewGameDialog(ButtonNewGameDialog):
        custom_text = 'Cancel'
