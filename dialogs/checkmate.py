import glooey

import resources
from lib.publisher import Publisher


class CheckMateLabel(glooey.Label):
    custom_font_size = 10
    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True


class CheckmateTitleDialog(glooey.Label):
    custom_text = 'Checkmate'

    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True


class CheckmateDialog(glooey.Button):
    Foreground = CheckMateLabel
    Background = glooey.Image
    custom_base_image = resources.custom_base_image_dialog
    custom_over_image = resources.custom_over_image_dialog
    custom_down_image = resources.custom_down_image_dialog


class DialogCheckmate(glooey.ButtonDialog):
    EVENT_DIALOG_CLOSED = 'EVENT_DIALOG_CLOSED'

    def __init__(self, *args, **kwargs):
        super(DialogCheckmate, self).__init__(*args, **kwargs)
        self._cancel_button = self.CancelButtonCheckmateDialog()
        self._cancel_button.push_handlers(on_click=self.on_cancel_button_click)
        self.get_buttons().add(self._cancel_button)
        self._publisher = Publisher([self.EVENT_DIALOG_CLOSED])


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


    class CancelButtonCheckmateDialog(CheckmateDialog):
        custom_text = 'Cancel'
