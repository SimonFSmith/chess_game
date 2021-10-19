import pyglet

sprite_image = pyglet.resource.image('resources/spritesheet.png')

sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)

danger_img = pyglet.resource.image('resources/danger.png')

chessboard = pyglet.resource.image('resources/chessboard.png')
valid_img = pyglet.resource.image('resources/validmove.png')
promo_img = pyglet.resource.image('resources/promotion.png')

sprite_image = pyglet.resource.image('resources/spritesheet.png')

sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)

undo_button_black = pyglet.resource.image('resources/undo_button_black.png')
undo_button_press = pyglet.resource.image('resources/undo_button_press.png')
undo_button_hover = pyglet.resource.image('resources/undo_button_hover.png')

add_button_black = pyglet.resource.image('resources/button_add_black.png')
add_button_hover = pyglet.resource.image('resources/button_add_hover.png')
add_button_press = pyglet.resource.image('resources/button_add_press.png')

rules_button_black = pyglet.resource.image('resources/button_rules_black.png')
rules_button_hover = pyglet.resource.image('resources/button_rules_hover.png')
rules_button_press = pyglet.resource.image('resources/button_rules_press.png')

stop_button_black = pyglet.resource.image('resources/stop_button_black.png')
stop_button_hover = pyglet.resource.image('resources/stop_button_hover.png')
stop_button_press = pyglet.resource.image('resources/stop_button_press.png')

about_button_black = pyglet.resource.image('resources/about_button_black.png')
about_button_hover = pyglet.resource.image('resources/about_button_hover.png')
about_button_press = pyglet.resource.image('resources/about_button_press.png')
