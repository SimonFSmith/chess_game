import glooey

import resources
from lib.publisher import Publisher


class TitleAboutDialog(glooey.Label):
    custom_text = "About"
    custom_font_size = 10
    custom_color = '#000000'
    custom_alignment = 'left'
    custom_bold = True


class ContentAboutDialog(glooey.Label):
    custom_color = '#000000'
    custom_alignment = 'center'
    custom_bold = True
    custom_text = '          Project manager / Programmer \n                  ' +\
                  'Simon Fournier-Smith \n  \n ' \
                  + '                      Programmers              ' \
                  + '\n                         Benoit Côté' + '\n                         ' \
                                              'Félix Poirier' \
                  + '\n                    Samuel Legendre   ' \
                  + '\n  \n            Based on the chess project of \n          ' \
                  + '           Fahad Ahmed Kan  \n \n        ' \
                  + '        Find the project on GitHub \n' \
                  + 'https://github.com/SimonFSmith/chess_game \n '



class ButtonAboutDialog(glooey.Button):
    Foreground = ContentAboutDialog
    Background = glooey.Image
    custom_base_image = resources.custom_base_image_dialog
    custom_over_image = resources.custom_over_image_dialog
    custom_down_image = resources.custom_down_image_dialog


class DialogAbout(glooey.ButtonDialog):
    EVENT_CANCEL_BUTTON = "EVENT_CANCEL_BUTTON"
    custom_alignment = "top right"
    custom_height_hint = 450
    custom_width_hint = 400


    def __init__(self, *args, **kwargs):
        super(DialogAbout, self).__init__(*args, **kwargs)

        self._cancel_button = self.CancelButtonAboutDialog()
        self._cancel_button.push_handlers(on_click=self.on_cancel_button_click)
        self.get_buttons().add(self._cancel_button)

        self._publisher = Publisher([self.EVENT_CANCEL_BUTTON])

    def on_cancel_button_click(self, widget):
        self._publisher.dispatch(self.EVENT_CANCEL_BUTTON)
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

    class CancelButtonAboutDialog(ButtonAboutDialog):
        custom_text = 'Close'
