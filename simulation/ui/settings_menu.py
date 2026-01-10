"""
Professional settings menu for game configuration.
"""
import pygame
from simulation.ui.components import Button, Slider
from simulation.config import (
    UI_PANEL_BG, UI_TEXT_COLOR, UI_BORDER_COLOR,
    UI_ACCENT_COLOR, UI_BG_COLOR, UI_HOVER_COLOR
)


class SettingsMenu:
    """Professional settings menu with tabs."""
    
    def __init__(self):
        self.visible = False
        self.font = None
        self.font_title = None
        self.tabs = ["Graphics", "Audio", "Gameplay"]
        self.active_tab = "Graphics"
        self.tab_buttons = {}
        self.buttons = {}
        self.sliders = {}
        
        # Settings values
        self.settings = {
            # Graphics
            "show_trails": False,
            "show_vision": False,
            "particle_quality": 1.0,  # 0.5 = low, 1.0 = medium, 1.5 = high
            "show_minimap": True,
            "show_fps": True,
            
            # Audio
            "music_enabled": True,
            "sfx_enabled": True,
            "music_volume": 0.5,
            "sfx_volume": 0.7,
            
            # Gameplay
            "auto_pause": False,
            "show_tooltips": True,
            "show_notifications": True,
            "camera_smoothing": True,
        }
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI elements."""
        # Tab buttons will be positioned dynamically in draw()
        pass
    
    def toggle(self):
        """Toggle settings menu visibility."""
        self.visible = not self.visible
    
    def handle_event(self, event, sound_manager=None):
        """Handle input events."""
        if not self.visible:
            return {}
        
        actions = {}
        
        # Handle tab switching
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.visible = False
                return actions
        
        # Mouse interactions handled in draw loop with collision detection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check tab clicks
            for tab_name, button_rect in self.tab_buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    self.active_tab = tab_name
                    if sound_manager:
                        sound_manager.play_ui_click()
            
            # Check setting buttons
            for setting_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    # Toggle boolean settings
                    if setting_name in self.settings:
                        if isinstance(self.settings[setting_name], bool):
                            self.settings[setting_name] = not self.settings[setting_name]
                            actions[setting_name] = self.settings[setting_name]
                            if sound_manager:
                                sound_manager.play_ui_click()
        
        # Handle slider events
        for slider in self.sliders.values():
            slider.handle_event(event)
        
        # Update settings from sliders
        for setting_name, slider in self.sliders.items():
            self.settings[setting_name] = slider.value
            actions[setting_name] = slider.value
        
        return actions
    
    def draw(self, surface):
        """Draw settings menu."""
        if not self.visible:
            return
        
        if not self.font:
            self.font = pygame.font.Font(None, 22)
            self.font_title = pygame.font.Font(None, 32)
        
        # Semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Settings panel
        panel_width = 800
        panel_height = 600
        panel_x = (surface.get_width() - panel_width) // 2
        panel_y = (surface.get_height() - panel_height) // 2
        
        # Panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((40, 42, 54, 250))
        pygame.draw.rect(panel_surface, UI_BORDER_COLOR,
                        (0, 0, panel_width, panel_height), 3, border_radius=15)
        
        # Title
        title = self.font_title.render("Settings", True, UI_ACCENT_COLOR)
        title_rect = title.get_rect(centerx=panel_width // 2, y=20)
        panel_surface.blit(title, title_rect)
        
        # Close hint
        close_text = self.font.render("[ESC to close]", True, (150, 150, 160))
        panel_surface.blit(close_text, (panel_width - 150, 25))
        
        # Draw tabs
        tab_y = 70
        tab_width = 150
        tab_height = 40
        tab_spacing = 10
        tab_start_x = 50
        
        self.tab_buttons.clear()
        
        for i, tab_name in enumerate(self.tabs):
            tab_x = tab_start_x + i * (tab_width + tab_spacing)
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            
            # Store for click detection
            screen_rect = pygame.Rect(panel_x + tab_x, panel_y + tab_y, tab_width, tab_height)
            self.tab_buttons[tab_name] = screen_rect
            
            # Draw tab
            is_active = (tab_name == self.active_tab)
            color = UI_ACCENT_COLOR if is_active else UI_PANEL_BG
            text_color = UI_BG_COLOR if is_active else UI_TEXT_COLOR
            
            pygame.draw.rect(panel_surface, color, tab_rect, border_radius=8)
            pygame.draw.rect(panel_surface, UI_BORDER_COLOR, tab_rect, 2, border_radius=8)
            
            tab_text = self.font.render(tab_name, True, text_color)
            text_rect = tab_text.get_rect(center=tab_rect.center)
            panel_surface.blit(tab_text, text_rect)
        
        # Draw tab content
        content_y = 130
        self._draw_tab_content(panel_surface, content_y, panel_x, panel_y)
        
        surface.blit(panel_surface, (panel_x, panel_y))
    
    def _draw_tab_content(self, surface, start_y, panel_x, panel_y):
        """Draw content for active tab."""
        y_offset = start_y
        self.buttons.clear()
        self.sliders.clear()
        
        if self.active_tab == "Graphics":
            self._draw_graphics_settings(surface, y_offset, panel_x, panel_y)
        elif self.active_tab == "Audio":
            self._draw_audio_settings(surface, y_offset, panel_x, panel_y)
        elif self.active_tab == "Gameplay":
            self._draw_gameplay_settings(surface, y_offset, panel_x, panel_y)
    
    def _draw_graphics_settings(self, surface, y_offset, panel_x, panel_y):
        """Draw graphics settings."""
        settings = [
            ("show_trails", "Show Agent Trails", "Display movement trails for agents"),
            ("show_vision", "Show Vision Ranges", "Display vision circles around agents"),
            ("show_minimap", "Show Minimap", "Display minimap overlay"),
            ("show_fps", "Show FPS Counter", "Display frames per second"),
        ]
        
        for setting_name, title, description in settings:
            y_offset = self._draw_toggle_setting(
                surface, setting_name, title, description, 
                y_offset, panel_x, panel_y
            )
        
        # Particle quality slider
        y_offset += 20
        section_text = self.font.render("Particle Quality", True, UI_TEXT_COLOR)
        surface.blit(section_text, (50, y_offset))
        y_offset += 30
        
        slider = Slider(50, y_offset, 300, 20, 0.5, 1.5, 
                       self.settings["particle_quality"], "Quality")
        slider.draw(surface, self.font)
        
        # Store for event handling
        screen_slider = Slider(panel_x + 50, panel_y + y_offset, 300, 20,
                              0.5, 1.5, self.settings["particle_quality"], "Quality")
        screen_slider.rect = pygame.Rect(panel_x + 50, panel_y + y_offset, 300, 20)
        screen_slider.handle_x = slider.handle_x + panel_x
        screen_slider.handle_y = slider.handle_y + panel_y
        self.sliders["particle_quality"] = screen_slider
    
    def _draw_audio_settings(self, surface, y_offset, panel_x, panel_y):
        """Draw audio settings."""
        # Music toggle
        y_offset = self._draw_toggle_setting(
            surface, "music_enabled", "Background Music",
            "Enable background music", y_offset, panel_x, panel_y
        )
        
        # Music volume slider
        if self.settings["music_enabled"]:
            section_text = self.font.render("Music Volume", True, UI_TEXT_COLOR)
            surface.blit(section_text, (50, y_offset))
            y_offset += 30
            
            slider = Slider(50, y_offset, 300, 20, 0.0, 1.0,
                           self.settings["music_volume"], "Volume")
            slider.draw(surface, self.font)
            
            screen_slider = Slider(panel_x + 50, panel_y + y_offset, 300, 20,
                                  0.0, 1.0, self.settings["music_volume"], "Volume")
            screen_slider.rect = pygame.Rect(panel_x + 50, panel_y + y_offset, 300, 20)
            screen_slider.handle_x = slider.handle_x + panel_x
            screen_slider.handle_y = slider.handle_y + panel_y
            self.sliders["music_volume"] = screen_slider
            y_offset += 50
        
        # SFX toggle
        y_offset = self._draw_toggle_setting(
            surface, "sfx_enabled", "Sound Effects",
            "Enable sound effects", y_offset, panel_x, panel_y
        )
        
        # SFX volume slider
        if self.settings["sfx_enabled"]:
            section_text = self.font.render("SFX Volume", True, UI_TEXT_COLOR)
            surface.blit(section_text, (50, y_offset))
            y_offset += 30
            
            slider = Slider(50, y_offset, 300, 20, 0.0, 1.0,
                           self.settings["sfx_volume"], "Volume")
            slider.draw(surface, self.font)
            
            screen_slider = Slider(panel_x + 50, panel_y + y_offset, 300, 20,
                                  0.0, 1.0, self.settings["sfx_volume"], "Volume")
            screen_slider.rect = pygame.Rect(panel_x + 50, panel_y + y_offset, 300, 20)
            screen_slider.handle_x = slider.handle_x + panel_x
            screen_slider.handle_y = slider.handle_y + panel_y
            self.sliders["sfx_volume"] = screen_slider
            y_offset += 50
    
    def _draw_gameplay_settings(self, surface, y_offset, panel_x, panel_y):
        """Draw gameplay settings."""
        settings = [
            ("auto_pause", "Auto-Pause on Events", 
             "Pause simulation when disasters occur"),
            ("show_tooltips", "Show Tooltips", 
             "Display helpful tooltips on hover"),
            ("show_notifications", "Show Notifications",
             "Display achievement and event notifications"),
            ("camera_smoothing", "Smooth Camera",
             "Enable smooth camera transitions"),
        ]
        
        for setting_name, title, description in settings:
            y_offset = self._draw_toggle_setting(
                surface, setting_name, title, description,
                y_offset, panel_x, panel_y
            )
    
    def _draw_toggle_setting(self, surface, setting_name, title, description, 
                            y_offset, panel_x, panel_y):
        """Draw a toggle setting with checkbox."""
        # Title
        title_text = self.font.render(title, True, UI_TEXT_COLOR)
        surface.blit(title_text, (50, y_offset))
        
        # Description (smaller, grayed)
        desc_font = pygame.font.Font(None, 18)
        desc_text = desc_font.render(description, True, (150, 150, 160))
        surface.blit(desc_text, (50, y_offset + 25))
        
        # Checkbox/toggle
        toggle_x = 650
        toggle_width = 60
        toggle_height = 30
        toggle_rect = pygame.Rect(toggle_x, y_offset, toggle_width, toggle_height)
        
        # Store for click detection
        screen_rect = pygame.Rect(panel_x + toggle_x, panel_y + y_offset, 
                                 toggle_width, toggle_height)
        self.buttons[setting_name] = screen_rect
        
        # Draw toggle switch
        is_on = self.settings.get(setting_name, False)
        bg_color = UI_ACCENT_COLOR if is_on else (80, 80, 90)
        pygame.draw.rect(surface, bg_color, toggle_rect, border_radius=15)
        
        # Switch circle
        circle_x = toggle_x + (toggle_width - 15) if is_on else toggle_x + 15
        pygame.draw.circle(surface, UI_TEXT_COLOR, 
                          (circle_x, y_offset + toggle_height // 2), 12)
        
        # Status text
        status = "ON" if is_on else "OFF"
        status_color = (80, 250, 123) if is_on else (150, 150, 160)
        status_text = self.font.render(status, True, status_color)
        surface.blit(status_text, (toggle_x + toggle_width + 15, y_offset + 5))
        
        return y_offset + 70
    
    def get_setting(self, name, default=None):
        """Get a setting value."""
        return self.settings.get(name, default)
    
    def set_setting(self, name, value):
        """Set a setting value."""
        self.settings[name] = value

