import pygame
import random

player1_name = "PLAYER"
win_cap = 3
is_paused = True


def welcome():
    global player1_name
    print("- - - W E L C O M E   T O   T H E   P O N K - - -")
    player1_name = input("PLAYER:  ")


welcome()


display_width = 1000
display_height = 800


word = ""
f = open("h_s.txt", "r")
for letter in reversed(f.read()):
    if letter.isspace():
        break
    else:
        word += letter
player_high_score = int(word[::-1])

pygame.init()

player1_score = 0

gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption("Ponk!")
icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)

direction = [-1, 1]

def displayText(text, size, x, y):
    fontText = pygame.font.Font('freesansbold.ttf', size)
    TextSurface = fontText.render(text, True, white)
    TextRect = TextSurface.get_rect()
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurface, TextRect)

def ball(x, y, r):
    pygame.draw.circle(gameDisplay, white, (x, y), r)

def muter():
    global is_paused
    if is_paused:
        pygame.mixer.music.pause()
        is_paused = False
    else:
        pygame.mixer.music.unpause()
        is_paused = True


def endgame():
    global player1_score
    global player_high_score
    global best_name
    pygame.mixer.music.stop()
    if player1_score > player_high_score:
        pygame.mixer.music.load("wano.mp3")
        player_high_score = player1_score
        f = open("h_s.txt", "w+")
        f.write(player1_name + " " + str(player_high_score))
        f.close()
    else:
        pygame.mixer.music.load("darkness.mp3")
    pygame.mixer.music.play()
    gameDisplay.fill(black)
    h = open("h_s.txt", "r")
    displayText("Your score: " + str(player1_score), 70, (display_width/2), (display_height/2))
    displayText(("Best score: " + h.readline()), 50, (display_width / 2), (display_height*2/3))
    h.close()
    pygame.display.update()
    pygame.time.wait(3000)

    player1_score = 0
    game()




def paddle(x, y, width, height):
    pygame.draw.rect(gameDisplay, white, [x, y, width, height])


def game_loop():
    #pygame.mixer.music.load("popstars.mp3")
    pygame.mixer.music.load("baddest.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()

    global black
    global player1_name

    firstTime = True

    ball_r = 10
    ball_x = int(display_width / 2)
    ball_y = int(display_height / 2)

    ball_speed = 2
    ball_speedX = ball_speed*direction[random.randint(0, 1)]
    ball_speedY = ball_speed+direction[random.randint(0, 1)]

    paddle_width = 10
    paddle_height = int(display_height/4)


    paddle1_x = 0
    paddle1_y = int(display_height / 3)

    paddle1_speed = 0
    paddle_speed = 8

    while True:
        global player1_score
        gameDisplay.fill(black)
        ball(ball_x, ball_y, ball_r)
        paddle(paddle1_x, paddle1_y, paddle_width, paddle_height)
        displayText((player1_name + ": " + str(player1_score)), 30, display_width/2, 40)



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

                if event.key == pygame.K_UP:
                    paddle1_speed = -paddle_speed
                if event.key == pygame.K_DOWN:
                    paddle1_speed = paddle_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle1_speed = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if ball_y < 0+ball_r:
            ball_speedY *= -1
        if ball_y > display_height-ball_r:
            ball_speedY *= -1
        if ball_x > display_width-ball_r:
            ball_speedX += -1

        if ball_x <= 0 + paddle_width and ball_x >= 0:
            if paddle1_y < ball_y and paddle1_y + paddle_height > ball_y:
                ball_speedX *= -1
                ball_speedY = ball_speedY + random.randint(-1, 1)
                player1_score += 1
                if player1_score%3 == 0 and player1_score != 0:
                    ball_speedX *= 1.5
                black = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
            else:
                endgame()

        paddle1_y += paddle1_speed
        if paddle1_y < 0: paddle1_y = 0
        if paddle1_y > display_height-paddle_height: paddle1_y = display_height-paddle_height
        ball_x += int(ball_speedX)
        ball_y -= int(ball_speedY)

        pygame.display.update()
        clock.tick(160)


def game():
    while True:
        gameDisplay.fill(black)
        displayText("P O N K", 100, display_width/2, display_height/2)
        pygame.display.update()
        for event in pygame.event.get():
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    game_loop()

game()
