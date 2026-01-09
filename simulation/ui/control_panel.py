"""
Control panel for simulation settings.
"""
import pygame
from simulation.ui.components import Button, Slider, Label, NumericInput
from simulation.config import (
    WHITE,
    BLACK,
    DARK_GRAY,
    UI_PADDING,
    UI_BUTTON_WIDTH,
    UI_BUTTON_HEIGHT,
    UI_SLIDER_WIDTH,
    UI_SLIDER_HEIGHT,
    UI_FONT_SIZE,
    UI_TITLE_FONT_SIZE,
    INITIAL_SPECIES_COUNTS,
    EPISODE_LENGTH_STEPS,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    FOOD_RESPAWN_RATE,
    MUTATION_SIGMA,
)


class ControlPanel:
    """Control panel for adjusting simulation parameters."""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = None
        self.title_font = None

        # Control state
        self.paused = False
        self.show_vision = False
        self.simulation_speed = 1.0
        self.trait_options = ["speed", "vision", "energy_efficiency", "size"]
        self.trait_index = 0

        self.buttons = {}
        self.sliders = {}
        self.labels = {}
        self.inputs = {}

        # Cached values for resets
        self.initial_counts = dict(INITIAL_SPECIES_COUNTS)
        self.episode_length = EPISODE_LENGTH_STEPS
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        self.food_spawn_rate = FOOD_RESPAWN_RATE
        self.mutation_strength = MUTATION_SIGMA
        self.obstacles_enabled = False

        self.setup_ui()

    def setup_ui(self):
        x = self.rect.x + UI_PADDING
        y = self.rect.y + UI_PADDING + 20

        self.labels["title"] = Label(x, self.rect.y + UI_PADDING, "Control Panel", WHITE, UI_TITLE_FONT_SIZE)

        # Control buttons
        self.buttons["pause"] = Button(x, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, "Pause", DARK_GRAY)
        y += UI_BUTTON_HEIGHT + UI_PADDING
        self.buttons["reset_gen"] = Button(x, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT, "Reset Generation", DARK_GRAY)
        y += UI_BUTTON_HEIGHT + UI_PADDING
        self.buttons["reset_all"] = Button(x, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, "Reset All", DARK_GRAY)
        y += UI_BUTTON_HEIGHT + UI_PADDING
        self.buttons["export"] = Button(x, y, UI_BUTTON_WIDTH + 20, UI_BUTTON_HEIGHT, "Export Stats", DARK_GRAY)
        y += UI_BUTTON_HEIGHT + UI_PADDING

        # Toggles and sliders
        self.sliders["speed"] = Slider(x, y, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT, 0.1, 5.0, 1.0, "Speed")
        y += UI_SLIDER_HEIGHT + UI_PADDING
        self.sliders["mutation"] = Slider(x, y, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT, 0.01, 0.5, self.mutation_strength, "Mutation σ")
        y += UI_SLIDER_HEIGHT + UI_PADDING
        self.sliders["episode"] = Slider(x, y, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT, 200, 2000, self.episode_length, "Episode Steps")
        y += UI_SLIDER_HEIGHT + UI_PADDING
        self.sliders["food"] = Slider(x, y, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT, 0.0, 0.1, self.food_spawn_rate, "Food Spawn")
        y += UI_SLIDER_HEIGHT + UI_PADDING

        # Species inputs
        self.labels["pop_title"] = Label(x, y, "Initial Populations", WHITE, UI_FONT_SIZE)
        y += 22
        for species, val in self.initial_counts.items():
            self.inputs[f"count_{species}"] = NumericInput(x, y, 80, 26, val, label=species.title(), min_val=0, max_val=400)
            y += 32

        # World inputs
        y += UI_PADDING
        self.labels["world"] = Label(x, y, "World", WHITE, UI_FONT_SIZE)
        y += 22
        self.inputs["world_w"] = NumericInput(x, y, 100, 26, self.world_width, label="Width", min_val=200, max_val=2000)
        y += 32
        self.inputs["world_h"] = NumericInput(x, y, 100, 26, self.world_height, label="Height", min_val=200, max_val=2000)
        y += 32
        self.buttons["obstacles"] = Button(x, y, UI_BUTTON_WIDTH + 20, UI_BUTTON_HEIGHT, "Toggle Obstacles", DARK_GRAY)
        y += UI_BUTTON_HEIGHT + UI_PADDING

        # Trait selector
        self.labels["trait_label"] = Label(x, y, self._trait_label_text(), WHITE)
        y += 20
        self.buttons["trait_cycle"] = Button(x, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT, "Next Trait", DARK_GRAY)
        y += UI_BUTTON_HEIGHT + UI_PADDING

        # Stats labels
        self.labels["stats_title"] = Label(x, y, "Live Stats", WHITE, UI_FONT_SIZE)
        y += 22
        self.labels["generation"] = Label(x, y, "Generation: 1", WHITE)
        y += 20
        self.labels["time_step"] = Label(x, y, "Step: 0", WHITE)
        y += 20
        self.labels["populations"] = {}
        for species in self.initial_counts.keys():
            self.labels["populations"][species] = Label(x, y, f"{species.title()}: 0", WHITE)
            y += 18
        self.labels["food_count"] = Label(x, y, "Food: 0", WHITE)

    def handle_event(self, event):
        actions = {}
        if self.buttons["pause"].handle_event(event):
            self.paused = not self.paused
            self.buttons["pause"].text = "Resume" if self.paused else "Pause"
            actions["toggle_pause"] = True
        if self.buttons["reset_gen"].handle_event(event):
            actions["reset_gen"] = True
        if self.buttons["reset_all"].handle_event(event):
            actions["reset_all"] = True
        if self.buttons["export"].handle_event(event):
            actions["export"] = True
        if self.buttons["trait_cycle"].handle_event(event):
            self.trait_index = (self.trait_index + 1) % len(self.trait_options)
            self.labels["trait_label"].set_text(self._trait_label_text())
            actions["trait_changed"] = True
        if self.buttons["obstacles"].handle_event(event):
            self.obstacles_enabled = not self.obstacles_enabled
            actions["obstacles_toggled"] = True

        for slider in self.sliders.values():
            slider.handle_event(event)
        for input_box in self.inputs.values():
            input_box.handle_event(event)

        self.simulation_speed = self.sliders["speed"].value
        self.mutation_strength = self.sliders["mutation"].value
        self.episode_length = int(self.sliders["episode"].value)
        self.food_spawn_rate = self.sliders["food"].value
        return actions

    def update(self, world):
        self.labels["generation"].set_text(f"Generation: {world.generation}")
        self.labels["time_step"].set_text(f"Step: {world.episode_step}/{world.episode_length}")
        for species, lbl in self.labels["populations"].items():
            lbl.set_text(f"{species.title()}: {len(world.populations.get(species, []))}")
        self.labels["food_count"].set_text(f"Food: {len(world.food)}")

    def draw(self, surface):
        if not self.font:
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)
        pygame.draw.rect(surface, BLACK, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        for label in self.labels.values():
            if isinstance(label, dict):
                continue
            if hasattr(label, "font_size") and label.font_size > UI_FONT_SIZE:
                label.draw(surface, self.title_font)
            else:
                label.draw(surface, self.font)
        for lbl in self.labels.get("populations", {}).values():
            lbl.draw(surface, self.font)

        for button in self.buttons.values():
            button.draw(surface, self.font)
        for slider in self.sliders.values():
            slider.draw(surface, self.font)
        for input_box in self.inputs.values():
            input_box.draw(surface, self.font)

    def get_selected_trait(self):
        return self.trait_options[self.trait_index]

    def _trait_label_text(self):
        trait_name = self.get_selected_trait().replace("_", " ").title()
        return f"Trait Graph: {trait_name}"

    def get_config_overrides(self):
        counts = {k.split("_", 1)[1]: box.value for k, box in self.inputs.items() if k.startswith("count_")}
        self.world_width = self.inputs["world_w"].value
        self.world_height = self.inputs["world_h"].value
        return {
            "initial_counts": counts,
            "world_width": self.world_width,
            "world_height": self.world_height,
            "episode_length": self.episode_length,
            "food_respawn_rate": self.food_spawn_rate,
            "mutation_sigma": self.mutation_strength,
            "obstacles_enabled": self.obstacles_enabled,
        }
