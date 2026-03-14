from dataclasses import dataclass

import pygame


@dataclass
class Level:
    name: str
    spawn: tuple[int, int]
    switches: int
    platforms: list[pygame.Rect]
    hazards: list[pygame.Rect]
    exit_rect: pygame.Rect
    final_core: bool = False
