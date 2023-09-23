import random
import sys
import curses


# "Cyclomatic complexity too high"
# ???
def main(stdsrc):
    # curses
    curses.noecho()
    curses.cbreak()
    stdsrc.keypad(True)
    stdsrc.scrollok(0)
    curses.curs_set(0)
    curses.halfdelay(2)

    SNAKE = '◼'
    BLANK = '.'
    RAT = '🐀'

    start = False
    # criar window principal
    screen_height, screen_width = stdsrc.getmaxyx()
    win = curses.newwin(screen_height, screen_width, 0, 0)

    arena_height, arena_width = win.getmaxyx()
    # caracteres em terminais comuns são retangulares.
    # visualmente isso é ruim para o nosso jogo já que isso faz
    # com que a cobra pareça se mover mais rápido na vertical.
    # a solução pra isso é adicionar um espaço entre cada coluna de
    # caracteres e para isso é necessário remover metade das colunas
    arena_width = arena_width//2 - 1
    arena_height = arena_height-2
    # lembrando que arena é só um pouquinho menor do que a window principal
    # por isso devemos remover uma margem pequena

    Y, X, HEAD = 0, 1, 0

    # posicionar cobra
    startY, startX = arena_height//2+1, arena_width//2
    snake = [[startY, startX], [startY-1, startX], [startY-2, startX],
             [startY-3, startX]]
    # posições validas pra na hora de calcular onde spawnar um novo ratinho
    VALID_POSITIONS = [[y, x] for x in range(arena_width)
                       for y in range(arena_height)]

    def clear_arena():
        return [[BLANK for j in range(arena_width)]
                for i in range(arena_height)]

    # faz a cobra rastejar
    def move(new_head_pos, snake):
        return [new_head_pos] + snake[:-1]

    def random_rat():
        # todas as posições validas menos as posições onde a cobra esta
        valid_positions = [i for i in VALID_POSITIONS if i not in snake]
        if len(valid_positions) == 0:
            raise Exception("vitória!")
        return valid_positions[random.randint(0, len(valid_positions)-1)]

    # nosso ratinho
    rat = random_rat()

    while True:

        arena = clear_arena()

        arena[rat[Y]][rat[X]] = RAT
        for body_part in snake:
            arena[body_part[Y]][body_part[X]] = SNAKE

        for i, foo in enumerate(arena):
            for j, icon in enumerate(foo):
                try:
                    # vezes dois cria os espaços entre as colunas
                    win.addstr(i+1, j*2+1, icon + ' ')
                except (curses.error):
                    pass

        win.border()
        win.addstr(0, 2, ' wasd ou hjkl para controlar. ctrl+c para sair.')
        pontos = f' pontos: {len(snake)-4} '
        win.addstr(0, screen_width - len(pontos) - 1, pontos)

        c = win.getch()

        if c != -1:
            start = True
        if not start:
            continue

        # movimentação

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

        # verificar se movimento é permitido

        not_backwards = head != snake[HEAD+1]

        inside_width = head[X] >= 0 and head[X] < arena_width
        inside_height = head[Y] >= 0 and head[Y] < arena_height
        inside_arena = inside_width and inside_height

        self_collision = any(head == body_part for body_part in snake[2:])

        if not inside_arena or self_collision:
            raise Exception("game over ┐(´ー｀)┌. Pontos: " + str(len(snake)-4))

        if not_backwards:
            snake = move(head, snake)

        # cobra encontrou o ratinho
        if head == rat:
            rat = random_rat()
            snake = snake + [snake[-1]]

        win.refresh()


try:
    curses.wrapper(main)
except KeyboardInterrupt:
    sys.exit(0)
