"""
Main simulation runner with pygame interface and a front menu scene.
"""
import os
import pygame
import sys
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
)


class Simulation:
    """Main simulation controller with menu + play scenes."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Evolving Animals Sandbox")

        self.world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.clock = pygame.time.Clock()
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)

        self.control_panel = ControlPanel(WORLD_WIDTH + 10, 10, STATS_PANEL_WIDTH - 20, WINDOW_HEIGHT - 20)
        self.population_graph = PopulationGraph(
            WORLD_WIDTH + 10, 420, STATS_PANEL_WIDTH - 20, 140, species_names=list(SPECIES_STYLE.keys())
        )
        self.trait_graph = TraitGraph(WORLD_WIDTH + 10, 580, STATS_PANEL_WIDTH - 20, 110, self._current_trait_title())
        self.log_panel = LogPanel(WORLD_WIDTH + 10, 700, STATS_PANEL_WIDTH - 20, 50)

        self.running = True
        self.paused = True
        self.started = False
        self.scene = "menu"  # menu | play
        self.show_credits = False
        self.update_counter = 0

        cx = WORLD_WIDTH // 2 - 90
        cy = WORLD_HEIGHT // 2
        self.menu_buttons = {
            "start": Button(cx, cy - 50, 180, 42, "Start Game"),
            "continue": Button(cx, cy + 5, 180, 42, "Continue"),
            "credits": Button(cx, cy + 60, 180, 42, "Credits"),
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

            if self.scene == "menu":
                self._handle_menu_event(event)
            else:
                actions = self.control_panel.handle_event(event)
                if actions.get("toggle_pause"):
                    self.paused = self.control_panel.paused
                if actions.get("reset_gen"):
                    self.world.reset_generation()
                if actions.get("reset_all"):
                    self.world.reset_all(self.control_panel.get_config_overrides())
                if actions.get("export"):
                    self._export_stats()
                if actions.get("trait_changed"):
                    self.trait_graph.title = self._current_trait_title()
                    self.trait_graph.update(self.world.populations.get("grazer", []), self._current_trait())

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

        self.control_panel.update(self.world)

    def draw(self):
        self.screen.fill(BLACK)
        self.world_surface.fill(BLACK)

        for food in self.world.food:
            food.draw(self.world_surface)
        for rock in self.world.rocks:
            rock.draw(self.world_surface)
        for shelter in self.world.shelters:
            shelter.draw(self.world_surface)
        for agent in self.world.get_all_agents():
            agent.draw(self.world_surface)

        self.screen.blit(self.world_surface, (0, 0))
        pygame.draw.rect(self.screen, WHITE, (0, 0, WORLD_WIDTH, WORLD_HEIGHT), 2)

        self.control_panel.draw(self.screen)
        self.population_graph.draw(self.screen)
        self.trait_graph.draw(self.screen)
        self.log_panel.draw(self.screen)

        if self.scene == "menu":
            self._draw_menu()

        fps_font = pygame.font.Font(None, 20)
        fps_text = fps_font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
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
                    self.scene = "play"
                    self.paused = False
                    self.started = True
                elif name == "credits":
                    self.show_credits = not self.show_credits

    def _start_new_world(self):
        self.world.reset_all(self.control_panel.get_config_overrides())
        self.scene = "play"
        self.paused = False
        self.started = True
        self.show_credits = False

    def _draw_menu(self):
        overlay = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 25, 220))
        title_font = pygame.font.Font(None, 52)
        text_font = pygame.font.Font(None, 24)
        title = title_font.render("Evolving Animals Sandbox", True, WHITE)
        subtitle = text_font.render("Start a new world or continue the current run.", True, WHITE)
        overlay.blit(title, (WORLD_WIDTH // 2 - title.get_width() // 2, WORLD_HEIGHT // 2 - 140))
        overlay.blit(subtitle, (WORLD_WIDTH // 2 - subtitle.get_width() // 2, WORLD_HEIGHT // 2 - 110))
        for btn in self.menu_buttons.values():
            btn.draw(overlay, text_font)
        if self.show_credits:
            credits = [
                "Credits",
                "Design & Code: You",
                "Inspired by evolutionary ecosystems",
                "Thanks for playing!",
            ]
            for i, line in enumerate(credits):
                txt = text_font.render(line, True, WHITE)
                overlay.blit(txt, (WORLD_WIDTH // 2 - txt.get_width() // 2, WORLD_HEIGHT // 2 + 120 + i * 22))
        self.screen.blit(overlay, (0, 0))


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
