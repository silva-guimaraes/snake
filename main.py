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

    SNAKE = '◼'
    BLANK = '.'
    RAT = '🐀'

    screen_height, screen_width = stdsrc.getmaxyx()
    win = curses.newwin(screen_height, screen_width, 0, 0)
    win.nodelay(True)

    arena_height, arena_width = win.getmaxyx()
    arena_width = arena_width//2 - 1
    arena_height = arena_height-2

    Y, X, HEAD = 0, 1, 0

    def inside_arena(head):
        y = head[Y]
        x = head[X]
        return y >= 0 and y < arena_height and x >= 0 and x < arena_width

    def clean_arena():
        return [[BLANK for j in range(arena_width)]
                for i in range(arena_height)]

    startY, startX = arena_height//2+1, 1
    snake = [[startY, startX], [startY-1, startX], [startY-2, startX],
             [startY-3, startX]]

    def move(new_head_pos, snake):
        return [new_head_pos] + snake[:-1]

    def get_direction(snake):
        head = snake[HEAD]
        body_part = snake[HEAD+1]
        y = head[Y] - body_part[Y]
        x = head[X] - body_part[X]
        return y, x

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
        head = snake[HEAD]
        win.addstr(0, 2, ' wasd ou hjkl para controlar. ctrl+c para sair.')

        c = win.getch()

        if c == ord('w') or c == ord('k'):
            head = snake[HEAD].copy()
            head[Y] -= 1
            if inside_arena(head):
                snake = move(head, snake)

        elif c == ord('a') or c == ord('h'):
            head = snake[HEAD].copy()
            head[X] -= 1
            if inside_arena(head):
                snake = move(head, snake)

        elif c == ord('s') or c == ord('j'):
            head = snake[HEAD].copy()
            head[Y] += 1
            if inside_arena(head):
                snake = move(head, snake)

        elif c == ord('d') or c == ord('l'):
            head = snake[HEAD].copy()
            head[X] += 1
            if inside_arena(head):
                snake = move(head, snake)
        elif c == -1:
            y, x = get_direction(snake)
            head = snake[HEAD].copy()
            head[Y] += y
            head[X] += x
            if inside_arena(head):
                snake = move(head, snake)

        # win.addstr(1, 0, f'arena len: {len(arena)}x{len(arena[0])}')
        # win.addstr(2, 0, f'head: {head[Y]}x{head[X]}')
        win.refresh()
        time.sleep(.1)


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    sys.exit(0)
