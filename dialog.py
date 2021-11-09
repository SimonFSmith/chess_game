import glooey
import pyglet

import resources
from lib.publisher import Publisher


class WesnothLabel(glooey.Label):
    custom_font_size = 10
    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True

class WesnothTitle(glooey.Label):
    custom_text = 'Create new game'
    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True




class WesnothButton(glooey.Button):
    Foreground = WesnothLabel
    Background = glooey.Image
    custom_base_image = resources.custom_base_image_dialog
    custom_over_image = resources.custom_over_image_dialog
    custom_down_image = resources.custom_down_image_dialog
    # custom_white_king = 'resource/button/'


class WesnothDialog(glooey.ButtonDialog):
    EVENT_BLACK_BUTTON_CLICKED = 'EVENT_BLACK_BUTTON_CLICKED'
    EVENT_WHITE_BUTTON_CLICKED = 'EVENT_WHITE_BUTTON_CLICKED'
    EVENT_DIALOG_CLOSED = 'EVENT_DIALOG_CLOSED'


    def __init__(self, *args, **kwargs):
        super(WesnothDialog, self).__init__(*args, **kwargs)
        self._black_button = self.BlackButton()
        self._black_button.push_handlers(on_click=self.on_black_button_click)
        self._white_button = self.WhiteButton()
        self._white_button.push_handlers(on_click=self.on_white_button_click)
        self._cancel_button = self.CancelButton()
        self._cancel_button.push_handlers(on_click=self.on_cancel_button_click)
        self.get_buttons().add(self._black_button)
        self.get_buttons().add(self._white_button)
        self.get_buttons().add(self._cancel_button)
        self._publisher = Publisher([self.EVENT_BLACK_BUTTON_CLICKED, self.EVENT_WHITE_BUTTON_CLICKED,
                                     self.EVENT_DIALOG_CLOSED])

    def on_get_label_appeared(self, widget):
        self._publisher.dispatch(self.EVENT_TITLE_APPEARED)



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
        custom_center = pyglet.resource.texture('resources/dialog/center.png')
        custom_top = pyglet.resource.texture('resources/dialog/top.png')
        custom_bottom = pyglet.resource.texture('resources/dialog/bottom.png')
        custom_left = pyglet.resource.texture('resources/dialog/left.png')
        custom_right = pyglet.resource.texture('resources/dialog/right.png')
        custom_top_left = pyglet.resource.image('resources/dialog/top_left.png')
        custom_top_right = pyglet.resource.image('resources/dialog/top_right.png')
        custom_bottom_left = pyglet.resource.image('resources/dialog/bottom_left.png')
        custom_bottom_right = pyglet.resource.image('resources/dialog/bottom_right.png')

    class Box(glooey.Grid):
        custom_right_padding = 14
        custom_top_padding = 14
        custom_left_padding = 17
        custom_bottom_padding = 17
        custom_cell_padding = 9

    class Buttons(glooey.HBox):
        custom_cell_padding = 3
        custom_alignment = 'right'

    class BlackButton(WesnothButton):
        custom_text = 'Black'

    class WhiteButton(WesnothButton):
        custom_text = 'White'

    class CancelButton(WesnothButton):
        custom_text = 'Cancel'




