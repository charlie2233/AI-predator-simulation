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
    UI_BG_COLOR,
    UI_PANEL_BG,
    UI_TEXT_COLOR,
    UI_BORDER_COLOR,
    UI_ACCENT_COLOR
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
        self.trait_options = ["speed", "vision", "energy_efficiency", "size", "bravery", "metabolism"]
        self.trait_index = 0

        self.buttons = {}
        self.sliders = {}
        self.labels = {}
        self.inputs = {}
        self.event_selection = None

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
        # Clear existing UI elements if re-initializing
        self.buttons = {}
        self.sliders = {}
        self.labels = {}
        self.inputs = {}

        x_padding = UI_PADDING + 10
        y_start = self.rect.y + UI_PADDING + 10
        
        # --- Title ---
        self.labels["title"] = Label(self.rect.x + x_padding, y_start, "Control Panel", UI_ACCENT_COLOR, UI_TITLE_FONT_SIZE + 4)
        y = y_start + 40

        # --- Live Stats Group ---
        # We'll render these dynamically in draw(), but let's place static labels
        self.labels["stats_title"] = Label(self.rect.x + x_padding, y, "Live Stats", UI_TEXT_COLOR, UI_FONT_SIZE + 2)
        y += 25
        self.labels["generation"] = Label(self.rect.x + x_padding, y, "Generation: 1", UI_TEXT_COLOR)
        y += 20
        self.labels["time_step"] = Label(self.rect.x + x_padding, y, "Step: 0", UI_TEXT_COLOR)
        y += 20
        self.labels["food_count"] = Label(self.rect.x + x_padding, y, "Food: 0", UI_TEXT_COLOR)
        y += 25
        # Run Stats
        self.labels["run_stats"] = Label(self.rect.x + x_padding, y, "Runs: 1 | Extinctions: 0", UI_ACCENT_COLOR, 16)
        y += 25
        
        # Population counts in a grid-like fashion
        self.labels["populations"] = {}
        col_x = self.rect.x + x_padding
        for i, species in enumerate(self.initial_counts.keys()):
            self.labels["populations"][species] = Label(col_x, y, f"{species.title()}: 0", UI_TEXT_COLOR)
            if i % 2 == 1:
                y += 20
                col_x = self.rect.x + x_padding
            else:
                col_x = self.rect.x + x_padding + 120
        
        if len(self.initial_counts) % 2 != 0:
            y += 20

        # Divider
        y += 10
        # self.dividers.append(y) # If we had a divider component
        
        # --- Controls ---
        y += 10
        self.buttons["pause"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, "Pause", UI_PANEL_BG)
        self.buttons["reset_gen"] = Button(self.rect.x + x_padding + UI_BUTTON_WIDTH + 10, y, UI_BUTTON_WIDTH + 20, UI_BUTTON_HEIGHT, "Reset Gen", UI_PANEL_BG)
        y += UI_BUTTON_HEIGHT + 10
        self.buttons["reset_all"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, "Reset All", UI_PANEL_BG)
        self.buttons["export"] = Button(self.rect.x + x_padding + UI_BUTTON_WIDTH + 10, y, UI_BUTTON_WIDTH + 20, UI_BUTTON_HEIGHT, "Export Stats", UI_PANEL_BG)
        y += UI_BUTTON_HEIGHT + 20

        # --- Sliders ---
        self.sliders["speed"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 0.1, 5.0, 1.0, "Sim Speed")
        y += UI_SLIDER_HEIGHT + 25
        self.sliders["mutation"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 0.01, 0.5, self.mutation_strength, "Mutation σ")
        y += UI_SLIDER_HEIGHT + 25
        self.sliders["episode"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 200, 2000, self.episode_length, "Episode Steps")
        y += UI_SLIDER_HEIGHT + 25
        self.sliders["food"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 0.0, 0.1, self.food_spawn_rate, "Food Spawn")
        y += UI_SLIDER_HEIGHT + 30

        # --- Trait View ---
        self.labels["trait_label"] = Label(self.rect.x + x_padding, y, self._trait_label_text(), UI_TEXT_COLOR)
        y += 20
        self.buttons["trait_cycle"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT, "Cycle Trait", UI_PANEL_BG)
        y += UI_BUTTON_HEIGHT + 20

        # --- Events ---
        self.labels["event_title"] = Label(self.rect.x + x_padding, y, "God Mode (Events)", UI_TEXT_COLOR)
        y += 25
        btn_w = (self.rect.width - 40) // 3
        self.buttons["ev_quake"] = Button(self.rect.x + x_padding, y, btn_w, UI_BUTTON_HEIGHT, "Quake", UI_PANEL_BG)
        self.buttons["ev_tsunami"] = Button(self.rect.x + x_padding + btn_w + 5, y, btn_w, UI_BUTTON_HEIGHT, "Wave", UI_PANEL_BG)
        self.buttons["ev_meteor"] = Button(self.rect.x + x_padding + (btn_w + 5) * 2, y, btn_w, UI_BUTTON_HEIGHT, "Meteor", UI_PANEL_BG)
        y += UI_BUTTON_HEIGHT + 10
        self.labels["event_hint"] = Label(self.rect.x + x_padding, y, "Click world to drop event", UI_TEXT_COLOR, 14)
        y += 20

        # --- World Config (Collapsible/Small) ---
        self.buttons["obstacles"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT, "Toggle Obstacles", UI_PANEL_BG)
        y += UI_BUTTON_HEIGHT + 20

        # We skip population inputs for now to save space, or make them very compact if needed.
        # But let's add them back compactly
        self.labels["pop_title"] = Label(self.rect.x + x_padding, y, "Initial Config", UI_TEXT_COLOR)
        y += 25
        col_x = self.rect.x + x_padding
        for i, (species, val) in enumerate(self.initial_counts.items()):
            self.inputs[f"count_{species}"] = NumericInput(col_x, y, 70, 24, val, label=species[:3].title(), min_val=0, max_val=400)
            if i % 3 == 2:
                y += 45
                col_x = self.rect.x + x_padding
            else:
                col_x += 85
        
        if len(self.initial_counts) % 3 != 0:
            y += 45
            
        # World Dimensions
        self.inputs["world_w"] = NumericInput(self.rect.x + x_padding, y, 80, 24, self.world_width, label="W", min_val=200, max_val=2000)
        self.inputs["world_h"] = NumericInput(self.rect.x + x_padding + 90, y, 80, 24, self.world_height, label="H", min_val=200, max_val=2000)


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
        if self.buttons["ev_quake"].handle_event(event):
            self.event_selection = "earthquake"
            actions["event_armed"] = "earthquake"
        if self.buttons["ev_tsunami"].handle_event(event):
            self.event_selection = "tsunami"
            actions["event_armed"] = "tsunami"
        if self.buttons["ev_meteor"].handle_event(event):
            self.event_selection = "meteor"
            actions["event_armed"] = "meteor"

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
        
        # Update run stats
        if hasattr(world, "run_history"):
            s = world.run_history["starts"]
            e = world.run_history["extinctions"]
            self.labels["run_stats"].set_text(f"Runs: {s} | Extinctions: {e}")

        if self.event_selection:
            self.labels["event_hint"].set_text(f"ARMED: {self.event_selection.upper()}!")
            self.labels["event_hint"].color = UI_ACCENT_COLOR
        else:
            self.labels["event_hint"].set_text("Click world to drop event")
            self.labels["event_hint"].color = UI_TEXT_COLOR

    def draw(self, surface):
        if not self.font:
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)
            
        # Main background
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2)

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
        return f"Trait: {trait_name}"

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
