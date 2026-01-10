"""
Tutorial and help system for the game.
"""
import pygame
from simulation.config import (
    UI_PANEL_BG, UI_TEXT_COLOR, UI_BORDER_COLOR, 
    UI_ACCENT_COLOR, UI_BG_COLOR
)


class TutorialStep:
    """Single tutorial step."""
    
    def __init__(self, title, description, highlight_area=None, arrow_target=None):
        self.title = title
        self.description = description  # Can be a list of strings
        self.highlight_area = highlight_area  # pygame.Rect to highlight
        self.arrow_target = arrow_target  # (x, y) to point arrow at
        self.completed = False


class TutorialManager:
    """Manages tutorial flow and display."""
    
    def __init__(self):
        self.active = False
        self.current_step = 0
        self.steps = []
        self.font = None
        self.font_title = None
        self.shown_before = False
        
        self._init_tutorial_steps()
    
    def _init_tutorial_steps(self):
        """Initialize tutorial steps."""
        self.steps = [
            TutorialStep(
                "Welcome to Evolution Sandbox!",
                [
                    "Watch as creatures evolve and adapt in real-time.",
                    "Multiple species compete for survival using genetic algorithms.",
                    "",
                    "Click NEXT to learn the basics..."
                ]
            ),
            TutorialStep(
                "The World",
                [
                    "🌍 Creatures live in a dynamic ecosystem with:",
                    "  • Food sources (green dots)",
                    "  • Water zones (blue areas)",
                    "  • Rocks and shelters",
                    "",
                    "Each species has unique behaviors and traits."
                ]
            ),
            TutorialStep(
                "Species Overview",
                [
                    "🦎 Grazer (Green) - Herbivores that eat plants",
                    "🦊 Hunter (Red) - Predators that hunt prey",
                    "🦅 Scavenger (Orange) - Opportunistic eaters",
                    "🛡️ Protector (Cyan) - Defenders with stun ability",
                    "🦠 Parasite (Purple) - Energy drainers",
                    "👑 Apex (Yellow) - Top predators",
                    "🐟 Sea Hunter (Blue) - Aquatic predators"
                ]
            ),
            TutorialStep(
                "Evolution System",
                [
                    "🧬 Each generation:",
                    "  • Creatures with better traits survive longer",
                    "  • Successful creatures reproduce",
                    "  • Offspring inherit parent traits with mutations",
                    "  • Natural selection favors the fittest",
                    "",
                    "Watch populations adapt over time!"
                ]
            ),
            TutorialStep(
                "Controls - Camera",
                [
                    "🎥 Navigation:",
                    "  • Mouse Wheel - Zoom in/out",
                    "  • Click Minimap - Jump to location",
                    "  • Click Agent - Inspect details",
                    "",
                    "  • SPACE - Pause/Resume",
                    "  • R - Reset generation",
                    "  • ESC - Menu"
                ]
            ),
            TutorialStep(
                "Control Panel",
                [
                    "🎛️ Right panel controls:",
                    "  • Speed Slider - Simulation speed",
                    "  • World/Evolution Tabs - Settings",
                    "  • Manual Events - Trigger disasters",
                    "  • Export Stats - Save data",
                    "",
                    "Experiment with different settings!"
                ]
            ),
            TutorialStep(
                "God Mode Events",
                [
                    "⚡ Trigger disasters manually:",
                    "  1. Click Earthquake/Wave/Meteor button",
                    "  2. Click on the world to place event",
                    "  3. Watch the ecosystem respond",
                    "",
                    "Disasters test species resilience!"
                ]
            ),
            TutorialStep(
                "Achievements & Goals",
                [
                    "🏆 Unlock achievements by:",
                    "  • Reaching generation milestones",
                    "  • Maintaining diverse ecosystems",
                    "  • Evolving extreme traits",
                    "  • Surviving disasters",
                    "",
                    "Check the achievements panel to track progress!"
                ]
            ),
            TutorialStep(
                "Ready to Play!",
                [
                    "✨ You're all set!",
                    "",
                    "Start with default settings or customize:",
                    "  • Population sizes",
                    "  • World dimensions",
                    "  • Mutation rates",
                    "  • Episode length",
                    "",
                    "Enjoy watching evolution unfold!",
                    "",
                    "Press ESC anytime for help menu."
                ]
            ),
        ]
    
    def start(self):
        """Start the tutorial."""
        self.active = True
        self.current_step = 0
    
    def next_step(self):
        """Go to next tutorial step."""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            return True
        else:
            self.complete()
            return False
    
    def prev_step(self):
        """Go to previous tutorial step."""
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False
    
    def skip(self):
        """Skip tutorial."""
        self.complete()
    
    def complete(self):
        """Complete tutorial."""
        self.active = False
        self.shown_before = True
    
    def handle_event(self, event):
        """Handle tutorial events."""
        if not self.active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                return self.next_step()
            elif event.key == pygame.K_LEFT:
                return self.prev_step()
            elif event.key == pygame.K_ESCAPE:
                self.skip()
                return False
        
        return False
    
    def draw(self, surface):
        """Draw tutorial overlay."""
        if not self.active:
            return
        
        if not self.font:
            self.font = pygame.font.Font(None, 22)
            self.font_title = pygame.font.Font(None, 32)
        
        # Semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Tutorial panel
        panel_width = 700
        panel_height = 500
        panel_x = (surface.get_width() - panel_width) // 2
        panel_y = (surface.get_height() - panel_height) // 2
        
        # Panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((40, 42, 54, 250))
        pygame.draw.rect(panel_surface, UI_ACCENT_COLOR, 
                        (0, 0, panel_width, panel_height), 3, border_radius=15)
        
        # Current step
        step = self.steps[self.current_step]
        
        # Title
        title = self.font_title.render(step.title, True, UI_ACCENT_COLOR)
        title_rect = title.get_rect(centerx=panel_width // 2, y=30)
        panel_surface.blit(title, title_rect)
        
        # Progress indicator
        progress_text = f"Step {self.current_step + 1} of {len(self.steps)}"
        progress = self.font.render(progress_text, True, (150, 150, 160))
        progress_rect = progress.get_rect(centerx=panel_width // 2, y=70)
        panel_surface.blit(progress, progress_rect)
        
        # Description
        y_offset = 120
        descriptions = step.description if isinstance(step.description, list) else [step.description]
        
        for line in descriptions:
            if line:  # Non-empty line
                text = self.font.render(line, True, UI_TEXT_COLOR)
                panel_surface.blit(text, (50, y_offset))
            y_offset += 30
        
        # Navigation buttons
        button_y = panel_height - 70
        
        # Previous button
        if self.current_step > 0:
            prev_text = self.font.render("← Previous", True, UI_TEXT_COLOR)
            panel_surface.blit(prev_text, (50, button_y))
        
        # Skip button
        skip_text = self.font.render("Skip (ESC)", True, (150, 150, 160))
        skip_rect = skip_text.get_rect(centerx=panel_width // 2, y=button_y)
        panel_surface.blit(skip_text, skip_rect)
        
        # Next button
        if self.current_step < len(self.steps) - 1:
            next_text = self.font.render("Next →", True, UI_ACCENT_COLOR)
            next_rect = next_text.get_rect(right=panel_width - 50, y=button_y)
            panel_surface.blit(next_text, next_rect)
        else:
            finish_text = self.font.render("Start Playing! →", True, (80, 250, 123))
            finish_rect = finish_text.get_rect(right=panel_width - 50, y=button_y)
            panel_surface.blit(finish_text, finish_rect)
        
        # Draw panel
        surface.blit(panel_surface, (panel_x, panel_y))


class HelpMenu:
    """Quick help menu accessible anytime."""
    
    def __init__(self):
        self.visible = False
        self.font = None
        self.font_title = None
    
    def toggle(self):
        """Toggle help menu visibility."""
        self.visible = not self.visible
    
    def draw(self, surface):
        """Draw help menu."""
        if not self.visible:
            return
        
        if not self.font:
            self.font = pygame.font.Font(None, 20)
            self.font_title = pygame.font.Font(None, 28)
        
        # Panel
        width = 600
        height = 600
        x = (surface.get_width() - width) // 2
        y = (surface.get_height() - height) // 2
        
        # Background
        help_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        help_surface.fill((40, 42, 54, 245))
        pygame.draw.rect(help_surface, UI_BORDER_COLOR, (0, 0, width, height), 
                        2, border_radius=10)
        
        # Title
        title = self.font_title.render("Quick Help", True, UI_ACCENT_COLOR)
        help_surface.blit(title, (20, 20))
        
        # Close hint
        close = self.font.render("[Press H or ESC to close]", True, (150, 150, 160))
        help_surface.blit(close, (width - 230, 25))
        
        # Help content
        y_offset = 70
        sections = [
            ("Keyboard Controls:", [
                "SPACE - Pause/Resume simulation",
                "R - Reset current generation",
                "ESC - Open menu",
                "H - Toggle this help menu",
            ]),
            ("Mouse Controls:", [
                "Scroll Wheel - Zoom in/out",
                "Click Agent - Inspect details",
                "Click Minimap - Jump to location",
                "Click UI - Interact with controls",
            ]),
            ("Species Colors:", [
                "Green - Grazer (Herbivore)",
                "Red - Hunter (Predator)",
                "Orange - Scavenger",
                "Cyan - Protector",
                "Purple - Parasite",
                "Yellow - Apex Predator",
                "Blue - Sea Hunter",
            ]),
            ("Tips:", [
                "• Watch population graphs for balance",
                "• Adjust mutation rate for faster evolution",
                "• Use events to test species resilience",
                "• Export stats for analysis",
            ]),
        ]
        
        for section_title, items in sections:
            # Section title
            sec_text = self.font_title.render(section_title, True, UI_ACCENT_COLOR)
            help_surface.blit(sec_text, (30, y_offset))
            y_offset += 35
            
            # Items
            for item in items:
                item_text = self.font.render(item, True, UI_TEXT_COLOR)
                help_surface.blit(item_text, (50, y_offset))
                y_offset += 25
            
            y_offset += 15
        
        surface.blit(help_surface, (x, y))

