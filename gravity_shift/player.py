import pygame

from gravity_shift.settings import GRAVITY_ACCEL, MAX_FALL_SPEED, MOVE_SPEED, VECTORS, tangent_axis


class Player:
    def __init__(self, spawn: tuple[int, int]):
        self.rect = pygame.Rect(spawn[0], spawn[1], 28, 28)
        self.vel = pygame.Vector2(0, 0)
        self.gravity_name = "down"
        self.grounded = False

    def reset(self, spawn: tuple[int, int]) -> None:
        self.rect.topleft = spawn
        self.vel.update(0, 0)
        self.gravity_name = "down"
        self.grounded = False

    def switch_gravity(self, new_gravity: str) -> None:
        if new_gravity == self.gravity_name:
            return

        current_gravity = VECTORS[self.gravity_name]
        current_tangent = pygame.Vector2(-current_gravity.y, current_gravity.x)
        tangent_speed = self.vel.dot(current_tangent)

        self.gravity_name = new_gravity

        next_gravity = VECTORS[new_gravity]
        next_tangent = pygame.Vector2(-next_gravity.y, next_gravity.x)
        self.vel = next_tangent * tangent_speed
        self.grounded = False

    def update(self, move_input: float, platforms: list[pygame.Rect]) -> None:
        gravity_vector = VECTORS[self.gravity_name]
        tangent_vector = tangent_axis(self.gravity_name)

        self.vel += gravity_vector * GRAVITY_ACCEL
        if self.vel.length() > MAX_FALL_SPEED * 1.4:
            self.vel.scale_to_length(MAX_FALL_SPEED * 1.4)

        self.vel += tangent_vector * (move_input * 0.9)
        tangent_velocity = self.vel.dot(tangent_vector)
        tangent_velocity = max(-MOVE_SPEED, min(MOVE_SPEED, tangent_velocity))
        gravity_velocity = self.vel.dot(gravity_vector)
        self.vel = tangent_vector * tangent_velocity + gravity_vector * gravity_velocity

        self.grounded = False
        self._move_axis("x", platforms)
        self._move_axis("y", platforms)

    def _move_axis(self, axis: str, platforms: list[pygame.Rect]) -> None:
        amount = self.vel.x if axis == "x" else self.vel.y
        if amount == 0:
            return

        if axis == "x":
            self.rect.x += int(round(amount))
        else:
            self.rect.y += int(round(amount))

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            if axis == "x":
                if amount > 0:
                    self.rect.right = platform.left
                else:
                    self.rect.left = platform.right
                self.vel.x = 0
            else:
                if amount > 0:
                    self.rect.bottom = platform.top
                else:
                    self.rect.top = platform.bottom
                self.vel.y = 0

            if self._is_support_collision(axis, amount):
                self.grounded = True

    def _is_support_collision(self, axis: str, amount: float) -> bool:
        if self.gravity_name == "down" and axis == "y" and amount > 0:
            return True
        if self.gravity_name == "up" and axis == "y" and amount < 0:
            return True
        if self.gravity_name == "left" and axis == "x" and amount < 0:
            return True
        if self.gravity_name == "right" and axis == "x" and amount > 0:
            return True
        return False
