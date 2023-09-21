import math
import pygame


class Road:
    """Endless scrolling, TOPDOWN [ top to bottom ]"""
    def __init__(self):
        self.image = pygame.image.load("img/road.png").convert_alpha()
        self.image_height = self.image.get_height()

        self.scroll = 0
        self.panels = math.ceil(WINDOW_HEIGHT / self.image_height + 2)

        self.acc = 0
        self.speed = 30
        self.min_speed = 30
        self.max_speed = 160
        self.increase = False
        self.decrease = False

    def scrolling(self):
        """Endless scroll method"""
        self.scroll += 1
        for i in range(self.panels):
            y_pos = int((i * self.image_height) + self.scroll - self.image_height)
            screen.blit(self.image, (0, y_pos))
            if abs(self.scroll) >= self.image_height:
                self.scroll = 0

    def update_speed_string(self):
        """Display and update speed"""
        if self.increase:
            self.speed += 1.5
        elif self.decrease:
            self.speed -= 1

        self.speed = max(self.min_speed, min(self.max_speed, self.speed))

        speed_text = FONT.render(f"{int(self.speed)} km/h", 1, "Black")
        screen.blit(speed_text, (10, 750))

    def movement(self):
        """Adjust scrolling speed based on user input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.acc += 0.15
            self.increase = True
            self.decrease = False
            # don't speed forever
            self.acc = min(self.acc, 10)
        else:
            # Gradually reduce acceleration when no UP key is pressed
            if self.acc > 0:
                self.acc -= 0.1  # Adjust this value for the desired rate of decrease
                self.speed -= 3
                self.increase = True
                self.decrease = False
                if self.scroll <= 0.02:
                    self.scroll = 0
            elif self.acc < 0:
                self.decrease = True
                self.increase = False

        self.scroll += self.acc

    def update(self):
        self.scrolling()
        self.movement()
        self.update_speed_string()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/car.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(midbottom=(300, 750))

    def movement(self):
        """Move the player's car left or right based on user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.x <= 160:
                self.rect.x += 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
            if self.rect.x >= 390:
                self.rect.x -= 10

    def update(self):
        self.movement()


def fps_counter():
    """Display the current FPS rate"""
    fps = str(round(clock.get_fps(), 2))
    fps_text = FONT.render(fps, 1, "Black")
    screen.blit(fps_text, (0, 0))


pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FONT = pygame.font.SysFont("Arial", 25, bold=True)
running = True

pygame.display.set_caption("Endless Scrolling")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED, vsync=1)

road = Road()

player = pygame.sprite.GroupSingle()
player.add(Player())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    road.update()
    player.draw(screen)
    player.update()

    fps_counter()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
