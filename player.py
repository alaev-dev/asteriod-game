from typing import ClassVar
from circleshape import CircleShape
from constants import (
    PLATER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_SHOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
import pygame

from shot import Shot
import shot


class Player(CircleShape):
    containers: ClassVar[tuple] = ()

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.countdown_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # type: ignore
        b = self.position - forward * self.radius - right  # type: ignore
        c = self.position - forward * self.radius + right  # type: ignore
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)

        if keys[pygame.K_SPACE]:
            self.shoot()

        self.countdown_timer -= dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_vector_with_speed = rotated_vector * PLAYER_SPEED * dt

        self.position += rotated_vector_with_speed

    def shoot(self):
        if self.countdown_timer > 0:
            return

        shot = Shot(self.position.x, self.position.y)
        unit = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = unit * PLAYER_SHOT_SPEED

        self.countdown_timer = PLATER_SHOOT_COOLDOWN_SECONDS
