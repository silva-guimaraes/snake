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
    curses.halfdelay(2)

    SNAKE = '◼'
    BLANK = '.'
    RAT = '🐀'

    screen_height, screen_width = stdsrc.getmaxyx()
    win = curses.newwin(screen_height, screen_width, 0, 0)
    # win.nodelay(True)

    arena_height, arena_width = win.getmaxyx()
    arena_width = arena_width//2 - 1
    arena_height = arena_height-2

    Y, X, HEAD = 0, 1, 0

    def clean_arena():
        return [[BLANK for j in range(arena_width)]
                for i in range(arena_height)]

    startY, startX = arena_height//2+1, arena_width//2
    snake = [[startY, startX], [startY-1, startX], [startY-2, startX],
             [startY-3, startX]]

    def move(new_head_pos, snake):
        return [new_head_pos] + snake[:-1]

    while True:

        arena = clean_arena()

        for body_part in snake:
            arena[body_part[Y]][body_part[X]] = SNAKE

        for i, foo in enumerate(arena):
            for j, icon in enumerate(foo):
                try:
                    win.addstr(i+1, j*2+1, icon + ' ')
                except (curses.error):
                    pass

        win.border()
        head = snake[HEAD]
        win.addstr(0, 2, ' wasd ou hjkl para controlar. ctrl+c para sair.')

        c = win.getch()

        head = snake[HEAD].copy()
        if c == ord('w') or c == ord('k'):
            head[Y] -= 1

        elif c == ord('a') or c == ord('h'):
            head[X] -= 1

        elif c == ord('s') or c == ord('j'):
            head[Y] += 1

        elif c == ord('d') or c == ord('l'):
            head[X] += 1

        else:
            body_part = snake[HEAD+1]
            head[Y] += head[Y] - body_part[Y]
            head[X] += head[X] - body_part[X]

        not_backwards = head != snake[HEAD+1]

        inside_width = head[X] >= 0 and head[X] < arena_width
        inside_height = head[Y] >= 0 and head[Y] < arena_height
        inside_arena = inside_width and inside_height

        if not inside_arena:
            raise Exception("game over")

        if not_backwards:
            snake = move(head, snake)

        win.refresh()
        # time.sleep(.1)


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    sys.exit(0)
