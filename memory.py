import pygame, random

pygame.init()

# ------------ FORMATTING OF FPS
clock = pygame.time.Clock()         

# ------------ CONSTANT VARIABLES
w_width = 800
w_height = 800
w_size = (w_width, w_height)

cell_width = 160
cell_height = 160
cell_size = (cell_width, cell_height)

cell_marginx = 2
cell_marginy = 2

w_paddingx = 74                                 # padding around the grid along the x- and y-axis
w_paddingy = 74

blank_box = pygame.Surface(cell_size)           # creates a blank cell sized surface to color onto

white = (255, 255, 255)
black = (0, 0, 0)
beige = (192, 186, 153)

green = (191, 228, 118)
blue = (154, 206, 223)
teal = (208, 246, 210)
purple = (193, 179, 215)
red = (253, 202, 162)
yellow = (255, 250, 129)
orange = (255, 236, 206)
pink = (253, 222, 238)

colors = [green, blue, teal, purple,
          red, yellow, orange, pink] 
cell_colors = colors + colors               # creates a list with duplicate colors
random.shuffle(cell_colors)                 # shuffles the colors for each play
                                   
indices = []                                # stores a list of the matching cells' indices

guess1 = None                               # stores the first and second guesses
guess2 = None

score = 0
clicked = 0                                 # how many cells has been clicked. maximum of two clicks 

# ------------ WINDOW SETUP
window = pygame.display.set_mode(w_size)
window.fill(beige)
pygame.display.set_caption('Memory Game')

big_font = pygame.font.Font('Nice Sugar.ttf', 40)
small_font = pygame.font.Font('Nice Sugar.ttf', 25)

# ------------ GENERATES THE TITLE ON SCREEN
def game_title():
    title_text = big_font.render('Memory Game', True, white)
    title_rect = title_text.get_rect(center = (w_width//2, 760))
    window.blit(title_text, title_rect)

# ------------ GENERATES THE GRID
def grid():
    grid_matrix = []
    for i in range(4):
        for j in range(4):
            cell = pygame.draw.rect(
                 window,
                 white,
                 ((i * (cell_width + cell_marginx) + w_paddingx), (j * (cell_height + cell_marginy) + w_paddingy), cell_width, cell_height)
                 )
            grid_matrix.append(cell)

    return grid_matrix

# ------------ CHANGES THE CELL COLOR 
def change_cell_color(color, cell):
    global blank_box
    global window

    blank_box.fill(color)
    window.blit(blank_box, cell)
    pygame.display.flip()

# ------------ CHECKS IF THE GUESSES ARE RIGHT OR WRONG
def check_guess(g1, g2, c1, c2):
    global score

    if cell_colors[g1] == cell_colors[g2]:
        score += 1
        pygame.time.delay(500)
        indices.extend((g1, g2))
    else:
        score += 1
        pygame.time.delay(800)
        change_cell_color(white, c1)
        change_cell_color(white, c2)   

# ------------ UPDATES SCORE ON THE SCREEN
def update_score(score):
    coverage_box = pygame.draw.rect(window, beige, (145, 20, 130, 50))
    score_text = small_font.render(f'Turns: {score}', True, white, beige)
    window.blit(score_text, (155, 30))
    pygame.display.update(coverage_box)

# ------------ GENERATES RESTART BUTTON
def restart():
    restart_text = small_font.render('Restart ', True, white)
    restart_rect = pygame.draw.rect(window, beige, (540, 20, 100, 40), 0, 3)
    window.blit(restart_text, (540, 30))
    return restart_rect

# ------------ STARTER BOARD
grid_board = grid()
name = game_title()
restart_game = restart()

# ------------ MAIN GAME LOOP
running = True 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# ------------ GAME LOGIC
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             for i in range(len(grid_board)):
                cell = grid_board[i]
                if cell.collidepoint(event.pos) and clicked==0 and i not in indices:
                    change_cell_color(cell_colors[i], cell)
                    guess1 = i
                    clicked += 1
                    c1 = cell
                if cell.collidepoint(event.pos) and clicked == 1 and i != guess1 and i not in indices:
                    change_cell_color(cell_colors[i], cell)
                    guess2 = i
                    clicked += 1
                    c2 = cell
                if clicked == 2:
                    check_guess(guess1, guess2, c1, c2)  
                    clicked = 0

# ------------ GENERATES THE 'GAME COMPLETED' TEXT
    if len(indices) == len(cell_colors):
        text = big_font.render(f"Game completed in {score} turns!", True, white, beige)
        banner = text.get_rect(center=(w_width // 2, w_height // 2))
        window.blit(text, banner)

# ------------ GENERATES A NEW BOARD WHEN CLICKING RESTART
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if restart_game.collidepoint(event.pos):
            window.fill(beige)
            grid_board = grid()
            restart_game = restart()
            name = game_title()
            random.shuffle(cell_colors)
            indices = []
            score = 0
            clicked = 0
            guess1 = None
            guess2 = None
    
    clock.tick(60)
    update_score(score)
    pygame.display.flip()

pygame.quit()