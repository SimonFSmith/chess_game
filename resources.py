import pyglet

sprite_image = pyglet.resource.image('resources/spritesheet.png')

sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)

danger_img = pyglet.resource.image('resources/danger.png')

chessboard = pyglet.resource.image('resources/chessboard.png')
valid_img = pyglet.resource.image('resources/validmove.png')
promo_img = pyglet.resource.image('resources/promotion.png')

sprite_image = pyglet.resource.image('resources/spritesheet.png')

sprite_sheet = pyglet.image.ImageGrid(sprite_image, 2, 6)

undo_noir = pyglet.resource.image('resources/undo_noir.png')
undo_vert = pyglet.resource.image('resources/undo_vert.png')
undo_release = pyglet.resource.image('resources/undo_release.png')
undo_hover = pyglet.resource.image('resources/undo_hover.png')
