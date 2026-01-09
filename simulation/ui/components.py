"""
UI components for the simulation.
"""
import pygame
from simulation.config import (
    WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY,
    UI_PADDING, UI_SLIDER_WIDTH, UI_SLIDER_HEIGHT,
    UI_BUTTON_WIDTH, UI_BUTTON_HEIGHT, UI_FONT_SIZE
)


class Button:
    """Clickable button UI element."""
    
    def __init__(self, x, y, width, height, text, color=GRAY, text_color=WHITE):
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
        self.hover_color = tuple(min(255, c + 30) for c in color)
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
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, self.text_color)
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
        self.handle_radius = height // 2 + 2
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
        label_surface = font.render(f"{self.label}: {self.value:.1f}", True, WHITE)
        surface.blit(label_surface, (self.rect.x, self.rect.y - 20))
        
        # Draw track
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, 2)
        
        # Draw filled portion
        filled_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(surface, GRAY, filled_rect)
        
        # Draw handle
        pygame.draw.circle(surface, WHITE, (self.handle_x, self.handle_y), self.handle_radius)
        pygame.draw.circle(surface, LIGHT_GRAY, (self.handle_x, self.handle_y), self.handle_radius - 2)


class Label:
    """Text label UI element."""
    
    def __init__(self, x, y, text, color=WHITE, font_size=UI_FONT_SIZE):
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
