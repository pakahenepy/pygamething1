import pygame


# constants
FPS = 60

WINDOW_CAPTION = "pygamething1"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_PADDING = 20

FONT_SIZE = 72

PADDLE_WIDTH = 50
PADDLE_HEIGHT = 20
PADDLE_COLOR = (250, 0, 0)
PADDLE_SPAWN = (300, 500)

BALL_SIZE = 20
BALL_VELOCITY = [10, 10]
BALL_COLOR = (250, 250, 0)
BALL_SPAWN = (150, 150)

BRICK_HEIGHT = 30
BRICK_ROWS = 3
BRICK_COLUMNS = 10
BRICK_PADDING = 10
BRICK_BASE_COLOR = (0, 255, 0)
BRICK_GRADIENT = 5  # 0 means all colors are the same, anything higher affects how much of gradient there will be
MAX_BRICK_BRIGHTNESS = 255  # 0-255, 0 means black, 255 means white


# methods
def create_bricks():
    bricks = []

    # brick width is scaled to the width of the window
    # add an extra column to add padding on the sides
    brick_width = (WINDOW_WIDTH - ((BRICK_COLUMNS + 1) * BRICK_PADDING)) / BRICK_COLUMNS

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            # calculate the position of the brick, accounting for padding
            pos_x = BRICK_PADDING + (col * (brick_width + BRICK_PADDING))
            pos_y = BRICK_PADDING + (row * (BRICK_HEIGHT + BRICK_PADDING))
            brick = pygame.Rect(pos_x, pos_y, brick_width, BRICK_HEIGHT)
            bricks.append(brick)
    return bricks


def get_brick_color(i):
    # brick color can be a function of i, we just need to write some formula for it
    # lets do something linear, y=mx+b for example
    # y = our rgb values
    # m, b are just arbitrary values, choose whatever
    b = 0
    value = i * BRICK_GRADIENT + b

    r = min(max(0, BRICK_BASE_COLOR[0] + value), MAX_BRICK_BRIGHTNESS)
    g = min(max(0, BRICK_BASE_COLOR[1] + value), MAX_BRICK_BRIGHTNESS)
    b = min(max(0, BRICK_BASE_COLOR[2] + value), MAX_BRICK_BRIGHTNESS)

    return (r, g, b)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_CAPTION)

    # set up sprites and other variables
    font = pygame.font.SysFont(None, FONT_SIZE)
    bricks = create_bricks()

    paddle_rect = pygame.Rect(*PADDLE_SPAWN, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(*BALL_SPAWN, BALL_SIZE, BALL_SIZE)

    gameover = False
    clock = pygame.time.Clock()

    # game loop starts here
    while not gameover:
        clock.tick(FPS)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                gameover = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameover = True
                # other key events here that happen ONCE when you press

        # keys that you can hold down:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            paddle_rect[0] += 5
        elif keys[pygame.K_LEFT]:
            paddle_rect[0] -= 5

        # actions that happen every cycle
        # move stuff
        ball_rect[0] += BALL_VELOCITY[0]
        ball_rect[1] += BALL_VELOCITY[1]

        if ball_rect[1] > WINDOW_HEIGHT - WINDOW_PADDING:
            BALL_VELOCITY[1] = -5
        if ball_rect[0] > WINDOW_WIDTH - WINDOW_PADDING:
            BALL_VELOCITY[0] = -5
        if ball_rect[1] < WINDOW_PADDING:
            BALL_VELOCITY[1] = 5
        if ball_rect[0] < WINDOW_PADDING:
            BALL_VELOCITY[0] = 5

        # handle collisions
        if paddle_rect.colliderect(ball_rect):
            BALL_VELOCITY[1] *= -1
            # add paddle off ball sound

        for brick in bricks.copy():
            if ball_rect.colliderect(brick):
                bricks.remove(brick)
                BALL_VELOCITY[1] *= -1
                # add ball of brick sound

        # clear the screen
        screen.fill((0, 0, 0))

        # draw stuff
        # ORDER MATTERS, things drawn before will appear below things draw after
        # we want score on top of game elements.
        pygame.draw.ellipse(screen, BALL_COLOR, ball_rect)
        pygame.draw.rect(screen, PADDLE_COLOR, paddle_rect)

        for i in range(len(bricks)):
            pygame.draw.rect(screen, get_brick_color(i), bricks[i])

        score_text = font.render(str(len(bricks)), True, (250, 250, 0))
        screen.blit(score_text, (700, 10))

        # show the new screen (60x per second).
        pygame.display.flip()

    pygame.quit()


# app entry
if __name__ == "__main__":
    main()
