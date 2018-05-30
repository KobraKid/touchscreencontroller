import pygame
import common

# screen size constants
# top-left = 0, 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
# Actual screen
screen = None
myfont = None


def init_pygame():
    # Set up Pygame for testing button locations
    global screen, myfont
    global SCREEN_WIDTH, SCREEN_HEIGHT
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 40)
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 127))
    # Letters
    pygame.draw.circle(screen, (0, 255, 0), (common.buttons["a"][common.ID.X], common.buttons["a"][common.ID.Y]), 20)
    label = myfont.render("A", 1, (255, 0, 255))
    screen.blit(label, (common.buttons["a"][common.ID.X] - 12, common.buttons["a"][common.ID.Y] - 20))
    pygame.draw.circle(screen, (255, 0, 0), (common.buttons["b"][common.ID.X], common.buttons["b"][common.ID.Y]), 20)
    label = myfont.render("B", 1, (0, 255, 255))
    screen.blit(label, (common.buttons["b"][common.ID.X] - 12, common.buttons["b"][common.ID.Y] - 20))
    pygame.draw.circle(screen, (0, 0, 255), (common.buttons["x"][common.ID.X], common.buttons["x"][common.ID.Y]), 20)
    label = myfont.render("X", 1, (255, 255, 0))
    screen.blit(label, (common.buttons["x"][common.ID.X] - 12, common.buttons["x"][common.ID.Y] - 20))
    pygame.draw.circle(screen, (255, 255, 0), (common.buttons["y"][common.ID.X], common.buttons["y"][common.ID.Y]), 20)
    label = myfont.render("Y", 1, (0, 0, 255))
    screen.blit(label, (common.buttons["y"][common.ID.X] - 12, common.buttons["y"][common.ID.Y] - 20))
    # Arrows
    pygame.draw.rect(screen, (0, 255, 0), (common.buttons["up arrow"][common.ID.X],
                                           common.buttons["up arrow"][common.ID.Y],
                                           common.buttons["up arrow"][common.ID.WIDTH],
                                           common.buttons["up arrow"][common.ID.HEIGHT]))
    label = myfont.render("↑", 1, (255, 0, 255))
    screen.blit(label, (common.buttons["up arrow"][common.ID.X] + 10, common.buttons["up arrow"][common.ID.Y]))
    pygame.draw.rect(screen, (255, 0, 0), (common.buttons["down arrow"][common.ID.X],
                                           common.buttons["down arrow"][common.ID.Y],
                                           common.buttons["down arrow"][common.ID.WIDTH],
                                           common.buttons["down arrow"][common.ID.HEIGHT]))
    label = myfont.render("↓", 1, (0, 255, 255))
    screen.blit(label, (common.buttons["down arrow"][common.ID.X] + 10, common.buttons["down arrow"][common.ID.Y]))
    pygame.draw.rect(screen, (0, 0, 255), (common.buttons["left arrow"][common.ID.X],
                                           common.buttons["left arrow"][common.ID.Y],
                                           common.buttons["left arrow"][common.ID.WIDTH],
                                           common.buttons["left arrow"][common.ID.HEIGHT]))
    label = myfont.render("←", 1, (255, 255, 0))
    screen.blit(label, (common.buttons["left arrow"][common.ID.X] + 10, common.buttons["left arrow"][common.ID.Y]))
    pygame.draw.rect(screen, (255, 255, 0), (common.buttons["right arrow"][common.ID.X],
                                             common.buttons["right arrow"][common.ID.Y],
                                             common.buttons["right arrow"][common.ID.WIDTH],
                                             common.buttons["right arrow"][common.ID.HEIGHT]))
    label = myfont.render("→", 1, (0, 0, 255))
    screen.blit(label, (common.buttons["right arrow"][common.ID.X] + 10, common.buttons["right arrow"][common.ID.Y]))
    # Home button
    pygame.draw.rect(screen, (255, 255, 255), (common.buttons["esc"][common.ID.X],
                                               common.buttons["esc"][common.ID.Y],
                                               common.buttons["esc"][common.ID.WIDTH],
                                               common.buttons["esc"][common.ID.HEIGHT]))
    label = myfont.render("⌂", 1, (0, 0, 0))
    screen.blit(label, (common.buttons["esc"][common.ID.X] + 13, common.buttons["esc"][common.ID.Y] - 4))
    # Keypress label
    pygame.draw.circle(screen, (255, 255, 255), (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)), 20)
    key_label = myfont.render("X", 1, (0, 0, 0))
    screen.blit(key_label, (int(SCREEN_WIDTH / 2) - 12, int(SCREEN_HEIGHT / 2) - 20))
    pygame.display.update()


def update_screen():
    global screen, myfont
    for evt in pygame.event.get():
        if evt.type == pygame.KEYDOWN:
            pygame.draw.circle(screen, (255, 255, 255), (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)), 20)
            key_label = myfont.render(str(evt.unicode), 1, (0, 0, 0))
            screen.blit(key_label, (int(SCREEN_WIDTH / 2) - 12, int(SCREEN_HEIGHT / 2) - 20))
            pygame.display.update()
