"""
Professional main menu with animations and polish.
"""
import pygame
import math
import random
from simulation.config import (
    UI_PANEL_BG, UI_TEXT_COLOR, UI_BORDER_COLOR,
    UI_ACCENT_COLOR, UI_BG_COLOR, UI_HOVER_COLOR, SPECIES_STYLE
)


class AnimatedParticle:
    """Background particle for menu atmosphere."""
    
    def __init__(self, x, y, vx, vy, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.alpha = random.randint(100, 200)
    
    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy
        
        # Wrap around screen
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0
        if self.y < 0:
            self.y = height
        elif self.y > height:
            self.y = 0
    
    def draw(self, surface):
        color_with_alpha = (*self.color[:3], self.alpha)
        glow = pygame.Surface((int(self.size * 4), int(self.size * 4)), pygame.SRCALPHA)
        pygame.draw.circle(glow, color_with_alpha, 
                          (int(self.size * 2), int(self.size * 2)), int(self.size))
        surface.blit(glow, (int(self.x - self.size * 2), int(self.y - self.size * 2)))


class MenuButton:
    """Animated menu button with hover effects."""
    
    def __init__(self, x, y, width, height, text, color=UI_ACCENT_COLOR, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.icon = icon
        self.hover = False
        self.hover_progress = 0.0
        self.click_animation = 0.0
        self.glow_pulse = 0.0
    
    def update(self, dt=1.0):
        # Smooth hover animation
        target = 1.0 if self.hover else 0.0
        self.hover_progress += (target - self.hover_progress) * 0.15
        
        # Click animation
        if self.click_animation > 0:
            self.click_animation -= 0.1
        
        # Glow pulse
        self.glow_pulse += 0.05
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.click_animation = 1.0
                return True
        return False
    
    def draw(self, surface, font):
        # Scale effect on hover
        scale = 1.0 + self.hover_progress * 0.05
        click_scale = 1.0 - self.click_animation * 0.05
        total_scale = scale * click_scale
        
        scaled_width = int(self.rect.width * total_scale)
        scaled_height = int(self.rect.height * total_scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Glow effect on hover
        if self.hover_progress > 0.01:
            glow_alpha = int(50 * self.hover_progress)
            glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.color[:3], glow_alpha),
                           (0, 0, scaled_width + 20, scaled_height + 20),
                           border_radius=scaled_height // 2)
            surface.blit(glow_surface, (scaled_x - 10, scaled_y - 10))
        
        # Main button
        color = self.color if not self.hover else UI_HOVER_COLOR
        pygame.draw.rect(surface, color, scaled_rect, border_radius=scaled_height // 2)
        
        # Border
        border_alpha = int(255 * (0.5 + self.hover_progress * 0.5))
        border_color = (*UI_BORDER_COLOR[:3], border_alpha)
        
        border_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, border_color,
                        (0, 0, scaled_width, scaled_height),
                        3, border_radius=scaled_height // 2)
        surface.blit(border_surface, (scaled_x, scaled_y))
        
        # Text with shadow
        text_color = UI_BG_COLOR if self.hover else UI_TEXT_COLOR
        shadow_text = font.render(self.text, True, (0, 0, 0))
        main_text = font.render(self.text, True, text_color)
        
        shadow_rect = shadow_text.get_rect(center=(scaled_rect.centerx + 2, scaled_rect.centery + 2))
        text_rect = main_text.get_rect(center=scaled_rect.center)
        
        surface.blit(shadow_text, shadow_rect)
        surface.blit(main_text, text_rect)


class MainMenu:
    """Professional animated main menu."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_title = None
        self.font_subtitle = None
        self.font_button = None
        self.font_small = None
        
        self.buttons = {}
        self.particles = []
        self.animation_time = 0
        self.show_credits = False
        self.show_how_to_play = False
        
        # Create background particles
        self._init_particles()
        
        # Initialize buttons
        self._init_buttons()
    
    def _init_particles(self):
        """Create atmospheric background particles."""
        colors = [
            (80, 250, 123),   # Green
            (139, 233, 253),  # Cyan
            (189, 147, 249),  # Purple
            (255, 184, 108),  # Orange
            (255, 121, 198),  # Pink
        ]
        
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-0.5, 0.5)
            color = random.choice(colors)
            size = random.uniform(1, 3)
            
            self.particles.append(AnimatedParticle(x, y, vx, vy, color, size))
    
    def _init_buttons(self):
        """Initialize menu buttons."""
        button_width = 300
        button_height = 60
        button_spacing = 20
        center_x = self.width // 2 - button_width // 2
        start_y = self.height // 2 + 20
        
        self.buttons = {
            "new_game": MenuButton(
                center_x, start_y,
                button_width, button_height,
                "🎮 New Game",
                UI_ACCENT_COLOR
            ),
            "continue": MenuButton(
                center_x, start_y + button_height + button_spacing,
                button_width, button_height,
                "▶️ Continue",
                (80, 250, 123)
            ),
            "tutorial": MenuButton(
                center_x, start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "📚 Tutorial",
                (139, 233, 253)
            ),
            "settings": MenuButton(
                center_x, start_y + (button_height + button_spacing) * 3,
                button_width, button_height,
                "⚙️ Settings",
                (255, 184, 108)
            ),
            "achievements": MenuButton(
                center_x, start_y + (button_height + button_spacing) * 4,
                button_width, button_height,
                "🏆 Achievements",
                (255, 121, 198)
            ),
            "quit": MenuButton(
                center_x, start_y + (button_height + button_spacing) * 5,
                button_width, button_height,
                "🚪 Quit",
                (255, 85, 85)
            ),
        }
    
    def handle_event(self, event, has_save=False):
        """Handle menu events. Returns action string or None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.show_credits or self.show_how_to_play:
                    self.show_credits = False
                    self.show_how_to_play = False
                    return None
                return "quit"
        
        # Button events
        for name, button in self.buttons.items():
            if button.handle_event(event):
                # Disable continue if no save
                if name == "continue" and not has_save:
                    return None
                return name
        
        return None
    
    def update(self):
        """Update menu animations."""
        self.animation_time += 1
        
        # Update particles
        for particle in self.particles:
            particle.update(self.width, self.height)
        
        # Update buttons
        for button in self.buttons.values():
            button.update()
    
    def draw(self, surface, has_save=False):
        """Draw the main menu."""
        if not self.font_title:
            self.font_title = pygame.font.Font(None, 72)
            self.font_subtitle = pygame.font.Font(None, 32)
            self.font_button = pygame.font.Font(None, 28)
            self.font_small = pygame.font.Font(None, 20)
        
        # Background gradient
        for y in range(self.height):
            ratio = y / self.height
            color = (
                int(15 + 10 * ratio),
                int(20 + 10 * ratio),
                int(35 + 10 * ratio)
            )
            pygame.draw.line(surface, color, (0, y), (self.width, y))
        
        # Draw particles
        for particle in self.particles:
            particle.draw(surface)
        
        # Animated title with wave effect
        title_text = "EVOLUTION SANDBOX"
        title_y = 100
        
        # Shadow
        for i, char in enumerate(title_text):
            wave_offset = math.sin(self.animation_time * 0.05 + i * 0.3) * 5
            char_surface = self.font_title.render(char, True, (0, 0, 0))
            x_pos = self.width // 2 - len(title_text) * 20 + i * 40
            surface.blit(char_surface, (x_pos + 3, title_y + wave_offset + 3))
        
        # Main title
        for i, char in enumerate(title_text):
            wave_offset = math.sin(self.animation_time * 0.05 + i * 0.3) * 5
            # Rainbow color effect
            hue_offset = (self.animation_time + i * 20) % 360
            if i % 3 == 0:
                color = (189, 147, 249)  # Purple
            elif i % 3 == 1:
                color = (139, 233, 253)  # Cyan
            else:
                color = (255, 121, 198)  # Pink
            
            char_surface = self.font_title.render(char, True, color)
            x_pos = self.width // 2 - len(title_text) * 20 + i * 40
            surface.blit(char_surface, (x_pos, title_y + wave_offset))
        
        # Subtitle with pulse
        pulse = abs(math.sin(self.animation_time * 0.02)) * 0.2 + 0.8
        subtitle_font = pygame.font.Font(None, int(32 * pulse))
        subtitle = subtitle_font.render("Watch Life Evolve in Real-Time", True, (150, 150, 160))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 180))
        surface.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        for name, button in self.buttons.items():
            # Dim continue button if no save
            if name == "continue" and not has_save:
                # Draw dimmed
                dimmed_surface = pygame.Surface((button.rect.width, button.rect.height), pygame.SRCALPHA)
                dimmed_surface.fill((60, 60, 70, 200))
                surface.blit(dimmed_surface, button.rect.topleft)
                
                text = self.font_button.render(button.text, True, (100, 100, 110))
                text_rect = text.get_rect(center=button.rect.center)
                surface.blit(text, text_rect)
            else:
                button.draw(surface, self.font_button)
        
        # Version and credits at bottom
        version_text = self.font_small.render("v1.0 | Enhanced Edition", True, (100, 100, 110))
        surface.blit(version_text, (20, self.height - 40))
        
        credits_text = self.font_small.render("Press C for Credits | H for How to Play", 
                                              True, (100, 100, 110))
        credits_rect = credits_text.get_rect(right=self.width - 20, y=self.height - 40)
        surface.blit(credits_text, credits_rect)
        
        # Show credits or how to play if active
        if self.show_credits:
            self._draw_credits(surface)
        elif self.show_how_to_play:
            self._draw_how_to_play(surface)
    
    def _draw_credits(self, surface):
        """Draw credits overlay."""
        # Semi-transparent background
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # Credits panel
        panel_width = 600
        panel_height = 400
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2
        
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((40, 42, 54, 250))
        pygame.draw.rect(panel, UI_ACCENT_COLOR, (0, 0, panel_width, panel_height),
                        3, border_radius=15)
        
        # Title
        title = self.font_subtitle.render("Credits", True, UI_ACCENT_COLOR)
        title_rect = title.get_rect(centerx=panel_width // 2, y=30)
        panel.blit(title, title_rect)
        
        # Credits content
        credits_lines = [
            "",
            "Game Design & Development",
            "Original: charlie2233",
            "",
            "Enhanced Edition",
            "AI-Enhanced UI/UX Design",
            "",
            "Built with:",
            "Python • Pygame • NumPy",
            "",
            "Special Thanks:",
            "Evolutionary Algorithm Research Community",
            "Artificial Life Enthusiasts",
            "",
            "Press ESC to close"
        ]
        
        y_offset = 100
        for line in credits_lines:
            if line:
                color = UI_ACCENT_COLOR if ":" in line else UI_TEXT_COLOR
                text = self.font_small.render(line, True, color)
                text_rect = text.get_rect(centerx=panel_width // 2, y=y_offset)
                panel.blit(text, text_rect)
            y_offset += 25
        
        surface.blit(panel, (panel_x, panel_y))
    
    def _draw_how_to_play(self, surface):
        """Draw how to play overlay."""
        # Similar to credits but with gameplay info
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        panel_width = 700
        panel_height = 500
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2
        
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((40, 42, 54, 250))
        pygame.draw.rect(panel, UI_ACCENT_COLOR, (0, 0, panel_width, panel_height),
                        3, border_radius=15)
        
        title = self.font_subtitle.render("How to Play", True, UI_ACCENT_COLOR)
        title_rect = title.get_rect(centerx=panel_width // 2, y=30)
        panel.blit(title, title_rect)
        
        info_lines = [
            "",
            "🎮 Controls:",
            "SPACE - Pause/Resume  |  R - Reset Generation  |  ESC - Menu",
            "Mouse Wheel - Zoom  |  Click Agent - Inspect Details",
            "",
            "🧬 Evolution:",
            "Creatures evolve traits over generations through natural selection",
            "Successful creatures pass on their genes to offspring",
            "",
            "🎯 Goal:",
            "Maintain a balanced ecosystem and watch evolution unfold!",
            "Unlock achievements and survive disasters",
            "",
            "💡 Tips:",
            "• Adjust simulation speed for faster evolution",
            "• Use manual events to test species resilience",
            "• Watch the population graphs for ecosystem health",
            "",
            "Press ESC to close"
        ]
        
        y_offset = 90
        for line in info_lines:
            if line:
                color = UI_ACCENT_COLOR if any(icon in line for icon in ["🎮", "🧬", "🎯", "💡"]) else UI_TEXT_COLOR
                font = self.font_small if not any(icon in line for icon in ["🎮", "🧬", "🎯", "💡"]) else self.font_button
                text = font.render(line, True, color)
                text_rect = text.get_rect(centerx=panel_width // 2, y=y_offset)
                panel.blit(text, text_rect)
                y_offset += 22 if font == self.font_small else 30
        
        surface.blit(panel, (panel_x, panel_y))

