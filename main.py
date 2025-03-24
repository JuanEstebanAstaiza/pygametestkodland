import pygame
import random
import time
import os

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic War")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# Rutas base para recursos
BASE_PATH = os.path.dirname(__file__)

# Cargar imágenes
player_img = pygame.image.load(os.path.join(BASE_PATH, "player.png"))
enemy_img = pygame.image.load(os.path.join(BASE_PATH, "enemy.png"))
boss_img = pygame.image.load(os.path.join(BASE_PATH, "boss.png"))
bullet_img = pygame.image.load(os.path.join(BASE_PATH, "bullet.png"))
background_img = pygame.image.load(os.path.join(BASE_PATH, "background.png"))

# Cargar sonidos
shoot_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "explosion.wav"))

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
        self.triple_shot = False
        self.credits = 10

    def move(self, keys):
        # Se elimina la restricción con los bordes
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        show_text(f"Vidas: {self.lives}", 10, 10)
        show_text(f"Puntos: {self.score}", 10, 40)
        show_text(f"Poder: {self.power}", 10, 70)
        show_text(f"Triple Disparo: {'Sí' if self.triple_shot else 'No'}", 10, 100)
        show_text(f"Créditos: {self.credits}", 10, 130)

# Clase Enemigo
class Enemy:
    def __init__(self, enemy_type="normal"):
        self.type = enemy_type
        self.image = enemy_img if self.type == "normal" else boss_img
        self.x = random.randint(0, WIDTH - self.image.get_width())
        self.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4) if self.type == "normal" else 2
        # Enemigos normales tienen 1 vida, bosses resisten 3 disparos
        self.health = 1 if self.type == "normal" else 3

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

# Función de colisión utilizando rectángulos
def check_collision(bullets, enemies, player):
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.image.get_width(), bullet.image.get_height())
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
            if bullet_rect.colliderect(enemy_rect):
                enemy.health -= bullet.power
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy.health <= 0:
                    if enemy in enemies:
                        enemies.remove(enemy)
                    explosion_sound.play()
                    player.score += 10
                    # Si se eliminó un boss, se otorga 1 crédito extra.
                    if enemy.type != "normal":
                        player.credits += 1
                break

# Función de la tienda (menú de pausa)
def shop(player):
    shop_running = True
    while shop_running:
        screen.fill(BLACK)
        show_text("Tienda - Mejora tu Nave", WIDTH // 3, HEIGHT // 4)
        show_text("1. Triple Disparo (7 créditos)", WIDTH // 4, HEIGHT // 3)
        show_text("2. 2 Vidas extra (7 créditos)", WIDTH // 4, int(HEIGHT // 2.5))
        show_text("Presiona ESC para volver", WIDTH // 4, int(HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if player.credits >= 7:
                        player.triple_shot = True
                        player.credits -= 7
                elif event.key == pygame.K_2:
                    if player.credits >= 7:
                        player.lives += 2
                        player.credits -= 7
                elif event.key == pygame.K_ESCAPE:
                    shop_running = False
        pygame.time.delay(50)

# Función de Game Over
def game_over(player):
    game_over_running = True
    while game_over_running:
        screen.fill(BLACK)
        show_text("GAME OVER", WIDTH // 3, HEIGHT // 3, RED)
        show_text(f"Puntos: {player.score}", WIDTH // 3, HEIGHT // 2, WHITE)
        show_text("Presiona ESC para salir", WIDTH // 3, int(HEIGHT // 1.5), WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        pygame.time.delay(50)

# Función principal
def main():
    clock = pygame.time.Clock()
    player = Player()
    enemies = []
    bullets = []
    last_enemy_spawn_time = time.time()
    group_count = 0  # Cuenta los grupos de enemigos normales generados

    running = True
    paused = False
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Presionar ESC alterna la pausa y abre la tienda
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        shop(player)
                        paused = False  # Al salir de la tienda, se reanuda el juego
                # Disparo
                if event.key == pygame.K_SPACE:
                    if player.triple_shot:
                        bullets.append(Bullet(player.x - 20, player.y, player.power))
                        bullets.append(Bullet(player.x, player.y, player.power))
                        bullets.append(Bullet(player.x + 20, player.y, player.power))
                    else:
                        bullets.append(Bullet(player.x, player.y, player.power))
                    shoot_sound.play()

        # Lógica del juego cuando no está en pausa
        if not paused:
            screen.blit(background_img, (0, 0))
            keys = pygame.key.get_pressed()
            player.move(keys)

            # Generar enemigos cada 5 segundos
            if time.time() - last_enemy_spawn_time > 5:
                group_count += 1
                # Generar 3 enemigos normales
                for _ in range(3):
                    enemies.append(Enemy("normal"))
                # Cada 3 grupos, generar 2 bosses
                if group_count % 3 == 0:
                    for _ in range(2):
                        enemies.append(Enemy("boss"))
                last_enemy_spawn_time = time.time()

            # Actualizar y dibujar enemigos
            for enemy in enemies[:]:
                enemy.move()
                enemy.draw()
                # Si el enemigo pasa la zona del jugador, se le resta una vida
                if enemy.y > player.y + player.image.get_height():
                    enemies.remove(enemy)
                    player.lives -= 1

            # Actualizar y dibujar balas
            for bullet in bullets[:]:
                bullet.move()
                bullet.draw()
                # Remover bala si sale de la pantalla
                if bullet.y < 0:
                    if bullet in bullets:
                        bullets.remove(bullet)

            # Comprobar colisiones
            check_collision(bullets, enemies, player)

            # Dibujar jugador
            player.draw()

        pygame.display.update()
        clock.tick(60)

        # Revisar condición de Game Over
        if player.lives < 0:
            game_over(player)

    pygame.quit()

if __name__ == "__main__":
    main()
