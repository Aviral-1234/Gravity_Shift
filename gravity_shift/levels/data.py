import pygame

from gravity_shift.level import Level
from gravity_shift.settings import HEIGHT, WIDTH


def rect(x: int, y: int, width: int, height: int) -> pygame.Rect:
    return pygame.Rect(x, y, width, height)


def room_bounds() -> list[pygame.Rect]:
    return [
        rect(0, HEIGHT - 24, WIDTH, 24),
        rect(0, 0, WIDTH, 24),
        rect(0, 0, 24, HEIGHT),
        rect(WIDTH - 24, 0, 24, HEIGHT),
    ]


def build_levels() -> list[Level]:
    common_bounds = room_bounds()

    return [
        Level(
            name="Level 1 - Introduction",
            spawn=(70, HEIGHT - 70),
            switches=5,
            platforms=[
                *common_bounds,
                rect(160, 500, 180, 24),
                rect(340, 430, 24, 110),
                rect(420, 340, 180, 24),
                rect(610, 260, 24, 110),
                rect(690, 180, 170, 24),
            ],
            hazards=[],
            exit_rect=rect(770, 130, 44, 44),
        ),
        Level(
            name="Level 2 - Puzzle Complexity",
            spawn=(70, HEIGHT - 70),
            switches=7,
            platforms=[
                *common_bounds,
                rect(150, 520, 220, 24),
                rect(370, 430, 24, 114),
                rect(460, 430, 180, 24),
                rect(640, 320, 24, 134),
                rect(560, 250, 160, 24),
                rect(420, 160, 24, 114),
                rect(250, 160, 180, 24),
                rect(220, 250, 24, 114),
                rect(120, 320, 130, 24),
            ],
            hazards=[rect(664, HEIGHT - 24, 140, 24)],
            exit_rect=rect(150, 110, 44, 44),
        ),
        Level(
            name="Level 3 - Gravity Core",
            spawn=(70, HEIGHT - 70),
            switches=8,
            platforms=[
                *common_bounds,
                rect(100, 540, 180, 24),
                rect(280, 460, 24, 104),
                rect(350, 460, 180, 24),
                rect(530, 370, 24, 114),
                rect(620, 370, 180, 24),
                rect(800, 280, 24, 114),
                rect(620, 200, 200, 24),
                rect(500, 200, 24, 114),
                rect(380, 120, 220, 24),
                rect(300, 200, 24, 114),
                rect(180, 280, 200, 24),
                rect(150, 360, 24, 114),
                rect(430, 285, 120, 24),
                rect(430, 285, 24, 120),
                rect(526, 285, 24, 56),
                rect(430, 381, 36, 24),
                rect(514, 381, 36, 24),
            ],
            hazards=[
                rect(304, HEIGHT - 24, 220, 24),
                rect(664, HEIGHT - 24, 136, 24),
            ],
            exit_rect=rect(468, 324, 44, 44),
            final_core=True,
        ),
    ]
