import pygame, random

pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
green = (0, 155, 0)
light_green = (0, 205, 0) # Hovering
dark_green = (0, 80, 0)
purple = (214, 32, 211)
blue = (0, 0, 255)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)


green_head = pygame.image.load('SnakeHeadGreen.png')
purple_head = pygame.image.load('SnakeHeadPurple.png')
apple_img = pygame.image.load('Apple.png')
font = pygame.font.SysFont("comicsansms", 50)
smallfont = pygame.font.SysFont("comicsansms", 25)
bigfont = pygame.font.SysFont("comicsansms", 85)

res_x = 600
res_y = 600
Display = pygame.display.set_mode((res_x, res_y))
FPS = 12
block_size = 20
apple_size = 32
apple_count = 1
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(apple_img)
clock = pygame.time.Clock()

direction = "right"
apples = set([])


class Snake:
    def __init__(self, pos, vel, angle, image, color=green):
        self.pos = pos
        self.vel = vel
        self.angle = angle
        self.img = image
        self.list = []
        self.lenght = 1
        self.head = self.img
        self.color = color

    def score_display(self, pos):
        score(self.lenght-1, pos, self.color)

    def key_event(self, direction):
        self.angle = direction

    def eat(self):
        for apple in apples:
            if self.pos[0] > apple.pos[0] and self.pos[0] < apple.pos[0] + apple_size or self.pos[0] + block_size > apple.pos[0] and self.pos[0] < apple.pos[0] + apple_size:
                if self.pos[1] > apple.pos[1] and self.pos[1] < apple.pos[1] + apple.size or self.pos[1] + block_size > apple.pos[1] and self.pos[1] < apple.pos[1] + apple.size:
                    apples.remove(apple)
                    apples.add(randAppleGen())
                    self.lenght += 1

        
    def update(self):
        gameOver = False
        
        if (self.angle == "right") and (self.vel[0] != -block_size):
            self.vel[0] = +block_size
            self.vel[1] = 0
            self.head = pygame.transform.rotate(self.img, 270)
            
        if (self.angle == "left") and (self.vel[0] != block_size):
            self.vel[0] = -block_size
            self.vel[1] = 0
            self.head = pygame.transform.rotate(self.img, 90)
            
        if (self.angle == "up") and (self.vel[1] != block_size):
            self.head = self.img
            self.vel[1] = -block_size
            self.vel[0] = 0
            
        if (self.angle == "down") and (self.vel[1] != -block_size):
            self.vel[1] = +block_size
            self.vel[0] = 0
            self.head = pygame.transform.rotate(self.img, 180)

        # update movement
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # build the snake
        snakeHead = []
        snakeHead.append(self.pos[0])
        snakeHead.append(self.pos[1])
        self.list.append(snakeHead)
        if len(self.list) > self.lenght:
            del self.list[0]
        if snakeHead in self.list[:-1]:
            gameOver = True
        # draw the snake
        for XnY in self.list[:-1]:
            pygame.draw.rect(Display, self.color, [XnY[0], XnY[1], block_size, block_size])
        # draw the snake's head
        Display.blit(self.head, (self.list[-1][0], self.list[-1][1]))
        
        # check if out of boundries
        if self.pos[0] < 0 or self.pos[0] >= res_x or self.pos[1] < 0 or self.pos[1] >= res_y:
            gameOver = True
        return gameOver


class Apple:
    def __init__(self, pos, size, image = None):
        self.pos = pos
        self.img = image
        self.size = size
        
    def draw(self):
        #pygame.draw.rect(Display, red,[self.pos[0], self.pos[1], self.size, self.size])
        Display.blit(self.img, self.pos)

        
def pause():
    paused = True
    message_screen("Paused", black, -100, "large")
    message_screen("Press Space to continue or Escape to quit", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    exit_game()
        clock.tick(10)

def score(score, pos, color):
    text = smallfont.render("Score: "+str(score), True, color)
    Display.blit(text, pos)


def text_objects(text, color, size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = font.render(text, True, color)
    elif size == "large":
        textSurface = bigfont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, pos, size = "small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (pos[0]+(pos[2]/2), pos[1]+(pos[3]/2))
    Display.blit(text_surf, text_rect)
    

def message_screen(msg, color, y_displace=0, size = "small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (res_x/2), (res_y/2)+y_displace
    Display.blit(text_surf, text_rect)


def randAppleGen():
    new_apple = Apple([round(random.randrange(apple_size, res_x-apple_size)/10)*10,
                 round(random.randrange(apple_size, res_y-apple_size)/10)*10],
                 apple_size, apple_img)
    return new_apple


def game_controls():
    controlls = True
    Display.fill(white)
    message_screen("Controls", green, -120, "large")
    message_screen("Green movement: Arrow keys", green, -30, "small")
    message_screen("Purple movement: W, A, S, D keys", purple, 10, "small")
    message_screen("Pause: P", black, 60, "small")
    while controlls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controlls = False
                elif event.key == pygame.K_ESCAPE:
                    exit_game()

        controlls = button("Main Menu", (res_x/2-70, res_y-150, 140, 50), yellow, light_yellow, action = "switch")
        button("Quit", (res_x/2+120, res_y-150, 100, 50), red, light_red, action = "quit")

        clock.tick(30)
        pygame.display.update()

def button(text, pos, color1, color2, action, text_color = black):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0]+pos[2] > cur[0] > pos[0] and pos[1]+pos[3] > cur[1] > pos[1]:
        pygame.draw.rect(Display, color2, pos)
        if click[0] == 1:
            if action == "switch":
                return False
            elif action == "controls":
                clock.tick(6)
                game_controls()
                clock.tick(6)
            elif action == "quit":
                exit_game()
    else:
        pygame.draw.rect(Display, color1, pos)
    text_to_button(text, text_color, pos)

    return True


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_ESCAPE:
                    exit_game()

        Display.fill(white)
        message_screen("Snake Game", green, -120, "large")
        message_screen("Collect apples, and do", black, -30, "small")
        message_screen("not hit yourself!", black, 10, "small")
        intro = button("Play", (res_x/2-220, res_y-150, 100, 50), green, light_green, action = "switch")
        button("Controls", (res_x/2-60, res_y-150, 120, 50), yellow, light_yellow, action = "controls")
        button("Quit", (res_x/2+120, res_y-150, 100, 50), red, light_red, action = "quit")
        clock.tick(30)
        pygame.display.update()

def gameLoop():
    global apple_count
    gameExit = False
    gameOver = False
    while apple_count > len(apples):
            apple = randAppleGen()
            apples.add(apple)
    snake1 = Snake([((res_x/2-5*block_size)/10)*10, (res_y/20)*10], [0, 0], None, green_head)
    snake2 = Snake([((res_x/2-5*block_size)/10)*10, (res_y/20)*10], [0, 0], None, purple_head, purple)

    while not gameExit:
        if apple_count > len(apples):
            apple = randAppleGen()
            apples.add(apple)
        elif apple_count < len(apples):
            apples.pop()
        
        if gameOver == True:
            message_screen("Game Over!", red, -50, "large")
            message_screen("Press Space to restart or Esc to quit.", black, 30)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit_game()
                        if event.key == pygame.K_SPACE:
                            gameLoop()

        for event in pygame.event.get():  # Events LEAD
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:          # Snake1
                    snake1.key_event("left")

                if event.key == pygame.K_RIGHT:
                    snake1.key_event("right")
                    
                if event.key == pygame.K_DOWN:
                    snake1.key_event("down")
                    
                if event.key == pygame.K_UP:
                    snake1.key_event("up")

                if event.key == pygame.K_a:          # Snake2
                    snake2.key_event("left")

                if event.key == pygame.K_d:
                    snake2.key_event("right")
                    
                if event.key == pygame.K_s:
                    snake2.key_event("down")
                    
                if event.key == pygame.K_w:
                    snake2.key_event("up")

                
                if event.key == pygame.K_SPACE:
                    pause()
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_e:
                    apple_count += 1
                if event.key == pygame.K_q:
                    apple_count = 100

        

        Display.fill(white)
        
        for apple in apples:
            apple.draw()

        if snake1.update() or snake2.update():
            gameOver = True

        snake1.score_display([50, 2])
        snake1.eat()
        snake2.score_display([res_x-150, 2])
        snake2.eat()
        

        pygame.display.update()
        


        clock.tick(FPS)
    exit_game()

def exit_game():
    pygame.quit()
    quit()

game_intro()
gameLoop()
#end
