"""
Control panel for simulation settings.
"""
import pygame
from simulation.ui.components import Button, Slider, Label
from simulation.config import (
    WHITE, BLACK, DARK_GRAY,
    UI_PADDING, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT,
    UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT, UI_FONT_SIZE, UI_TITLE_FONT_SIZE,
    STATS_PANEL_WIDTH
)


class ControlPanel:
    """Control panel for adjusting simulation parameters."""
    
    def __init__(self, x, y, width, height):
        """
        Initialize control panel.
        
        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = None
        self.title_font = None
        
        # Control state
        self.paused = False
        self.show_vision = False
        self.simulation_speed = 1.0
        self.trait_options = ['speed', 'vision', 'energy_efficiency', 'size']
        self.trait_index = 0
        
        # UI elements
        self.buttons = {}
        self.sliders = {}
        self.labels = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create UI elements."""
        x = self.rect.x + UI_PADDING
        y = self.rect.y + UI_PADDING + 40
        
        # Title
        self.labels['title'] = Label(x, self.rect.y + UI_PADDING, "Control Panel", WHITE, UI_TITLE_FONT_SIZE)
        
        # Buttons
        self.buttons['pause'] = Button(
            x, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT,
            "Pause", DARK_GRAY
        )
        y += UI_BUTTON_HEIGHT + UI_PADDING
        
        self.buttons['reset'] = Button(
            x, y, UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT,
            "Reset", DARK_GRAY
        )
        y += UI_BUTTON_HEIGHT + UI_PADDING * 2
        
        # Speed slider
        self.sliders['speed'] = Slider(
            x, y, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT,
            0.1, 5.0, 1.0, "Speed"
        )
        y += UI_SLIDER_HEIGHT + UI_PADDING * 2
        
        # Trait graph selector
        self.labels['trait_label'] = Label(x, y, self._trait_label_text(), WHITE)
        y += 20
        self.buttons['trait_cycle'] = Button(
            x, y, UI_BUTTON_WIDTH + 40, UI_BUTTON_HEIGHT,
            "Next Trait", DARK_GRAY
        )
        y += UI_BUTTON_HEIGHT + UI_PADDING * 2
        
        # Statistics labels
        self.labels['stats_title'] = Label(x, y, "Statistics", WHITE, UI_FONT_SIZE)
        y += 25
        
        self.labels['prey_count'] = Label(x, y, "Prey: 0", WHITE)
        y += 20
        
        self.labels['predator_count'] = Label(x, y, "Predators: 0", WHITE)
        y += 20
        
        self.labels['food_count'] = Label(x, y, "Food: 0", WHITE)
        y += 20
        
        self.labels['time_step'] = Label(x, y, "Time: 0", WHITE)
        y += 30
        
        # Evolution stats
        self.labels['evolution_title'] = Label(x, y, "Evolution", WHITE, UI_FONT_SIZE)
        y += 25
        
        self.labels['prey_avg_speed'] = Label(x, y, "Prey Speed: 0.0", WHITE)
        y += 20
        
        self.labels['prey_avg_vision'] = Label(x, y, "Prey Vision: 0.0", WHITE)
        y += 20
        
        self.labels['pred_avg_speed'] = Label(x, y, "Pred Speed: 0.0", WHITE)
        y += 20
        
        self.labels['pred_avg_vision'] = Label(x, y, "Pred Vision: 0.0", WHITE)
    
    def handle_event(self, event):
        """
        Handle UI events.
        
        Args:
            event: Pygame event
            
        Returns:
            Dictionary of actions triggered
        """
        actions = {}
        
        # Handle buttons
        if self.buttons['pause'].handle_event(event):
            self.paused = not self.paused
            self.buttons['pause'].text = "Resume" if self.paused else "Pause"
            actions['toggle_pause'] = True
        
        if self.buttons['reset'].handle_event(event):
            actions['reset'] = True
        
        if self.buttons['trait_cycle'].handle_event(event):
            self.trait_index = (self.trait_index + 1) % len(self.trait_options)
            self.labels['trait_label'].set_text(self._trait_label_text())
            actions['trait_changed'] = True
        
        # Handle sliders
        for slider in self.sliders.values():
            slider.handle_event(event)
        
        # Update simulation speed
        self.simulation_speed = self.sliders['speed'].value
        
        return actions
    
    def update(self, world):
        """
        Update panel with current simulation state.
        
        Args:
            world: World instance
        """
        # Update statistics
        self.labels['prey_count'].set_text(f"Prey: {len(world.prey)}")
        self.labels['predator_count'].set_text(f"Predators: {len(world.predators)}")
        self.labels['food_count'].set_text(f"Food: {len(world.food)}")
        self.labels['time_step'].set_text(f"Time: {world.time_step}")
        
        # Update evolution statistics
        if world.prey:
            avg_prey_speed = sum(p.traits.speed for p in world.prey) / len(world.prey)
            avg_prey_vision = sum(p.traits.vision for p in world.prey) / len(world.prey)
            self.labels['prey_avg_speed'].set_text(f"Prey Speed: {avg_prey_speed:.2f}")
            self.labels['prey_avg_vision'].set_text(f"Prey Vision: {avg_prey_vision:.1f}")
        else:
            self.labels['prey_avg_speed'].set_text("Prey Speed: N/A")
            self.labels['prey_avg_vision'].set_text("Prey Vision: N/A")
        
        if world.predators:
            avg_pred_speed = sum(p.traits.speed for p in world.predators) / len(world.predators)
            avg_pred_vision = sum(p.traits.vision for p in world.predators) / len(world.predators)
            self.labels['pred_avg_speed'].set_text(f"Pred Speed: {avg_pred_speed:.2f}")
            self.labels['pred_avg_vision'].set_text(f"Pred Vision: {avg_pred_vision:.1f}")
        else:
            self.labels['pred_avg_speed'].set_text("Pred Speed: N/A")
            self.labels['pred_avg_vision'].set_text("Pred Vision: N/A")
    
    def get_selected_trait(self):
        """Return the trait currently selected for the histogram."""
        return self.trait_options[self.trait_index]
    
    def _trait_label_text(self):
        """Formatted label for the trait selector."""
        trait_name = self.get_selected_trait().replace('_', ' ').title()
        return f"Trait Graph: {trait_name}"
    
    def draw(self, surface):
        """
        Draw the control panel.
        
        Args:
            surface: Pygame surface
        """
        # Initialize fonts if needed
        if not self.font:
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)
        
        # Draw background
        pygame.draw.rect(surface, BLACK, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw all UI elements
        for label in self.labels.values():
            if hasattr(label, 'font_size') and label.font_size > UI_FONT_SIZE:
                label.draw(surface, self.title_font)
            else:
                label.draw(surface, self.font)
        
        for button in self.buttons.values():
            button.draw(surface, self.font)
        
        for slider in self.sliders.values():
            slider.draw(surface, self.font)
