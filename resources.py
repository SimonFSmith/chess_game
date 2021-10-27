import pyglet

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

# Scrollbox
custom_center = pyglet.resource.texture('resources/scrollbox/center.png')
custom_top = pyglet.resource.image('resources/scrollbox/bar_top.png')
bar_custom_center = pyglet.resource.texture('resources/scrollbox/bar_vert.png')
custom_bottom = pyglet.resource.image('resources/scrollbox/bar_bottom.png')
custom_base_image = pyglet.resource.image('resources/scrollbox/forward_base.png')
custom_over_image = pyglet.resource.image('resources/scrollbox/forward_over.png')
custom_down_image = pyglet.resource.image('resources/scrollbox/forward_down.png')
back_custom_base_image = pyglet.resource.image('resources/scrollbox/backward_base.png')
back_custom_over_image = pyglet.resource.image('resources/scrollbox/backward_over.png')
back_custom_down_image = pyglet.resource.image('resources/scrollbox/backward_down.png')
custom_base_top = pyglet.resource.image('resources/scrollbox/grip_top_base.png')
custom_base_center = pyglet.resource.texture('resources/scrollbox/grip_vert_base.png')
custom_base_bottom = pyglet.resource.image('resources/scrollbox/grip_bottom_base.png')
custom_over_top = pyglet.resource.image('resources/scrollbox/grip_top_over.png')
custom_over_center = pyglet.resource.texture('resources/scrollbox/grip_vert_over.png')
custom_over_bottom = pyglet.resource.image('resources/scrollbox/grip_bottom_over.png')
custom_down_top = pyglet.resource.image('resources/scrollbox/grip_top_down.png')
custom_down_center = pyglet.resource.texture('resources/scrollbox/grip_vert_down.png')
custom_down_bottom = pyglet.resource.image('resources/scrollbox/grip_bottom_down.png')
