"""
UI components for the simulation.
"""
import pygame
from simulation.config import (
    WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY,
    UI_PADDING, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT,
    UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, UI_FONT_SIZE,
    UI_PANEL_BG, UI_TEXT_COLOR, UI_ACCENT_COLOR, UI_HOVER_COLOR,
    UI_BORDER_COLOR, UI_BG_COLOR
)
import pygame.locals as pl


class Button:
    """Clickable button UI element."""
    
    def __init__(self, x, y, width, height, text, color=UI_PANEL_BG, text_color=UI_TEXT_COLOR):
        """
        Initialize button.
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
            color: Button color
            text_color: Text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = UI_HOVER_COLOR
        self.is_hovered = False
    
    def handle_event(self, event):
        """
        Handle mouse events.
        
        Args:
            event: Pygame event
            
        Returns:
            True if button was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, surface, font):
        """
        Draw the button.
        
        Args:
            surface: Pygame surface
            font: Pygame font
        """
        color = self.hover_color if self.is_hovered else self.color
        
        # Rounded background
        pygame.draw.rect(surface, color, self.rect, border_radius=self.rect.height // 2)
        
        # Border
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2, border_radius=self.rect.height // 2)
        
        # Text shadow for better readability
        shadow_surface = font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        surface.blit(shadow_surface, shadow_rect)

        text_surface = font.render(self.text, True, self.text_color if not self.is_hovered else (40, 42, 54))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Slider:
    """Slider UI element for adjusting values."""
    
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        """
        Initialize slider.
        
        Args:
            x: X position
            y: Y position
            width: Slider width
            height: Slider height
            min_val: Minimum value
            max_val: Maximum value
            initial_val: Initial value
            label: Slider label
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        
        # Handle slider position
        self.handle_radius = height // 2 + 4
        self.update_handle_pos()
    
    def update_handle_pos(self):
        """Update handle position based on value."""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + int(ratio * self.rect.width)
        self.handle_y = self.rect.centery
    
    def handle_event(self, event):
        """
        Handle mouse events.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_rect = pygame.Rect(
                self.handle_x - self.handle_radius,
                self.handle_y - self.handle_radius,
                self.handle_radius * 2,
                self.handle_radius * 2
            )
            if handle_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value_from_mouse(event.pos[0])
    
    def update_value_from_mouse(self, mouse_x):
        """
        Update value based on mouse position.
        
        Args:
            mouse_x: Mouse X position
        """
        # Clamp to slider bounds
        mouse_x = max(self.rect.x, min(self.rect.right, mouse_x))
        
        # Calculate value
        ratio = (mouse_x - self.rect.x) / self.rect.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        
        self.update_handle_pos()
    
    def draw(self, surface, font):
        """
        Draw the slider.
        
        Args:
            surface: Pygame surface
            font: Pygame font
        """
        # Draw label
        label_surface = font.render(f"{self.label}: {self.value:.1f}", True, UI_TEXT_COLOR)
        surface.blit(label_surface, (self.rect.x, self.rect.y - 20))
        
        # Draw track
        pygame.draw.rect(surface, UI_PANEL_BG, self.rect, border_radius=self.rect.height // 2)
        
        # Draw filled portion
        filled_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(surface, UI_ACCENT_COLOR, filled_rect, border_radius=self.rect.height // 2)
        
        # Draw handle
        pygame.draw.circle(surface, UI_TEXT_COLOR, (self.handle_x, self.handle_y), self.handle_radius)
        pygame.draw.circle(surface, UI_PANEL_BG, (self.handle_x, self.handle_y), self.handle_radius - 2)


class Label:
    """Text label UI element."""
    
    def __init__(self, x, y, text, color=UI_TEXT_COLOR, font_size=UI_FONT_SIZE):
        """
        Initialize label.
        
        Args:
            x: X position
            y: Y position
            text: Label text
            color: Text color
            font_size: Font size
        """
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size
    
    def set_text(self, text):
        """Update label text."""
        self.text = text
    
    def draw(self, surface, font):
        """
        Draw the label.
        
        Args:
            surface: Pygame surface
            font: Pygame font
        """
        text_surface = font.render(str(self.text), True, self.color)
        surface.blit(text_surface, (self.x, self.y))


class NumericInput:
    """Simple numeric input box."""

    def __init__(self, x, y, width, height, value, label="", min_val=0, max_val=9999):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.label = label
        self.active = False
        self.min_val = min_val
        self.max_val = max_val
        self.text = str(value)

    def handle_event(self, event):
        if event.type == pl.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pl.KEYDOWN:
            if event.key == pl.K_RETURN:
                self._commit()
                self.active = False
            elif event.key == pl.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

    def _commit(self):
        try:
            num = int(self.text)
            num = max(self.min_val, min(self.max_val, num))
            self.value = num
        except ValueError:
            self.text = str(self.value)

    def draw(self, surface, font):
        color = UI_ACCENT_COLOR if self.active else UI_PANEL_BG
        
        pygame.draw.rect(surface, color, self.rect, border_radius=self.rect.height // 2)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 1, border_radius=self.rect.height // 2)
        
        label_surface = font.render(f"{self.label}: {self.value}", True, UI_TEXT_COLOR)
        surface.blit(label_surface, (self.rect.x, self.rect.y - 18))
        
        text_color = BLACK if self.active else UI_TEXT_COLOR
        text_surface = font.render(self.text, True, text_color)
        surface.blit(text_surface, (self.rect.x + 4, self.rect.y + 4))
