import pygame
from random import randrange


def game():
    pygame.init()
    width, height = 1200, 800
    fps = 60
    width_w = 200
    height_h = 25
    speed = 7
    game_over = False
    n = True
    rect = pygame.Rect(width // 2 - width_w // 2, height - height_h, width_w, height_h)
    pygame.display.set_caption('Retroid')
    sc = pygame.display.set_mode([width, height])
    clock = pygame.time.Clock()
    color_ball = randrange(0, 256), randrange(0, 256), randrange(0, 256)
    color_rect = randrange(0, 256), randrange(0, 256), randrange(0, 256)
    radius = 10
    ball_rect = int(radius * 2 ** 0.5)
    ball = pygame.Rect(randrange(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    g_list = [pygame.Rect(60 * i, 35 * j, 50, 30) for i in range(20) for j in range(8)]
    color = [(randrange(0, 256), randrange(0, 256), randrange(0, 256)) for i in range(20) for j in range(8)]
    font = pygame.font.SysFont('Arial', 30, bold=True).render('Game Over!', False, pygame.Color("red"))
    sound = pygame.mixer.Sound("Sounds/blast.mp3")
    sound1 = pygame.mixer.Sound("Sounds/collide.mp3")
    sound2 = pygame.mixer.Sound("Sounds/gameover.mp3")
    bg = pygame.image.load("img/space.jpg")

    def detect(dx, dy, rect, ball):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top
        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    while True:
        sc.fill("black")
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
        sc.blit(bg, (0, 0))
        [pygame.draw.rect(sc, color[clr], block) for clr, block in enumerate(g_list)]
        pygame.draw.rect(sc, color_rect, rect)
        pygame.draw.circle(sc, color_ball, ball.center, radius)
        if not game_over:
            ball.x += speed * dx
            ball.y += speed * dy
        if ball.centerx < radius or ball.centerx > width - radius:
            dx = -dx
        if ball.centery < radius:
            dy = -dy
        if ball.centery > height - radius:
            game_over = True
            while n:
                pygame.mixer.Sound.play(sound2, 0)
                n = False
        if game_over:
            sc.blit(font, (550, 350))
        if ball.colliderect(rect) and dy > 0:
            dx, dy = detect(dx, dy, ball, rect)
            pygame.mixer.Sound.play(sound1, 0)
        hit_list = ball.collidelist(g_list)
        if hit_list != -1:
            hit_rect = g_list.pop(hit_list)
            hit_color = color.pop(hit_list)
            dx, dy = detect(dx, dy, ball, hit_rect)
            pygame.draw.rect(sc, hit_color, hit_rect)
            pygame.mixer.Sound.play(sound, 0)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] and rect.x >= 0) and not game_over:
            rect.x -= speed * 2.5
        if (keys[pygame.K_d] and rect.x <= width - width_w) and not game_over:
            rect.x += speed * 2.5
        if keys[pygame.K_SPACE] and game_over:
            game()
        if len(g_list) <= 0:
            pygame.time.delay(1000)
            game()
        pygame.display.flip()
        clock.tick(fps)


game()
