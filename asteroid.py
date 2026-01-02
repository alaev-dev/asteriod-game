import random
from typing import ClassVar
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    containers: ClassVar[tuple] = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius < ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)

        first_new_vector = self.velocity.rotate(angle)
        second_new_vector = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first = Asteroid(self.position.x, self.position.y, new_radius)
        second = Asteroid(self.position.x, self.position.y, new_radius)

        first.velocity = first_new_vector * 1.2
        second.velocity = second_new_vector * 1.2
