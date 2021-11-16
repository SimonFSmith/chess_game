import glooey

import resources


class WesnothScrollBox(glooey.ScrollBox):
    custom_alignment = 'right'
    custom_height_hint = 200

    def __init__(self):
        super(WesnothScrollBox, self).__init__()

        self._text = "​"
        self._label = glooey.Label(self._text)
        self._label.set_color("#000000")
        self._label.set_bold(True)
        self.new_label()

    def new_label(self):
        self.clear()
        self.add(self._label)

    def update_label_text(self, text):
        self._text += "{}\n".format(text)
        self._label.set_text(self._text)

    def delete_label_last_line(self):
        _split_text = self._text.rsplit("\n", 2)

        if _split_text[0] == "​" or _split_text[1] == "":
            self._text = "​"
        else:
            self._text = _split_text[0] + "\n"

        self._label.set_text(self._text)

    def clear_label(self):
        self._text = "​"
        self._label.set_text(self._text)
        self.new_label()

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
