import sys
import pygame
import pygame_menu
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event, log_state
from player import Player
from shot import Shot

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.init()
pygame.font.init()


def start_the_game():
    print(f"Starting Asteroids woth pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, drawable, updatable)

    while True:
        font = pygame.font.Font("monaco.ttf", 36)
        log_state()

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                display_results(score)

            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    score += 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        for item in drawable:
            item.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000


def main_menu():
    menu = pygame_menu.Menu(
        "Welcome", SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK
    )

    menu.add.button("Play", start_the_game)
    menu.add.button("Exit", pygame_menu.events.EXIT)

    menu.mainloop(screen)


def display_results(score_value):
    results_menu = pygame_menu.Menu(
        "Game Over",
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        theme=pygame_menu.themes.THEME_DARK,
    )

    results_menu.add.label(f"Your Score: {score_value}", font_size=30)
    results_menu.add.button("Restart", start_the_game)
    results_menu.add.button("Quit", pygame_menu.events.EXIT)

    results_menu.mainloop(screen)


if __name__ == "__main__":
    main_menu()
