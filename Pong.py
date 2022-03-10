import pygame
import random

player1_name = "PLAYER 1"
player2_name = "PLAYER 2"
win_cap = 3
is_paused = True

display_width = 1200
display_height = 800

player1_score = 0
player2_score = 0

black = (0, 0, 0)
white = (255, 255, 255)

direction = [-1, 1]


def welcome():
    global win_cap
    global player1_name
    global player2_name
    print("- - - W E L C O M E   T O   T H E   P O N K - - -")
    player1_name = input("PLAYER 1:  ")
    player2_name = input("Player 2:  ")
    win_cap = int(input("How much \" rounds \":  "))







def displayText(text, size, x, y):
    fontText = pygame.font.Font('freesansbold.ttf', size)
    TextSurface = fontText.render(text, True, white)
    TextRect = TextSurface.get_rect()
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurface, TextRect)


def ball(x, y, r):
    pygame.draw.circle(gameDisplay, white, (x, y), r)


def endgame(player):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("music/win.mp3")
    pygame.mixer.music.play()
    gameDisplay.fill(black)
    displayText(player + " WINS!!", 70, (display_width / 2), (display_height / 2))
    pygame.display.update()
    pygame.time.wait(3000)
    global player2_score
    global player1_score
    player2_score = 0
    player1_score = 0
    game()


def muter():
    global is_paused
    if is_paused:
        pygame.mixer.music.pause()
        is_paused = False
    else:
        pygame.mixer.music.unpause()
        is_paused = True


def paddle(x, y, width, height):
    pygame.draw.rect(gameDisplay, white, [x, y, width, height])


def game_loop():
    pygame.mixer.music.load("music/popstars.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()

    global win_cap
    global player1_name
    global player2_name

    firstTime = True
    level_counter = 0

    ball_r = 10
    ball_x = int(display_width / 2)
    ball_y = int(display_height / 2)

    ball_speed = 2
    ball_speedX = ball_speed * direction[random.randint(0, 1)]
    ball_speedY = ball_speed + direction[random.randint(0, 1)]

    paddle_width = 10
    paddle_height = int(display_height / 5)

    paddle1_x = 0
    paddle1_y = int(display_height / 3)
    paddle2_x = int(display_width - paddle_width)
    paddle2_y = int(display_height / 3)

    paddle1_speed = 0
    paddle2_speed = 0
    paddle_speed = 8

    while True:
        global player1_score
        global player2_score
        gameDisplay.fill(black)
        ball(ball_x, ball_y, ball_r)
        paddle(paddle1_x, paddle1_y, paddle_width, paddle_height)
        paddle(paddle2_x, paddle2_y, paddle_width, paddle_height)
        displayText((player1_name + ": " + str(player1_score)), 30, 200, 40)
        displayText((player2_name + ": " + str(player2_score)), 30, display_width - 200, 40)

        if firstTime:
            pygame.display.update()
            pygame.time.wait(2000)
            firstTime = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_p:
                    muter()

                if event.key == pygame.K_a:
                    paddle1_speed = -paddle_speed
                if event.key == pygame.K_z:
                    paddle1_speed = paddle_speed

                if event.key == pygame.K_k:
                    paddle2_speed = -paddle_speed
                if event.key == pygame.K_m:
                    paddle2_speed = paddle_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_z:
                    paddle1_speed = 0
                if event.key == pygame.K_k or event.key == pygame.K_m:
                    paddle2_speed = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if ball_y < 0 + ball_r:
            ball_speedY *= -1
        if ball_y > display_height - ball_r:
            ball_speedY *= -1

        if ball_x <= 0 + paddle_width and ball_x >= 0:
            if paddle1_y < ball_y and paddle1_y + paddle_height > ball_y:
                ball_speedX *= -1
                ball_speedY = ball_speedY + random.randint(-2, 2)
                level_counter += 1
                if level_counter % 2 == 0 and level_counter != 0:
                    ball_speedX *= 1.5
            else:
                player2_score += 1
                if player2_score == win_cap:
                    endgame(player2_name)
                game_loop()
        if ball_x <= display_width and ball_x >= display_width - paddle_width:
            if paddle2_y < ball_y and paddle2_y + paddle_height > ball_y:
                ball_speedX *= -1
                ball_speedY = ball_speedY + random.randint(-2, 2)
            else:
                player1_score += 1
                if player1_score == win_cap:
                    endgame(player1_name)
                game_loop()

        paddle1_y += paddle1_speed
        if paddle1_y < 0: paddle1_y = 0
        if paddle1_y > display_height - paddle_height: paddle1_y = display_height - paddle_height
        paddle2_y += paddle2_speed
        if paddle2_y < 0: paddle2_y = 0
        if paddle2_y > display_height - paddle_height: paddle2_y = display_height - paddle_height
        ball_x += int(ball_speedX)
        ball_y -= int(ball_speedY)

        pygame.display.update()
        clock.tick(150)


def game():
    while True:
        gameDisplay.fill(black)
        displayText("P O N K", 100, display_width / 2, display_height / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    game_loop()

if __name__ == '__main__':
    welcome()
    pygame.init()
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Ponk!")
    icon = pygame.image.load("icons/icon.jpg")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    game()
