import pygame


WIDTH = 960
HEIGHT = 640
FPS = 60

BG_COLOR = (15, 18, 25)
PLATFORM_COLOR = (70, 90, 120)
HAZARD_COLOR = (140, 55, 55)
PLAYER_COLOR = (240, 240, 245)
GATE_COLOR = (80, 210, 140)
CORE_COLOR = (115, 220, 255)
TEXT_COLOR = (230, 232, 240)
ACCENT_COLOR = (255, 195, 95)

GRAVITY_ACCEL = 0.65
MAX_FALL_SPEED = 16
MOVE_SPEED = 4.0

VECTORS = {
    "down": pygame.Vector2(0, 1),
    "up": pygame.Vector2(0, -1),
    "left": pygame.Vector2(-1, 0),
    "right": pygame.Vector2(1, 0),
}


def tangent_axis(gravity_name: str) -> pygame.Vector2:
    if gravity_name in ("down", "up"):
        return pygame.Vector2(1, 0)
    return pygame.Vector2(0, 1)
