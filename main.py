from guiChess import Chess, pyglet


def main():
    my_game = Chess()
    pyglet.clock.schedule_interval(my_game.update, 1 / 60.)
    pyglet.app.run()


if __name__ == '__main__':
    main()
