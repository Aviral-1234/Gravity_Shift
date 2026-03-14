import math
import sys

import pygame

from gravity_shift.levels import build_levels
from gravity_shift.player import Player
from gravity_shift.settings import (
    ACCENT_COLOR,
    BG_COLOR,
    CORE_COLOR,
    FPS,
    GATE_COLOR,
    HEIGHT,
    HAZARD_COLOR,
    PLATFORM_COLOR,
    PLAYER_COLOR,
    TEXT_COLOR,
    WIDTH,
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gravity Shift")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 44, bold=True)

        self.levels = build_levels()
        self.level_idx = 0
        self.level = self.levels[self.level_idx]
        self.player = Player(self.level.spawn)
        self.switches_left = self.level.switches
        self.state = "menu"
        self.completion_timer = 0

        self.a_down_frames = 0
        self.d_down_frames = 0
        self.max_tap_frames = 8

    def start_level(self, idx: int) -> None:
        self.level_idx = idx
        self.level = self.levels[idx]
        self.player.reset(self.level.spawn)
        self.switches_left = self.level.switches
        self.state = "playing"
        self.completion_timer = 0
        self.a_down_frames = 0
        self.d_down_frames = 0

    def restart_level(self) -> None:
        self.start_level(self.level_idx)

    def try_switch(self, direction: str) -> None:
        if self.state != "playing":
            return
        if self.player.gravity_name == direction:
            return
        if self.switches_left <= 0:
            return

        self.player.switch_gravity(direction)
        self.switches_left -= 1

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.state == "menu" and event.key == pygame.K_RETURN:
                    self.start_level(0)
                    continue

                if self.state in ("level_clear", "final_sequence"):
                    if event.key == pygame.K_RETURN and self.state == "level_clear":
                        next_idx = self.level_idx + 1
                        if next_idx < len(self.levels):
                            self.start_level(next_idx)
                        else:
                            self.state = "finished"
                    if event.key == pygame.K_r:
                        self.restart_level()
                    continue

                if self.state == "finished":
                    if event.key == pygame.K_RETURN:
                        self.state = "menu"
                    continue

                if self.state == "playing":
                    if event.key == pygame.K_w:
                        self.try_switch("up")
                    elif event.key == pygame.K_s:
                        self.try_switch("down")
                    elif event.key == pygame.K_r:
                        self.restart_level()
                    elif event.key == pygame.K_a:
                        self.a_down_frames = 1
                    elif event.key == pygame.K_d:
                        self.d_down_frames = 1

            if event.type == pygame.KEYUP and self.state == "playing":
                if event.key == pygame.K_a:
                    if 0 < self.a_down_frames <= self.max_tap_frames:
                        self.try_switch("left")
                    self.a_down_frames = 0
                elif event.key == pygame.K_d:
                    if 0 < self.d_down_frames <= self.max_tap_frames:
                        self.try_switch("right")
                    self.d_down_frames = 0

    def update(self) -> None:
        if self.state != "playing":
            if self.state == "final_sequence":
                self.completion_timer += 1
                if self.completion_timer > 240:
                    self.state = "finished"
            return

        keys = pygame.key.get_pressed()
        if self.a_down_frames > 0:
            self.a_down_frames += 1
        if self.d_down_frames > 0:
            self.d_down_frames += 1

        move = 0
        if keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_d]:
            move += 1

        self.player.update(move, self.level.platforms)

        for hazard in self.level.hazards:
            if self.player.rect.colliderect(hazard):
                self.restart_level()
                return

        if not self.screen.get_rect().inflate(120, 120).colliderect(self.player.rect):
            self.restart_level()
            return

        if self.player.rect.colliderect(self.level.exit_rect):
            if self.level.final_core:
                self.state = "final_sequence"
                self.completion_timer = 0
            else:
                self.state = "level_clear"

    def draw_world(self) -> None:
        self.screen.fill(BG_COLOR)

        for platform in self.level.platforms:
            pygame.draw.rect(self.screen, PLATFORM_COLOR, platform)

        for hazard in self.level.hazards:
            pygame.draw.rect(self.screen, HAZARD_COLOR, hazard)

        if self.level.final_core:
            tick = pygame.time.get_ticks() * 0.006
            pulse = 0.55 + 0.45 * math.sin(tick)
            color = (
                int(CORE_COLOR[0] * pulse + 30),
                int(CORE_COLOR[1] * pulse + 15),
                int(CORE_COLOR[2] * pulse),
            )
            pygame.draw.ellipse(self.screen, color, self.level.exit_rect)
            pygame.draw.ellipse(
                self.screen,
                (220, 245, 255),
                self.level.exit_rect.inflate(-18, -18),
            )
        else:
            pygame.draw.rect(self.screen, GATE_COLOR, self.level.exit_rect, border_radius=8)
            pygame.draw.rect(
                self.screen,
                (170, 255, 220),
                self.level.exit_rect.inflate(-16, -16),
                border_radius=8,
            )

        pygame.draw.rect(self.screen, PLAYER_COLOR, self.player.rect, border_radius=4)

    def draw_hud(self) -> None:
        info_lines = [
            self.level.name,
            f"Switches Left: {self.switches_left}",
            f"Gravity: {self.player.gravity_name.upper()}",
            "Move: hold A / D  |  Gravity: W,S + tap A,D  |  Restart: R",
        ]

        for index, line in enumerate(info_lines):
            surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surface, (20, 18 + index * 28))

        if self.switches_left <= 0:
            warning = self.font.render(
                "No switches left. If stuck, press R to restart.",
                True,
                ACCENT_COLOR,
            )
            self.screen.blit(warning, (20, HEIGHT - 36))

    def draw_overlay(self) -> None:
        if self.state == "menu":
            self.screen.fill(BG_COLOR)
            title = self.big_font.render("GRAVITY SHIFT", True, TEXT_COLOR)
            subtitle = self.font.render("Directional Gravity Puzzle", True, ACCENT_COLOR)
            start = self.font.render("Press ENTER to start", True, TEXT_COLOR)
            controls = self.font.render(
                "W/S switch up/down, tap A/D switch left/right, hold A/D to move",
                True,
                TEXT_COLOR,
            )
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
            self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 260))
            self.screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 340))
            self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, 380))
            return

        if self.state == "level_clear":
            panel = pygame.Surface((520, 180), pygame.SRCALPHA)
            panel.fill((12, 16, 24, 220))
            self.screen.blit(panel, (220, 220))
            headline = self.big_font.render("Level Complete", True, GATE_COLOR)
            prompt = self.font.render("Press ENTER for next level", True, TEXT_COLOR)
            self.screen.blit(headline, (WIDTH // 2 - headline.get_width() // 2, 260))
            self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 330))
            return

        if self.state == "final_sequence":
            shake = 5 if (self.completion_timer // 6) % 2 == 0 else -5
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((200, 230, 255, min(180, self.completion_timer)))
            self.screen.blit(overlay, (shake, 0))
            if self.completion_timer > 40:
                headline = self.big_font.render("GRAVITY MASTERED", True, (20, 35, 55))
                subhead = self.font.render(
                    "The Gravity Core collapses all directions into one.",
                    True,
                    (20, 35, 55),
                )
                self.screen.blit(headline, (WIDTH // 2 - headline.get_width() // 2, 280))
                self.screen.blit(subhead, (WIDTH // 2 - subhead.get_width() // 2, 330))
            return

        if self.state == "finished":
            self.screen.fill((10, 14, 20))
            message = self.big_font.render("You Mastered Gravity", True, CORE_COLOR)
            tip = self.font.render("Press ENTER to return to menu", True, TEXT_COLOR)
            self.screen.blit(message, (WIDTH // 2 - message.get_width() // 2, 260))
            self.screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 330))

    def run(self) -> None:
        while True:
            self.process_events()
            self.update()

            if self.state in ("menu", "finished"):
                self.draw_overlay()
            else:
                self.draw_world()
                self.draw_hud()
                self.draw_overlay()

            pygame.display.flip()
            self.clock.tick(FPS)


def run_game() -> None:
    Game().run()
