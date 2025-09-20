import pygame
import os

# --- Initialize Pygame and mixer with high-quality sound ---
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Window setup
WIDTH, HEIGHT = 800, 800
FPS = 70

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (60, 160, 200)
GREEN = (80, 175, 90)

COLUMNS = 10
ROWS = 6

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BreakOut")
clock = pygame.time.Clock()

# --- Sounds ---
def load_sound(filename):
    path = os.path.join(os.getcwd(), filename)
    if os.path.exists(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(1.0)  # full volume
        return sound
    else:
        print(f"Sound file '{filename}' not found!")
        return None

bounce_sound = load_sound("bounce.wav")  # Paddle hit
hit_sound = load_sound("hit.wav")        # Brick hit

# --- Brick class ---
class Brick:
    def __init__(self):
        self.width = WIDTH // COLUMNS
        self.height = 30
        self.bricks = []

    def create_bricks(self):
        self.bricks = []
        for row in range(ROWS):
            brick_row = []
            for col in range(COLUMNS):
                x = col * self.width
                y = row * self.height
                br = pygame.Rect(x, y, self.width, self.height)
                brick_row.append(br)
            self.bricks.append(brick_row)

    def draw_bricks(self):
        for row in self.bricks:
            for br in row:
                pygame.draw.rect(WIN, GREEN, br)
                pygame.draw.rect(WIN, BLACK, br, 2)

# --- Paddle class ---
class Paddle:
    def __init__(self):
        self.width = WIDTH // COLUMNS
        self.height = 20
        self.rect = pygame.Rect(WIDTH//2 - self.width//2, HEIGHT-40, self.width, self.height)
        self.speed = 10

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# --- Ball class ---
class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.dx = 3
        self.dy = -3
        self.game_status = 0

    def draw(self):
        pygame.draw.circle(WIN, BLUE, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def move(self, paddle, bricks):
        # --- Wall collisions ---
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.dx *= -1
            if bounce_sound: bounce_sound.play()
        if self.rect.top <= 0:
            self.dy *= -1
            if bounce_sound: bounce_sound.play()

        # --- Paddle collision ---
        if self.rect.colliderect(paddle.rect) and self.dy > 0:
            self.dy *= -1
            if bounce_sound: bounce_sound.play()

        # --- Brick collisions ---
        for row in bricks.bricks:
            for br in row[:]:
                if self.rect.colliderect(br):
                    self.dy *= -1
                    row.remove(br)
                    if hit_sound: hit_sound.play()
                    break

        # --- Move ball ---
        self.rect.x += self.dx
        self.rect.y += self.dy

        # --- Game over ---
        if self.rect.bottom > HEIGHT:
            self.game_status = -1

        return self.game_status

# --- Game objects ---
paddle = Paddle()
ball = Ball(paddle.rect.centerx, paddle.rect.top - 10)
brick_wall = Brick()
brick_wall.create_bricks()

# --- Main loop ---
run = True
while run:
    clock.tick(FPS)
    WIN.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if ball.game_status == -1:
        font = pygame.font.SysFont(None, 50)
        text = font.render('GAME OVER', True, BLUE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        WIN.blit(text, text_rect)
    else:
        paddle.move()
        paddle.draw()
        brick_wall.draw_bricks()
        ball.draw()
        ball.move(paddle, brick_wall)

    pygame.display.update()

pygame.quit()
