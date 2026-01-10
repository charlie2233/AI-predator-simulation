"""
Agent inspector for viewing detailed agent information.
"""
import pygame
from simulation.config import (
    UI_PANEL_BG, UI_TEXT_COLOR, UI_BORDER_COLOR, 
    UI_ACCENT_COLOR, SPECIES_STYLE
)


class AgentInspector:
    """Panel showing detailed information about selected agent."""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.selected_agent = None
        self.font = None
        self.font_title = None
        self.visible = False
        self.follow_agent = False
    
    def select_agent(self, agent):
        """Select an agent to inspect."""
        self.selected_agent = agent
        self.visible = True if agent else False
    
    def deselect(self):
        """Deselect current agent."""
        self.selected_agent = None
        self.visible = False
        self.follow_agent = False
    
    def update(self):
        """Update inspector state."""
        # Auto-deselect if agent is dead or doesn't exist
        if self.selected_agent and not hasattr(self.selected_agent, 'alive'):
            self.deselect()
        elif self.selected_agent and not self.selected_agent.alive:
            self.deselect()
    
    def get_camera_target(self):
        """Get camera target if following agent."""
        if self.follow_agent and self.selected_agent:
            return (self.selected_agent.x, self.selected_agent.y)
        return None
    
    def draw(self, surface):
        """Draw the inspector panel."""
        if not self.visible or not self.selected_agent:
            return
        
        if not self.font:
            self.font = pygame.font.Font(None, 18)
            self.font_title = pygame.font.Font(None, 24)
        
        # Background
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        panel_surface.fill((40, 42, 54, 230))
        
        # Border
        pygame.draw.rect(panel_surface, UI_BORDER_COLOR, 
                        (0, 0, self.rect.width, self.rect.height), 2, border_radius=8)
        
        y_offset = 10
        
        # Species name
        species_name = self.selected_agent.__class__.__name__
        color = SPECIES_STYLE.get(species_name.lower(), {}).get("color", UI_ACCENT_COLOR)
        
        title = self.font_title.render(f"{species_name} Inspector", True, color)
        panel_surface.blit(title, (10, y_offset))
        y_offset += 35
        
        # Close button hint
        close_hint = self.font.render("[ESC to close]", True, (150, 150, 160))
        panel_surface.blit(close_hint, (self.rect.width - 120, 15))
        
        # Draw divider
        pygame.draw.line(panel_surface, UI_BORDER_COLOR, (10, y_offset), 
                        (self.rect.width - 10, y_offset), 1)
        y_offset += 10
        
        # Basic stats
        stats = [
            ("Health", f"{int(self.selected_agent.energy)}/{int(self.selected_agent.max_energy)}"),
            ("Age", f"{getattr(self.selected_agent, 'age', 0)} steps"),
            ("Position", f"({int(self.selected_agent.x)}, {int(self.selected_agent.y)})"),
            ("Alive", "Yes" if self.selected_agent.alive else "No"),
        ]
        
        for label, value in stats:
            text = self.font.render(f"{label}:", True, UI_TEXT_COLOR)
            panel_surface.blit(text, (15, y_offset))
            
            value_text = self.font.render(str(value), True, UI_ACCENT_COLOR)
            panel_surface.blit(value_text, (140, y_offset))
            y_offset += 22
        
        # DNA/Genes section
        y_offset += 10
        gene_title = self.font.render("Genetic Traits", True, color)
        panel_surface.blit(gene_title, (15, y_offset))
        y_offset += 25
        
        if hasattr(self.selected_agent, 'dna') and hasattr(self.selected_agent.dna, 'genes'):
            # Show key genes
            key_genes = ['speed', 'vision', 'size', 'energy_efficiency', 
                        'bravery', 'metabolism']
            
            for gene in key_genes:
                if gene in self.selected_agent.dna.genes:
                    value = self.selected_agent.dna.genes[gene]
                    gene_label = gene.replace('_', ' ').title()
                    
                    # Gene name
                    text = self.font.render(f"{gene_label}:", True, (200, 200, 210))
                    panel_surface.blit(text, (20, y_offset))
                    
                    # Bar visualization
                    bar_x = 145
                    bar_y = y_offset + 5
                    bar_width = self.rect.width - bar_x - 60
                    bar_height = 8
                    
                    # Background bar
                    pygame.draw.rect(panel_surface, (60, 60, 70),
                                   (bar_x, bar_y, bar_width, bar_height),
                                   border_radius=4)
                    
                    # Value bar (normalize to 0-1 range roughly)
                    if gene == 'speed':
                        normalized = min(1.0, value / 5.0)
                    elif gene == 'vision':
                        normalized = min(1.0, value / 300.0)
                    elif gene == 'size':
                        normalized = min(1.0, value / 12.0)
                    else:
                        normalized = min(1.0, value / 2.0)
                    
                    filled_width = int(bar_width * normalized)
                    pygame.draw.rect(panel_surface, color,
                                   (bar_x, bar_y, filled_width, bar_height),
                                   border_radius=4)
                    
                    # Value text
                    value_text = self.font.render(f"{value:.1f}", True, UI_TEXT_COLOR)
                    panel_surface.blit(value_text, (bar_x + bar_width + 5, y_offset))
                    
                    y_offset += 20
        
        # Special abilities
        y_offset += 10
        if y_offset < self.rect.height - 60:
            abilities_title = self.font.render("Abilities", True, color)
            panel_surface.blit(abilities_title, (15, y_offset))
            y_offset += 25
            
            # Species-specific abilities
            abilities = []
            if species_name.lower() == 'hunter':
                abilities.append("🗡️ Attack prey")
            elif species_name.lower() == 'protector':
                abilities.append("🛡️ Stun predators")
            elif species_name.lower() == 'parasite':
                abilities.append("🦠 Drain energy")
            elif species_name.lower() == 'scavenger':
                abilities.append("🍖 Eat carcasses")
            elif species_name.lower() == 'grazer':
                abilities.append("🌿 Herd behavior")
            
            for ability in abilities:
                ability_text = self.font.render(ability, True, (180, 180, 190))
                panel_surface.blit(ability_text, (20, y_offset))
                y_offset += 22
        
        surface.blit(panel_surface, self.rect.topleft)
    
    def draw_marker(self, surface, camera_offset, zoom):
        """Draw marker on selected agent in world view."""
        if not self.visible or not self.selected_agent:
            return
        
        # Calculate screen position
        screen_x = int(self.selected_agent.x * zoom + camera_offset[0])
        screen_y = int(self.selected_agent.y * zoom + camera_offset[1])
        
        # Get species color
        species_name = self.selected_agent.__class__.__name__.lower()
        color = SPECIES_STYLE.get(species_name, {}).get("color", UI_ACCENT_COLOR)
        
        # Draw pulsing circle around agent
        import math
        import pygame.time
        pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 0.3 + 0.7
        radius = int((15 + self.selected_agent.size) * zoom * pulse)
        
        # Outer glow
        for i in range(3):
            alpha = int(100 / (i + 1))
            glow_surface = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*color, alpha), 
                             (radius + 5, radius + 5), radius + i * 2, 2)
            surface.blit(glow_surface, (screen_x - radius - 5, screen_y - radius - 5))
        
        # Selection circle
        pygame.draw.circle(surface, color, (screen_x, screen_y), radius, 2)
        
        # Arrow pointing down
        arrow_points = [
            (screen_x, screen_y - radius - 15),
            (screen_x - 5, screen_y - radius - 25),
            (screen_x + 5, screen_y - radius - 25),
        ]
        pygame.draw.polygon(surface, color, arrow_points)


class Tooltip:
    """Hover tooltip for UI elements."""
    
    def __init__(self):
        self.text = ""
        self.position = (0, 0)
        self.visible = False
        self.font = None
        self.timer = 0
        self.delay = 30  # Frames before showing
    
    def show(self, text, position):
        """Show tooltip at position."""
        if text != self.text:
            self.timer = 0
        self.text = text
        self.position = position
        self.visible = True
    
    def hide(self):
        """Hide tooltip."""
        self.visible = False
        self.timer = 0
    
    def update(self):
        """Update tooltip state."""
        if self.visible:
            self.timer += 1
    
    def draw(self, surface):
        """Draw tooltip."""
        if not self.visible or self.timer < self.delay or not self.text:
            return
        
        if not self.font:
            self.font = pygame.font.Font(None, 18)
        
        # Render text
        text_surface = self.font.render(self.text, True, UI_TEXT_COLOR)
        width = text_surface.get_width() + 20
        height = text_surface.get_height() + 10
        
        # Position (avoid going off screen)
        x = min(self.position[0] + 15, surface.get_width() - width - 5)
        y = min(self.position[1] + 15, surface.get_height() - height - 5)
        
        # Background
        tooltip_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        tooltip_surface.fill((40, 42, 54, 240))
        pygame.draw.rect(tooltip_surface, UI_BORDER_COLOR, (0, 0, width, height), 
                        1, border_radius=5)
        
        # Text
        tooltip_surface.blit(text_surface, (10, 5))
        
        surface.blit(tooltip_surface, (x, y))

