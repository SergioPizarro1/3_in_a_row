import pygame
import sys

# === CONSTANTES ===
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 14
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 12
CROSS_WIDTH = 12
SPACE = SQUARE_SIZE // 4

BG_COLOR = (30, 30, 30)
LINE_COLOR = (255, 255, 255)
CROSS_COLOR = (38, 232, 230)   # Turquoise
CIRCLE_COLOR = (250, 128, 114) # Salmon
WIN_BANNER_COLOR = (255, 255, 255)
FOOTER_COLOR = (180, 180, 180)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tres en Raya")
font_banner = pygame.font.SysFont("arial", 48, bold=True)
font_footer = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()


# === VARIABLES DE JUEGO ===
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
current_player = "X"
game_over = False
winner = None
draw = False

# === FUNCIONES AUXILIARES ===
def draw_grid():
    screen.fill(BG_COLOR)
    # Dibujar líneas horizontales
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Dibujar líneas verticales
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                # Draw two crossing lines for X
                start1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                start2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                end2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

def check_winner():
    global winner, game_over, draw
    # Revisar filas y columnas
    for i in range(BOARD_ROWS):
        # Filas
        if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
            winner = board[i][0]
            game_over = True
            return
        # Columnas
        if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
            winner = board[0][i]
            game_over = True
            return
    # Diagonales
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
        game_over = True
        return
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
        game_over = True
        return
    # Empate
    if all(board[row][col] for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        winner = None
        draw = True
        game_over = True

def restart():
    global board, current_player, game_over, winner, draw
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    current_player = "X"
    game_over = False
    winner = None
    draw = False

def draw_banner():
    if winner:
        text = f"¡{winner} ha ganado!"
    elif draw:
        text = "¡Empate!"
    else:
        return
    banner = font_banner.render(text, True, WIN_BANNER_COLOR)
    banner_rect = banner.get_rect(center=(WIDTH//2, 40))
    screen.blit(banner, banner_rect)

def draw_footer():
    hint = "Pulsa R para reiniciar"
    footer = font_footer.render(hint, True, FOOTER_COLOR)
    footer_rect = footer.get_rect(center=(WIDTH//2, HEIGHT-20))
    screen.blit(footer, footer_rect)

def mouse_to_cell(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < BOARD_COLS and 0 <= row < BOARD_ROWS:
        return row, col
    return None, None

# === MAIN ===
def main():
    global current_player
    running = True

    while running:
        draw_grid()
        draw_figures()
        draw_banner()
        draw_footer()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                row, col = mouse_to_cell(mouse_pos)
                if row is not None and col is not None:
                    if not board[row][col]:
                        board[row][col] = current_player
                        check_winner()
                        if not game_over:
                            current_player = "O" if current_player == "X" else "X"

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()