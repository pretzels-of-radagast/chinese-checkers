import pygame, math

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Chinese(actually german) Checkers')

clock = pygame.time.Clock()

BOARD_WIDTH = 17
BOARD_HEIGHT = 17

board = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2],
         [2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [2, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2],
         [2, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2],
         [2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2],
         [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
         [2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2],
         [2, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2],
         [2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2],
         [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2],
         [2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

sets = [[(4, 4), (5, 4), (6, 4), (7, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (4, 7)],
        [(12, 0), (11, 1), (12, 1), (10, 2), (11, 2), (12, 2), (9, 3), (10, 3), (11, 3), (12, 3)],
        [(13, 4), (14, 4), (15, 4), (16, 4), (13, 5), (14, 5), (15, 5), (13, 6), (14, 6), (13, 7)],
        [(12, 9), (11, 10), (12, 10), (10, 11), (11, 11), (12, 11), (9, 12), (10, 12), (11, 12), (12, 12)],
        [(4, 13), (5, 13), (6, 13), (7, 13), (4, 14), (5, 14), (6, 14), (4, 15), (5, 15), (4, 16)],
        [(3, 9), (2, 10), (3, 10), (1, 11), (2, 11), (3, 11), (0, 12), (1, 12), (2, 12), (3, 12)]]

order_players = [0, 2, 4, 1, 2, 3]
num_players = 3
players = order_players[0:num_players]

containments = []
for i in range(17):
    containments.append([0] * 17)

piece_pos = []

for p in players:
    for s in sets[p]:
        containments[s[1]][s[0]] = p % 3 + 1
        piece_pos.append((s[0], s[1], p % 3 + 1))

selected_piece = -1
selected_piece_pos = (-1, -1, 0)

piece_colors = ((216, 130, 157), (168, 194, 86), (143, 184, 222))
board_color = (243, 217, 177)
hole_color = (194, 153, 121)
black = (80, 59, 49)

TILE_WIDTH = 36  # int(SCREEN_WIDTH / BOARD_WIDTH)
TILE_HEIGHT = int(math.sqrt(TILE_WIDTH ** 2 - (TILE_WIDTH / 2) ** 2))  # int(SCREEN_HEIGHT / BOARD_HEIGHT)
X_OFFSET = TILE_WIDTH / 2  # math.sqrt(TILE_HEIGHT ** 2 - (TILE_HEIGHT / 2) ** 2)

CENTER_OFFSETX = (SCREEN_WIDTH - TILE_WIDTH * 13) / 2
CENTER_OFFSETY = (SCREEN_HEIGHT - TILE_HEIGHT * 17) / 2

l_mouse_down_prev = False
r_mouse_down_prev = False

sign = lambda x: 0 if x == 0 else (1 if x > 1 else -1)

highlight = []

prev_moves = []

turn = 0
win = -1
stepped = False
onestepped = False


def darker(rgb, val=30):
    return max(0, rgb[0] - val), max(0, rgb[1] - val), max(0, rgb[2] - val)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        '''if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                stepped = False'''

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # board_mouse_x = int((mouse_x - (X_OFFSET + CENTER_OFFSETX)) / TILE_WIDTH + 6)
    # board_mouse_y = int((mouse_y - CENTER_OFFSETY) / TILE_HEIGHT)
    board_mouse_y = round(((mouse_y - TILE_HEIGHT / 2) - CENTER_OFFSETY) / TILE_HEIGHT)
    board_mouse_x = round(((mouse_x - TILE_WIDTH / 2) - board_mouse_y * X_OFFSET - CENTER_OFFSETX) / TILE_WIDTH + 6)
    l_mouse_down = pygame.mouse.get_pressed()[0]
    r_mouse_down = pygame.mouse.get_pressed()[2]

    if l_mouse_down and not l_mouse_down_prev:
        if 0 <= board_mouse_y < BOARD_HEIGHT and 0 <= board_mouse_x < BOARD_WIDTH and board[board_mouse_y][
            board_mouse_x] != 2:
            if selected_piece == -1:  # pick new piece
                if containments[board_mouse_y][board_mouse_x] == turn + 1:  # right piece color
                    print('piece select')
                    for i in range(len(piece_pos)):
                        if piece_pos[i][0] == board_mouse_x and piece_pos[i][1] == board_mouse_y:
                            selected_piece = i
                            selected_piece_pos = piece_pos[i]
                            break
                    if selected_piece == -1:
                        print('no piece selected')
            else:
                new_piece = False
                other_piece = False
                for i in range(len(piece_pos)):
                    if not selected_piece_pos == piece_pos[i] and piece_pos[i][0] == board_mouse_x and \
                            piece_pos[i][1] == board_mouse_y:
                        if containments[board_mouse_y][board_mouse_x] == turn + 1:
                            print('new piece select')
                            # reverse old piece
                            if len(prev_moves) > 0:
                                last = prev_moves[0]
                                containments[last[1]][last[0]] = piece_pos[selected_piece][2]
                                containments[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                                piece_pos[selected_piece] = (last[0], last[1], piece_pos[selected_piece][2])
                                selected_piece_pos = (last[0], last[1], piece_pos[selected_piece][2])
                                highlight.clear()

                            # select new piece
                            selected_piece = i
                            selected_piece_pos = piece_pos[i]
                            new_piece = True
                            # break

                            prev_moves.clear()
                        else:
                            other_piece = True

                if not new_piece:
                    if board_mouse_x == selected_piece_pos[0] and board_mouse_y == selected_piece_pos[1]:
                        if stepped:
                            print('piece deselect')
                            # deselect piece
                            selected_piece = -1
                            selected_piece_pos = (-1, -1, 1)
                            prev_moves.clear()
                            # new turn
                            turn = (turn + 1) % num_players
                            stepped = False
                            onestepped = False
                            print(turn)

                    elif not other_piece:
                        xdiff = board_mouse_x - selected_piece_pos[0]
                        ydiff = board_mouse_y - selected_piece_pos[1]
                        print('diff', xdiff, ydiff)

                        if (stepped and max(abs(xdiff), abs(ydiff)) == 1) or onestepped:
                            print('turn should be over')
                        elif xdiff == 0 or ydiff == 0 or ydiff == -xdiff:  # correct pos
                            print('piece place')
                            highlight = []

                            pieces_between = True
                            print('selelcted pos', selected_piece_pos)
                            for i in range(1, max(abs(xdiff), abs(ydiff))):
                                test_pos = (
                                    selected_piece_pos[0] + i * sign(xdiff), selected_piece_pos[1] + i * sign(ydiff))
                                print(i, test_pos, containments[test_pos[1]][test_pos[0]])

                                highlight.append(test_pos)

                                if containments[test_pos[1]][test_pos[0]] == 0:
                                    pieces_between = False
                                    # break

                            if pieces_between:
                                prev_moves.append(selected_piece_pos)

                                containments[board_mouse_y][board_mouse_x] = piece_pos[selected_piece][2]
                                print(piece_pos[selected_piece][2])
                                containments[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                                piece_pos[selected_piece] = (board_mouse_x, board_mouse_y, piece_pos[selected_piece][2])
                                selected_piece_pos = (board_mouse_x, board_mouse_y, piece_pos[selected_piece][2])
                                print('ok')

                                stepped = True
                            else:
                                print('not ok')

                        if max(abs(xdiff), abs(ydiff)) == 0:
                            onestepped = True

    if r_mouse_down and not r_mouse_down_prev:
        if len(prev_moves) > 0:
            last = prev_moves[-1]
            containments[last[1]][last[0]] = piece_pos[selected_piece][2]
            containments[selected_piece_pos[1]][selected_piece_pos[0]] = 0
            piece_pos[selected_piece] = (last[0], last[1], piece_pos[selected_piece][2])
            selected_piece_pos = (last[0], last[1], piece_pos[selected_piece][2])
            print('reverse, reverse!')
            prev_moves.pop()
            highlight.clear()

    l_mouse_down_prev = l_mouse_down
    r_mouse_down_prev = r_mouse_down

    # detect winner
    if win == -1:
        all_filled = True
        check = (order_players[turn] + 3) % 6
        for pos in sets[check]:
            if containments[pos[1]][pos[0]] != turn + 1:
                all_filled = False
                break

        if all_filled:
            win = turn

    screen.fill(board_color)

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            lx = (col - 6) * TILE_WIDTH + row * X_OFFSET + CENTER_OFFSETX
            uy = row * TILE_HEIGHT + CENTER_OFFSETY

            # pygame.draw.rect(screen, colors[board[row][col]], (lx, uy, TILE_WIDTH, TILE_HEIGHT))

            if board[row][col] != 2:
                if (col, row) in highlight:
                    pygame.draw.circle(screen, (255, 0, 0), (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 8)
                if win != -1:
                    pygame.draw.circle(screen, piece_colors[win], (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 4)
                elif row == board_mouse_y and col == board_mouse_x:
                    pygame.draw.circle(screen, darker(hole_color, 50), (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 4)
                else:
                    pygame.draw.circle(screen, hole_color, (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 4)

    for pos in piece_pos:
        lx = (pos[0] - 6) * TILE_WIDTH + pos[1] * X_OFFSET + CENTER_OFFSETX
        uy = pos[1] * TILE_HEIGHT + CENTER_OFFSETY

        # if pos[0:2] in highlight:
        #     pygame.draw.circle(screen, (255, 0, 0), (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 8)
        if pos[1] == board_mouse_y and pos[0] == board_mouse_x:
            pygame.draw.circle(screen, darker(piece_colors[pos[2] - 1]), (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 8)
        else:
            pygame.draw.circle(screen, piece_colors[pos[2] - 1], (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 8)

    if selected_piece != -1:
        # ghost piece
        lx = (board_mouse_x - 6) * TILE_WIDTH + board_mouse_y * X_OFFSET + CENTER_OFFSETX
        uy = board_mouse_y * TILE_HEIGHT + CENTER_OFFSETY

        grad = 8
        gc = pygame.Surface((grad * 2, grad * 2), pygame.SRCALPHA)
        pygame.draw.circle(gc, list(piece_colors[piece_pos[selected_piece][2] - 1]) + [128], (grad, grad), grad)
        screen.blit(gc, (lx + TILE_WIDTH / 2 - grad, uy + TILE_HEIGHT / 2 - grad))

        slx = (selected_piece_pos[0] - 6) * TILE_WIDTH + selected_piece_pos[1] * X_OFFSET + CENTER_OFFSETX
        suy = selected_piece_pos[1] * TILE_HEIGHT + CENTER_OFFSETY

        wrad = 12
        wc = pygame.Surface((wrad * 2, wrad * 2), pygame.SRCALPHA)
        pygame.draw.circle(wc, (255, 255, 255, 128), (wrad, wrad), wrad)
        screen.blit(wc, (slx + TILE_WIDTH / 2 - wrad, suy + TILE_HEIGHT / 2 - wrad))

        # pygame.draw.circle(screen, piece_colors[piece_pos[selected_piece][2] - 1],
        #                    (lx + TILE_WIDTH / 2, uy + TILE_HEIGHT / 2), 8)

    # turn show
    width = 20
    pygame.draw.rect(screen, piece_colors[turn], (0, 0, SCREEN_WIDTH, width))
    pygame.draw.rect(screen, piece_colors[turn], (0, 0, width, SCREEN_HEIGHT))
    pygame.draw.rect(screen, piece_colors[turn], (0, SCREEN_HEIGHT - width, SCREEN_WIDTH, width))
    pygame.draw.rect(screen, piece_colors[turn], (SCREEN_WIDTH - width, 0, width, SCREEN_HEIGHT))

    pygame.display.update()

    clock.tick(60)