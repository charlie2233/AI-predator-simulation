"""
Main simulation runner with pygame interface and a front menu scene.
Includes manual event injection via the control panel.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pygame
from simulation.world import World
from simulation.ui.control_panel import ControlPanel
from simulation.ui.visualization import PopulationGraph, TraitGraph, LogPanel
from simulation.ui.components import Button
from simulation.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    STATS_PANEL_WIDTH,
    FPS,
    BLACK,
    WHITE,
    SPECIES_STYLE,
    UI_BG_COLOR,
    UI_TEXT_COLOR,
    UI_BORDER_COLOR,
    UI_PANEL_BG
)


class Simulation:
    """Main simulation controller with menu + play scenes."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Evolving Animals Sandbox")

        self.world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.clock = pygame.time.Clock()
        self.save_path = os.path.join(os.getcwd(), "saves", "latest.json")
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT, {"save_path": self.save_path})

        self.viewport_width = WINDOW_WIDTH - STATS_PANEL_WIDTH
        
        self.control_panel = ControlPanel(self.viewport_width + 10, 10, STATS_PANEL_WIDTH - 20, WINDOW_HEIGHT - 20)
        self.population_graph = PopulationGraph(
            self.viewport_width + 10, 420, STATS_PANEL_WIDTH - 20, 140, species_names=list(SPECIES_STYLE.keys())
        )
        self.trait_graph = TraitGraph(self.viewport_width + 10, 580, STATS_PANEL_WIDTH - 20, 110, self._current_trait_title())
        self.log_panel = LogPanel(self.viewport_width + 10, 700, STATS_PANEL_WIDTH - 20, 50)

        self.running = True
        self.paused = True
        self.started = False
        self.scene = "menu"  # menu | play
        self.show_credits = False
        self.update_counter = 0
        self.pending_event_type = None
        self.prev_episode_step = 0
        self.viewport_width = WINDOW_WIDTH - STATS_PANEL_WIDTH
        self.zoom = 0.6
        self.camera_offset = [0, 0]
        self.has_save = os.path.exists(self.save_path)

        cx = self.viewport_width // 2
        cy = WINDOW_HEIGHT // 2
        self.menu_buttons = {
            "start": Button(cx - 90, cy - 50, 180, 42, "Start Game"),
            "continue": Button(cx - 90, cy + 5, 180, 42, "Continue"),
            "credits": Button(cx - 90, cy + 60, 180, 42, "Credits"),
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.scene == "menu":
                        self.running = False
                    else:
                        self.scene = "menu"
                        self.paused = True
                elif event.key == pygame.K_SPACE and self.scene == "play":
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.scene == "play":
                    self.world.reset_generation()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.scene == "play":
                if event.button == 1:
                    self._handle_world_click(event)
                elif event.button in (4, 5):  # scroll wheel
                    self._handle_zoom(1 if event.button == 4 else -1)
            elif event.type == pygame.MOUSEWHEEL and self.scene == "play":
                self._handle_zoom(event.y)

            if self.scene == "menu":
                self._handle_menu_event(event)
            else:
                actions = self.control_panel.handle_event(event)
                if actions.get("toggle_pause"):
                    self.paused = self.control_panel.paused
                if actions.get("reset_gen"):
                    self.world.reset_generation()
                    self.population_graph.add_reset_mark()
                if actions.get("reset_all"):
                    self.world.reset_all(self.control_panel.get_config_overrides())
                    self.population_graph.add_reset_mark()
                if actions.get("export"):
                    self._export_stats()
                if actions.get("trait_changed"):
                    self.trait_graph.title = self._current_trait_title()
                    self.trait_graph.update(self.world.populations.get("grazer", []), self._current_trait())
                if actions.get("event_armed"):
                    self.pending_event_type = actions["event_armed"]
                    self.log_panel.push(f"Armed {self.pending_event_type}. Click world to trigger.")

    def _handle_world_click(self, event):
        x, y = event.pos
        # Adjust for zoom and offset
        world_x = (x - self.camera_offset[0]) / self.zoom
        world_y = (y - self.camera_offset[1]) / self.zoom
        if world_x <= WORLD_WIDTH and world_y <= WORLD_HEIGHT and self.pending_event_type:
            self.world.apply_manual_event(self.pending_event_type, (world_x, world_y))
            self.log_panel.push(f"Manual event {self.pending_event_type} at ({int(world_x)}, {int(world_y)})")
            self.pending_event_type = None

    def update(self):
        if self.scene != "play":
            return
        if not self.paused:
            speed = int(self.control_panel.simulation_speed)
            for _ in range(max(1, speed)):
                self.world.update()
            self.update_counter += 1
            if self.update_counter % 10 == 0:
                self.population_graph.update(self.world)
                selected_trait = self._current_trait()
                self.trait_graph.title = self._current_trait_title()
                self.trait_graph.update(self.world.populations.get("grazer", []), selected_trait)
                self._pull_logs()
                self._detect_generation_reset()

        self.control_panel.update(self.world)

    def draw(self):
        self.screen.fill(UI_BG_COLOR)
        
        # Beautiful gradient background for world
        world_bg_top = (15, 20, 35)
        world_bg_bottom = (25, 30, 45)
        for y in range(WORLD_HEIGHT):
            ratio = y / WORLD_HEIGHT
            color = tuple(int(world_bg_top[i] + (world_bg_bottom[i] - world_bg_top[i]) * ratio) for i in range(3))
            pygame.draw.line(self.world_surface, color, (0, y), (WORLD_WIDTH, y))
        
        # Add subtle stars/particles in background
        import random
        random.seed(42)  # Consistent stars
        for _ in range(100):
            star_x = random.randint(0, WORLD_WIDTH)
            star_y = random.randint(0, WORLD_HEIGHT)
            brightness = random.randint(100, 200)
            pygame.draw.circle(self.world_surface, (brightness, brightness, brightness + 30), (star_x, star_y), 1)

        # Water zones overlay (sea vs river colors)
        for zx, zy, zw, zh, ztype in self.world.water_zones:
            water_rect = pygame.Rect(int(zx), int(zy), int(zw), int(zh))
            if ztype == "sea":
                color = SEA_COLOR
                accent = (min(255, SEA_COLOR[0] + 30), min(255, SEA_COLOR[1] + 30), min(255, SEA_COLOR[2] + 30))
            else:
                color = RIVER_COLOR
                accent = (min(255, RIVER_COLOR[0] + 40), min(255, RIVER_COLOR[1] + 40), min(255, RIVER_COLOR[2] + 40))
            pygame.draw.rect(self.world_surface, color, water_rect)
            for i in range(0, int(zh), 18):
                pygame.draw.line(self.world_surface, accent, (int(zx), int(zy + i)), (int(zx + zw), int(zy + i)), 1)

        for food in self.world.food:
            food.draw(self.world_surface)
        for rock in self.world.rocks:
            rock.draw(self.world_surface)
        for shelter in self.world.shelters:
            shelter.draw(self.world_surface)
        for agent in self.world.get_all_agents():
            agent.draw(self.world_surface)

        scaled_surface = pygame.transform.smoothscale(
            self.world_surface,
            (
                min(self.viewport_width, int(WORLD_WIDTH * self.zoom)),
                min(WINDOW_HEIGHT, int(WORLD_HEIGHT * self.zoom)),
            ),
        )
        
        # Clip world view to the viewport area
        self.screen.set_clip(pygame.Rect(0, 0, self.viewport_width, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, self.camera_offset)
        pygame.draw.rect(
            self.screen,
            UI_BORDER_COLOR,
            (
                self.camera_offset[0],
                self.camera_offset[1],
                min(self.viewport_width, int(WORLD_WIDTH * self.zoom)),
                min(WINDOW_HEIGHT, int(WORLD_HEIGHT * self.zoom)),
            ),
            2,
        )
        self.screen.set_clip(None) # Reset clip for UI

        # Draw a divider line
        pygame.draw.line(self.screen, UI_BORDER_COLOR, (self.viewport_width, 0), (self.viewport_width, WINDOW_HEIGHT), 2)

        self.control_panel.draw(self.screen)
        self.population_graph.draw(self.screen)
        self.trait_graph.draw(self.screen)
        self.log_panel.draw(self.screen)

        if self.scene == "menu":
            self._draw_menu()
        elif self.pending_event_type:
            self._draw_event_overlay()
            
        # Draw active event notification (Top Center)
        if self.world.active_event_text:
            self._draw_active_event()

        fps_font = pygame.font.Font(None, 20)
        fps_text = fps_font.render(f"FPS: {int(self.clock.get_fps())}", True, UI_TEXT_COLOR)
        self.screen.blit(fps_text, (10, 10))

        pygame.display.flip()

    def run(self):
        print("=" * 60)
        print("AI Evolving Animals Sandbox")
        print("=" * 60)
        print("\nControls:")
        print("  SPACE     - Pause/Resume")
        print("  R         - Reset generation")
        print("  ESC       - Quit / Back to menu")
        print("\nUI Controls:")
        print("  Speed slider - Adjust simulation speed")
        print("  Mutation/episode sliders - Evolution pacing")
        print("  Reset buttons - Restart generation or full run")
        print("\n" + "=" * 60)

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def _current_trait(self):
        return self.control_panel.get_selected_trait()

    def _current_trait_title(self):
        trait_name = self._current_trait().replace("_", " ").title()
        return f"Grazer {trait_name} Distribution"

    def _pull_logs(self):
        while self.world.extinction_log:
            msg = self.world.extinction_log.pop(0)
            self.log_panel.push(msg)

    def _export_stats(self):
        out_json = os.path.join(os.getcwd(), "generation_stats.json")
        out_csv = os.path.join(os.getcwd(), "generation_stats.csv")
        self.world.stats.export_json(out_json)
        self.world.stats.export_csv(out_csv)
        self.log_panel.push("Exported stats to CSV/JSON")

    def _handle_menu_event(self, event):
        for name, btn in self.menu_buttons.items():
            if btn.handle_event(event):
                if name == "start":
                    self._start_new_world()
                elif name == "continue":
                    if self._load_save():
                        self.scene = "play"
                        self.paused = False
                        self.started = True
                elif name == "credits":
                    self.show_credits = not self.show_credits

    def _start_new_world(self):
        self.world.reset_all(self.control_panel.get_config_overrides())
        self.zoom = 0.6
        self.camera_offset = [0, 0]
        self.scene = "play"
        self.paused = False
        self.started = True
        self.show_credits = False
        self.has_save = True

    def _draw_menu(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        # Dark semi-transparent overlay
        overlay.fill((25, 25, 40, 230))
        title_font = pygame.font.Font(None, 52)
        text_font = pygame.font.Font(None, 24)
        
        title = title_font.render("Evolving Animals Sandbox", True, UI_TEXT_COLOR)
        subtitle = text_font.render("Start a new world or continue the current run.", True, UI_TEXT_COLOR)
        
        cx = self.viewport_width // 2
        cy = WINDOW_HEIGHT // 2
        
        overlay.blit(title, (cx - title.get_width() // 2, cy - 140))
        overlay.blit(subtitle, (cx - subtitle.get_width() // 2, cy - 110))
        
        for btn in self.menu_buttons.values():
            if btn.text == "Continue" and not self.has_save:
                # Dim continue if no save
                btn.color = UI_PANEL_BG
                btn.text_color = (130, 130, 130)
            else:
                btn.color = UI_PANEL_BG
                btn.text_color = UI_TEXT_COLOR
            btn.draw(overlay, text_font)
            
        if self.show_credits:
            credits = [
                "Credits",
                "Design & Code: You",
                "Inspired by evolutionary ecosystems",
                "Thanks for playing!",
            ]
            for i, line in enumerate(credits):
                txt = text_font.render(line, True, UI_TEXT_COLOR)
                overlay.blit(txt, (cx - txt.get_width() // 2, cy + 120 + i * 22))
        self.screen.blit(overlay, (0, 0))

    def _draw_event_overlay(self):
        overlay = pygame.Surface((self.viewport_width, 40), pygame.SRCALPHA)
        overlay.fill((40, 42, 54, 200))
        font = pygame.font.Font(None, 24)
        msg = font.render(f"Armed event: {self.pending_event_type} — click on the world to trigger", True, UI_TEXT_COLOR)
        overlay.blit(msg, (10, 10))
        self.screen.blit(overlay, (0, 0))

    def _draw_active_event(self):
        """Draw big red text at top for active events."""
        font = pygame.font.Font(None, 64)
        # Add shadow
        text = self.world.active_event_text
        shadow = font.render(text, True, (0, 0, 0))
        fg = font.render(text, True, (255, 85, 85)) # Red
        
        cx = self.viewport_width // 2
        cy = 100

        shadow_rect = shadow.get_rect(center=(cx + 2, cy + 2))
        fg_rect = fg.get_rect(center=(cx, cy))
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(fg, fg_rect)

    def _handle_zoom(self, direction):
        self.zoom = max(0.25, min(2.5, self.zoom + direction * 0.1))
        self.camera_offset = [
            max(-WORLD_WIDTH, min(WORLD_WIDTH, self.camera_offset[0])),
            max(-WORLD_HEIGHT, min(WORLD_HEIGHT, self.camera_offset[1])),
        ]

    def _detect_generation_reset(self):
        if self.world.episode_step == 0 and self.prev_episode_step > 0:
            self.population_graph.add_reset_mark()
        self.prev_episode_step = self.world.episode_step

    def _load_save(self):
        loaded = self.world.load_state(self.save_path)
        self.has_save = loaded
        if loaded:
            self.zoom = 0.6
            self.camera_offset = [0, 0]
        return loaded


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
