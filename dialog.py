import glooey
import pyglet


class WesnothLabel(glooey.Label):
    custom_font_name = 'Lato Regular'
    custom_font_size = 10
    custom_color = '#b9ad86'
    custom_alignment = 'center'


class WesnothButton(glooey.Button):
    Foreground = WesnothLabel
    Background = glooey.Image
    custom_base_image = pyglet.resource.image('resources/dialog/base.png')
    custom_over_image = pyglet.resource.image('resources/dialog/over.png')
    custom_down_image = pyglet.resource.image('resources/dialog/down.png')


class WesnothDialog(glooey.YesNoDialog):
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

    class YesButton(WesnothButton):
        custom_text = 'Ok'

    class NoButton(WesnothButton):
        custom_text = 'Cancel'
