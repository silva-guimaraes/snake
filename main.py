# import os
import time
import sys
import curses


def main(stdsrc):
    curses.noecho()
    curses.cbreak()
    stdsrc.keypad(True)
    stdsrc.scrollok(0)
    curses.curs_set(0)

    SNAKE = '▆'
    BLANK = '.'
    RAT = '🐀'

    screen_height, screen_width = stdsrc.getmaxyx()
    win = curses.newwin(screen_height, screen_width, 0, 0)
    win.nodelay(True)

    arena_height, arena_width = win.getmaxyx()
    arena_width = arena_width//2 - 1
    arena_height = arena_height-2

    def inside_arena(y, x):
        return y >= 0 and y < arena_height and x >= 0 and x < arena_width

    def clean_arena():
        return [[BLANK for j in range(arena_width)]
                for i in range(arena_height)]

    startY, startX = arena_height//2+1, 1
    snake = [[startY, startX], [startY-1, startX], [startY-2, startX]]
    Y, X, HEAD = 0, 1, 0

    while True:

        arena = clean_arena()

        for body_part in snake:
            arena[body_part[Y]][body_part[X]] = SNAKE

        for i, foo in enumerate(arena):
            for j, bar in enumerate(foo):
                try:
                    win.addstr(i+1, j*2+1, arena[i][j] + ' ')
                except (curses.error):
                    pass
        win.border()
        c = win.getch()

        head = snake[HEAD]
        if c == ord('w') or c == ord('k'):
            if inside_arena(head[Y] - 1, head[X]):
                snake[0][Y] -= 1

        elif c == ord('a') or c == ord('h'):
            if inside_arena(head[Y], head[X] - 1):
                snake[0][X] -= 1

        elif c == ord('s') or c == ord('j'):
            if inside_arena(head[Y] + 1, head[X]):
                snake[0][Y] += 1

        elif c == ord('d') or c == ord('l'):
            if inside_arena(head[Y], head[X] + 1):
                snake[0][X] += 1

        win.addstr(0, 0, 'wasd ou hjkl para controlar. ctrl+c para sair.')
        win.addstr(1, 0, f'arena len: {len(arena)}x{len(arena[0])}')
        win.addstr(2, 0, f'head: {head[Y]}x{head[X]}')
        win.refresh()
        time.sleep(.01)


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    sys.exit(0)
