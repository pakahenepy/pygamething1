import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Demo Game")

#set up sprites and other variables
font = pygame.font.SysFont(None, 72)
brick_color = (250, 50, 0)
bricks = []
for row in range(3):
  for col in range(5):
    brick = pygame.Rect(col * 80 + 10, row * +60, 60, 20)
    bricks.append(brick)
paddle_rect = pygame.Rect(300,500,50,20)
paddle_color = (250,0,0)

ball_rect = pygame.Rect(150,150,20,20)
ball_color = (250,250,0)

ball_velocity = [10,10] 

gameover = False
clock = pygame.time.Clock()

#game loop starts here
while not gameover:2
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameover = True
            #other key events here that happen ONCE when you press


                
    #keys that you can hold down:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        paddle_rect[0] += 5
    elif keys[pygame.K_LEFT]:
      paddle_rect[0] -= 5
    #actions that happen automatically.               
    #move stuff
    ball_rect [1] += ball_velocity [1]
    ball_rect [0] += ball_velocity [0]
    if ball_rect[1] > 580:
      ball_velocity[1] = -5
    
    if ball_rect[0] > 780:
      ball_velocity[0] = -5
    if ball_rect[1] < 0:
      ball_velocity[1] = +5
    if ball_rect[0] < 0:
      ball_velocity[0] = 5
    
    #handle collisions
    if paddle_rect.colliderect(ball_rect):
      ball_velocity[1] *= -1
    for brick in bricks.copy():
      if ball_rect.colliderect(brick):
        bricks.remove(brick)
        ball_velocity[1] *= -1
    #clear the screen
    screen.fill((0,0,0))
    
    #draw stuff
    score_text = font.render(str(len(bricks)), True, (250,250,0))
    screen.blit(score_text, (700,10))
    pygame.draw.ellipse(screen, ball_color, ball_rect)
    pygame.draw.rect(screen, paddle_color, paddle_rect)
    for brick in bricks:
      pygame.draw.rect(screen, brick_color, brick)
    #show the new screen (60x per second).
    pygame.display.flip()

pygame.quit()
    
