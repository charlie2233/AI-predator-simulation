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
        self.tabs = ["World", "Evolution"]
        self.active_tab = "World"
        self.tab_content = {tab: {"buttons": set(), "sliders": set(), "inputs": set(), "labels": set()} for tab in self.tabs}
        self.always_visible = {"buttons": set(), "sliders": set(), "inputs": set(), "labels": set()}

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
        self.tab_content = {tab: {"buttons": set(), "sliders": set(), "inputs": set(), "labels": set()} for tab in self.tabs}
        self.always_visible = {k: set() for k in self.always_visible.keys()}

        x_padding = UI_PADDING + 10
        y_start = self.rect.y + UI_PADDING + 10
        
        # --- Title ---
        self.labels["title"] = Label(self.rect.x + x_padding, y_start, "Control Panel", UI_ACCENT_COLOR, UI_TITLE_FONT_SIZE + 4)
        self._register("labels", "title", always=True)
        y = y_start + 40

        # --- Tabs ---
        tab_w = 110
        tab_h = UI_BUTTON_HEIGHT - 6
        self.buttons["tab_world"] = Button(self.rect.x + x_padding, y, tab_w, tab_h, "World")
        self.buttons["tab_evo"] = Button(self.rect.x + x_padding + tab_w + 8, y, tab_w, tab_h, "Evolution")
        self._register("buttons", "tab_world", always=True)
        self._register("buttons", "tab_evo", always=True)
        y += tab_h + 14

        # --- Live Stats Group ---
        # We'll render these dynamically in draw(), but let's place static labels
        self.labels["stats_title"] = Label(self.rect.x + x_padding, y, "Live Stats", UI_TEXT_COLOR, UI_FONT_SIZE + 2)
        self._register("labels", "stats_title", always=True)
        y += 25
        self.labels["generation"] = Label(self.rect.x + x_padding, y, "Generation: 1", UI_TEXT_COLOR)
        self._register("labels", "generation", always=True)
        y += 20
        self.labels["time_step"] = Label(self.rect.x + x_padding, y, "Step: 0", UI_TEXT_COLOR)
        self._register("labels", "time_step", always=True)
        y += 20
        self.labels["food_count"] = Label(self.rect.x + x_padding, y, "Food: 0", UI_TEXT_COLOR)
        self._register("labels", "food_count", always=True)
        y += 25
        # Run Stats
        self.labels["run_stats"] = Label(self.rect.x + x_padding, y, "Runs: 1 | Extinctions: 0", UI_ACCENT_COLOR, 16)
        self._register("labels", "run_stats", always=True)
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
        self._register("buttons", "pause", always=True)
        self.buttons["reset_gen"] = Button(self.rect.x + x_padding + UI_BUTTON_WIDTH + 10, y, UI_BUTTON_WIDTH + 20, UI_BUTTON_HEIGHT, "Reset Gen", UI_PANEL_BG)
        self._register("buttons", "reset_gen", always=True)
        y += UI_BUTTON_HEIGHT + 10
        self.buttons["reset_all"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, "Reset All", UI_PANEL_BG)
        self._register("buttons", "reset_all", always=True)
        self.buttons["export"] = Button(self.rect.x + x_padding + UI_BUTTON_WIDTH + 10, y, UI_BUTTON_WIDTH + 20, UI_BUTTON_HEIGHT, "Export Stats", UI_PANEL_BG)
        self._register("buttons", "export", always=True)
        y += UI_BUTTON_HEIGHT + 20

        # --- Sliders ---
        self.sliders["speed"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 0.1, 5.0, 1.0, "Sim Speed")
        self._register("sliders", "speed", tab="World")
        y += UI_SLIDER_HEIGHT + 25
        self.sliders["mutation"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 0.01, 0.5, self.mutation_strength, "Mutation σ")
        self._register("sliders", "mutation", tab="Evolution")
        y += UI_SLIDER_HEIGHT + 25
        self.sliders["episode"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 200, 2000, self.episode_length, "Episode Steps")
        self._register("sliders", "episode", tab="Evolution")
        y += UI_SLIDER_HEIGHT + 25
        self.sliders["food"] = Slider(self.rect.x + x_padding, y, UI_SLIDER_WIDTH + 80, UI_SLIDER_HEIGHT, 0.0, 0.1, self.food_spawn_rate, "Food Spawn")
        self._register("sliders", "food", tab="World")
        y += UI_SLIDER_HEIGHT + 30

        # --- Trait View ---
        self.labels["trait_label"] = Label(self.rect.x + x_padding, y, self._trait_label_text(), UI_TEXT_COLOR)
        self._register("labels", "trait_label", tab="Evolution")
        y += 20
        self.buttons["trait_cycle"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT, "Cycle Trait", UI_PANEL_BG)
        self._register("buttons", "trait_cycle", tab="Evolution")
        y += UI_BUTTON_HEIGHT + 20

        # --- Events ---
        self.labels["event_title"] = Label(self.rect.x + x_padding, y, "God Mode (Events)", UI_TEXT_COLOR)
        self._register("labels", "event_title", tab="World")
        y += 25
        btn_w = (self.rect.width - 40) // 3
        self.buttons["ev_quake"] = Button(self.rect.x + x_padding, y, btn_w, UI_BUTTON_HEIGHT, "Quake", UI_PANEL_BG)
        self._register("buttons", "ev_quake", tab="World")
        self.buttons["ev_tsunami"] = Button(self.rect.x + x_padding + btn_w + 5, y, btn_w, UI_BUTTON_HEIGHT, "Wave", UI_PANEL_BG)
        self._register("buttons", "ev_tsunami", tab="World")
        self.buttons["ev_meteor"] = Button(self.rect.x + x_padding + (btn_w + 5) * 2, y, btn_w, UI_BUTTON_HEIGHT, "Meteor", UI_PANEL_BG)
        self._register("buttons", "ev_meteor", tab="World")
        y += UI_BUTTON_HEIGHT + 10
        self.labels["event_hint"] = Label(self.rect.x + x_padding, y, "Click world to drop event", UI_TEXT_COLOR, 14)
        self._register("labels", "event_hint", tab="World")
        y += 20

        # --- World Config (Collapsible/Small) ---
        self.buttons["obstacles"] = Button(self.rect.x + x_padding, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT, "Toggle Obstacles", UI_PANEL_BG)
        self._register("buttons", "obstacles", tab="World")
        y += UI_BUTTON_HEIGHT + 20

        # We skip population inputs for now to save space, or make them very compact if needed.
        # But let's add them back compactly
        self.labels["pop_title"] = Label(self.rect.x + x_padding, y, "Initial Config", UI_TEXT_COLOR)
        self._register("labels", "pop_title", tab="Evolution")
        y += 25
        col_x = self.rect.x + x_padding
        for i, (species, val) in enumerate(self.initial_counts.items()):
            self.inputs[f"count_{species}"] = NumericInput(col_x, y, 70, 24, val, label=species[:3].title(), min_val=0, max_val=400)
            self._register("inputs", f"count_{species}", tab="Evolution")
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
        self._register("inputs", "world_w", tab="World")
        self._register("inputs", "world_h", tab="World")


    def handle_event(self, event):
        actions = {}
        if self._button_clicked("tab_world", event):
            self.active_tab = "World"
        if self._button_clicked("tab_evo", event):
            self.active_tab = "Evolution"
        if self._button_clicked("pause", event):
            self.paused = not self.paused
            self.buttons["pause"].text = "Resume" if self.paused else "Pause"
            actions["toggle_pause"] = True
        if self._button_clicked("reset_gen", event):
            actions["reset_gen"] = True
        if self._button_clicked("reset_all", event):
            actions["reset_all"] = True
        if self._button_clicked("export", event):
            actions["export"] = True
        if self._button_clicked("trait_cycle", event):
            self.trait_index = (self.trait_index + 1) % len(self.trait_options)
            self.labels["trait_label"].set_text(self._trait_label_text())
            actions["trait_changed"] = True
        if self._button_clicked("obstacles", event):
            self.obstacles_enabled = not self.obstacles_enabled
            actions["obstacles_toggled"] = True
        if self._button_clicked("ev_quake", event):
            self.event_selection = "earthquake"
            actions["event_armed"] = "earthquake"
        if self._button_clicked("ev_tsunami", event):
            self.event_selection = "tsunami"
            actions["event_armed"] = "tsunami"
        if self._button_clicked("ev_meteor", event):
            self.event_selection = "meteor"
            actions["event_armed"] = "meteor"

        for key, slider in self.sliders.items():
            if self._is_visible("sliders", key):
                slider.handle_event(event)
        for key, input_box in self.inputs.items():
            if self._is_visible("inputs", key):
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

        for key, label in self.labels.items():
            if isinstance(label, dict):
                continue
            if not self._is_visible("labels", key):
                continue
            if hasattr(label, "font_size") and label.font_size > UI_FONT_SIZE:
                label.draw(surface, self.title_font)
            else:
                label.draw(surface, self.font)
                
        for lbl in self.labels.get("populations", {}).values():
            lbl.draw(surface, self.font)

        for key, button in self.buttons.items():
            if key.startswith("tab_"):
                if (self.active_tab == "World" and key == "tab_world") or (self.active_tab == "Evolution" and key == "tab_evo"):
                    button.color = UI_ACCENT_COLOR
                    button.text_color = UI_BG_COLOR
                else:
                    button.color = UI_PANEL_BG
                    button.text_color = UI_TEXT_COLOR
            if key.startswith("tab_") or self._is_visible("buttons", key):
                button.draw(surface, self.font)
        for key, slider in self.sliders.items():
            if self._is_visible("sliders", key):
                slider.draw(surface, self.font)
        for key, input_box in self.inputs.items():
            if self._is_visible("inputs", key):
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

    # --- Helpers ---
    def _register(self, kind, key, tab=None, always=False):
        if always:
            self.always_visible[kind].add(key)
        elif tab:
            self.tab_content[tab][kind].add(key)

    def _is_visible(self, kind, key):
        return key in self.always_visible.get(kind, set()) or key in self.tab_content[self.active_tab].get(kind, set())

    def _button_clicked(self, key, event):
        if key not in self.buttons:
            return False
        if not (key.startswith("tab_") or self._is_visible("buttons", key)):
            return False
        return self.buttons[key].handle_event(event)
