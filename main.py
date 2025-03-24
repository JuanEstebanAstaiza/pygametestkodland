import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic War")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Cargar imágenes
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
boss_img = pygame.image.load("boss.png")
bullet_img = pygame.image.load("bullet.png")
background_img = pygame.image.load("background.png")

# Sonidos
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Fuente
font = pygame.font.Font(None, 36)


def show_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Clase Jugador
class Player:
    def __init__(self):
        self.image = player_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 5
        self.lives = 3
        self.score = 0
        self.power = 1

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 64:
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        show_text(f"Vidas: {self.lives}", 10, 10)
        show_text(f"Puntos: {self.score}", 10, 40)
        show_text(f"Poder: {self.power}", 10, 70)


# Clase Enemigo
class Enemy:
    def __init__(self, enemy_type="normal"):
        self.type = enemy_type
        self.image = enemy_img if self.type == "normal" else boss_img
        self.x = random.randint(0, WIDTH - 64)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4) if self.type == "normal" else 2
        self.health = 1 if self.type == "normal" else 10

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# Clase Bala
class Bullet:
    def __init__(self, x, y, power):
        self.image = bullet_img
        self.x = x
        self.y = y
        self.speed = 7
        self.power = power

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# Pantallas del juego
def show_menu():
    screen.fill(BLACK)
    show_text("GALACTIC WAR", WIDTH // 3, HEIGHT // 3)
    show_text("Presiona ENTER para jugar", WIDTH // 3, HEIGHT // 2)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def game_over():
    screen.fill(BLACK)
    show_text("GAME OVER", WIDTH // 3, HEIGHT // 3, RED)
    show_text("Presiona ENTER para reiniciar", WIDTH // 3, HEIGHT // 2)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()


def shop(player):
    screen.fill(BLACK)
    show_text("Tienda - Mejora tu Nave", WIDTH // 3, HEIGHT // 4)
    show_text("1. Aumentar Poder (20 puntos)", WIDTH // 4, HEIGHT // 3)
    show_text("Presiona la tecla correspondiente para comprar", WIDTH // 5, HEIGHT // 2)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and player.score >= 20:
                    player.power += 1
                    player.score -= 20
                waiting = False


def main():
    clock = pygame.time.Clock()
    running = True
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    bullets = []
    show_menu()
    level = 1

    while running:
        screen.blit(background_img, (0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x + 16, player.y, player.power))
                    shoot_sound.play()
                if event.key == pygame.K_s:
                    shop(player)

        player.move(keys)
        player.draw()

        for enemy in enemies:
            enemy.move()
            enemy.draw()
            if enemy.y > HEIGHT:
                player.lives -= 1
                enemies.remove(enemy)
                enemies.append(Enemy())
                if player.lives == 0:
                    game_over()

        for bullet in bullets:
            bullet.move()
            bullet.draw()
            for enemy in enemies:
                if bullet.y < enemy.y + 64 and bullet.x in range(enemy.x, enemy.x + 64):
                    explosion_sound.play()
                    enemy.health -= bullet.power
                    if enemy.health <= 0:
                        player.score += 10
                        enemies.remove(enemy)
                        if random.randint(1, 5) == 1:
                            enemies.append(Enemy("boss"))
                        else:
                            enemies.append(Enemy())
                    bullets.remove(bullet)
                    break

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
