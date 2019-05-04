## pong.py - A simple clone of the classic game Pong.
## Part of a personal project to learn Game Dev with online resources.
import pygame
import random

## Define window dimensions and paddle speed
WIN_WIDTH = 1000
WIN_HEIGHT = 600
PADDLE_SPEED = 10

## Define colors and font
BLACK = 0, 0, 0
WHITE = 255, 255, 255

## Seeding random number generator
random.seed()

class Ball():
    def __init__(self):
        self.size = 15
        self.x = (WIN_WIDTH / 2) - (self.size / 2)
        self.y = (WIN_HEIGHT / 2) - (self.size / 2)

        self.x_vel = 4 if random.randrange(1, 3) == 1 else -4
        self.y_vel = random.uniform(-1, 1) * 4

    def updatePosition(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def resetBall(self):
        self.x = (WIN_WIDTH / 2) - (self.size / 2)
        self.y = (WIN_HEIGHT / 2) - (self.size / 2)
        self.x_vel = 0
        self.y_vel = 0

    def startMoving(self):
        self.x_vel = 4 if random.randrange(1, 3) == 1 else -4
        self.y_vel = random.uniform(-1, 1) * 4

    def detectWallCollision(self, paddle_left, paddle_right):
        if self.x <= 0:
            paddle_right.score += 1
            self.resetBall()
            return True

        elif self.x >= (WIN_WIDTH - self.size):
            paddle_left.score += 1
            self.resetBall()
            return True

        if self.y <= 0 or self.y >= (WIN_HEIGHT - self.size):
            self.y_vel = -self.y_vel
            return False

        return False

    def detectPaddleCollision(self, paddle):
        if not (self.x > paddle.x + paddle.width or paddle.x > self.x + self.size):
            if not (self.y > paddle.y + paddle.height or paddle.y > self.y + self.size):
                self.x_vel = -(self.x_vel + (self.x_vel * 0.03))
                self.y_vel = random.uniform(-1, 1) * 4

class Paddle():
    def __init__(self, x):
        self.width = 15
        self.height = 60

        self.score = 0

        self.x = x
        self.y = (WIN_HEIGHT / 2) - (self.height / 2)

        self.y_vel = 0
        self.up = False
        self.down = False
        self.hitUpWall = False
        self.hitDownWall = False

    def updatePosition(self):
        if self.up and not self.hitUpWall:
            self.y_vel = -PADDLE_SPEED
        elif self.down and not self.hitDownWall:
            self.y_vel = PADDLE_SPEED
        else:
            self.y_vel = 0


        self.y += self.y_vel

    def detectWallCollision(self):
        if self.y <= 0:
            self.hitUpWall = True

        elif self.y >= (WIN_HEIGHT - self.height):
            self.hitDownWall = True

        else:
            self.hitDownWall = False
            self.hitUpWall = False


def main():
    pygame.init()

    ## Creating the Font objects
    normalFont = pygame.font.Font("font.ttf", 40)

    ## Initializing a window and setting title
    pygame.display.set_caption("Pong")
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    ## Declaring important variables
    running = True
    state = "handling"
    ball = Ball()
    paddle_left = Paddle(30)
    paddle_right = Paddle(WIN_WIDTH - 30 - paddle_left.width)
    clock = pygame.time.Clock()
    fps = 60
    winnerPlayer = "none"

    ## Main game loop
    while running:
        if state == "playing":
            ## Input handling
            for event in pygame.event.get():
                ## If close button is pressed, terminate loop
                if event.type == pygame.QUIT:
                    running = False

                ## Check for keys being pressed
                elif event.type is pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "up":
                        paddle_right.up = True
                    elif pygame.key.name(event.key) == "down":
                        paddle_right.down = True
                    elif pygame.key.name(event.key) == "w":
                        paddle_left.up = True
                    elif pygame.key.name(event.key) == "s":
                        paddle_left.down = True

                ## Check for key being released
                elif event.type is pygame.KEYUP:
                    if pygame.key.name(event.key) == "up":
                        paddle_right.up = False
                    elif pygame.key.name(event.key) == "down":
                        paddle_right.down = False
                    elif pygame.key.name(event.key) == "w":
                        paddle_left.up = False
                    elif pygame.key.name(event.key) == "s":
                        paddle_left.down = False

            ## Check for collisions and update objects to be drawn
            paddle_left.detectWallCollision()
            paddle_right.detectWallCollision()
            ball.detectPaddleCollision(paddle_left)
            ball.detectPaddleCollision(paddle_right)
            if ball.detectWallCollision(paddle_left, paddle_right):
                if paddle_left.score < 10 and paddle_right.score < 10:
                    state = "handling"
                elif paddle_left.score == 10:
                    winnerPlayer = "player one"
                    state = "game_over"
                elif paddle_right.score == 10:
                    winnerPlayer = "player two"
                    state = "game_over"
            ball.updatePosition()
            paddle_left.updatePosition()
            paddle_right.updatePosition()

            ## Fill screen with black to erase all previous drawings
            win.fill(BLACK)

            ## Render the score counter
            left_score = normalFont.render(str(paddle_left.score), 0, WHITE)
            right_score = normalFont.render(str(paddle_right.score), 0, WHITE)
            win.blit(left_score, ((WIN_WIDTH / 2) - 100, 70))
            win.blit(right_score, ((WIN_WIDTH / 2) + 100, 70))

            ## Draw the updated objects and update the window
            pygame.draw.rect(win, WHITE, (ball.x, ball.y, ball.size, ball.size))
            pygame.draw.rect(win, WHITE, (paddle_left.x, paddle_left.y, paddle_left.width, paddle_left.height))
            pygame.draw.rect(win, WHITE, (paddle_right.x, paddle_right.y, paddle_right.width, paddle_right.height))
            pygame.display.update()

        if state == "handling":
            for event in pygame.event.get():
                ## If close button is pressed, terminate loop
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "space":
                        ball.startMoving()
                        state = "playing"

            ## Fill screen with black to erase all previous drawings
            win.fill(BLACK)

            ## Render the instructions message
            press_space = normalFont.render("Press SPACE to start", 0, WHITE)
            win.blit(press_space, ((WIN_WIDTH / 2) - 230, WIN_HEIGHT - 100))

            ## Draw the updated objects and update the window
            pygame.draw.rect(win, WHITE, (ball.x, ball.y, ball.size, ball.size))
            pygame.draw.rect(win, WHITE, (paddle_left.x, paddle_left.y, paddle_left.width, paddle_left.height))
            pygame.draw.rect(win, WHITE, (paddle_right.x, paddle_right.y, paddle_right.width, paddle_right.height))
            pygame.display.update()

        if state == "game_over":
            for event in pygame.event.get():
                ## If close button is pressed, terminate loop
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "space":
                        ball.startMoving()
                        winnerPlayer = "none"
                        state = "handling"
                        paddle_left.score = 0
                        paddle_right.score = 0

            ## Render the "play again" message
            winner = normalFont.render("Player " + winnerPlayer + " wins!", 0, WHITE)
            win.blit(winner, ((WIN_WIDTH / 2) - 240, WIN_HEIGHT - 200))
            play_again = normalFont.render("Press SPACE to play again", 0, WHITE)
            win.blit(play_again, ((WIN_WIDTH / 2) - 270, WIN_HEIGHT - 100))

            ## Draw the updated objects and update the window
            pygame.draw.rect(win, WHITE, (ball.x, ball.y, ball.size, ball.size))
            pygame.draw.rect(win, WHITE, (paddle_left.x, paddle_left.y, paddle_left.width, paddle_left.height))
            pygame.draw.rect(win, WHITE, (paddle_right.x, paddle_right.y, paddle_right.width, paddle_right.height))
            pygame.display.update()

        ## Make sure the program doesn't run faster than the set number for FPS
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()
