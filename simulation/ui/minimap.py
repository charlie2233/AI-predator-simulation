"""
Minimap component for navigation.
"""
import pygame
from simulation.config import SPECIES_STYLE, UI_PANEL_BG, UI_BORDER_COLOR, UI_TEXT_COLOR


class Minimap:
    """Minimap showing world overview and camera position."""
    
    def __init__(self, x, y, width, height, world_width, world_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.world_width = world_width
        self.world_height = world_height
        self.scale_x = width / world_width
        self.scale_y = height / world_height
        self.font = None
        self.dragging = False
    
    def handle_event(self, event, camera_offset, zoom, viewport_width, viewport_height):
        """Handle mouse interaction with minimap."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                return self._get_camera_target(event.pos, viewport_width, viewport_height, zoom)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            return self._get_camera_target(event.pos, viewport_width, viewport_height, zoom)
        return None
    
    def _get_camera_target(self, pos, viewport_width, viewport_height, zoom):
        """Convert minimap click to camera target position."""
        rel_x = (pos[0] - self.rect.x) / self.rect.width
        rel_y = (pos[1] - self.rect.y) / self.rect.height
        
        # World coordinates
        world_x = rel_x * self.world_width
        world_y = rel_y * self.world_height
        
        # Camera offset to center on this point
        offset_x = -(world_x * zoom - viewport_width / 2)
        offset_y = -(world_y * zoom - viewport_height / 2)
        
        return (offset_x, offset_y)
    
    def draw(self, surface, world, camera_offset, zoom, viewport_width, viewport_height):
        """Draw the minimap."""
        if not self.font:
            self.font = pygame.font.Font(None, 16)
        
        # Background
        minimap_surface = pygame.Surface((self.rect.width, self.rect.height))
        minimap_surface.fill((20, 25, 35))
        
        # Draw water zones
        for zx, zy, zw, zh, ztype in world.water_zones:
            color = (15, 50, 100) if ztype == "sea" else (15, 70, 50)
            rect = pygame.Rect(
                int(zx * self.scale_x),
                int(zy * self.scale_y),
                int(zw * self.scale_x),
                int(zh * self.scale_y)
            )
            pygame.draw.rect(minimap_surface, color, rect)
        
        # Draw food as tiny dots
        for food in world.food[:200]:  # Limit for performance
            x = int(food.x * self.scale_x)
            y = int(food.y * self.scale_y)
            pygame.draw.circle(minimap_surface, (60, 150, 60), (x, y), 1)
        
        # Draw agents
        for agent in world.get_all_agents():
            x = int(agent.x * self.scale_x)
            y = int(agent.y * self.scale_y)
            
            species_name = agent.__class__.__name__.lower()
            color = SPECIES_STYLE.get(species_name, {}).get("color", (255, 255, 255))
            
            # Draw as small dots with species color
            pygame.draw.circle(minimap_surface, color, (x, y), 2)
        
        # Draw camera viewport
        viewport_x = int(-camera_offset[0] / zoom * self.scale_x)
        viewport_y = int(-camera_offset[1] / zoom * self.scale_y)
        viewport_w = int(viewport_width / zoom * self.scale_x)
        viewport_h = int(viewport_height / zoom * self.scale_y)
        
        viewport_rect = pygame.Rect(viewport_x, viewport_y, viewport_w, viewport_h)
        pygame.draw.rect(minimap_surface, (255, 255, 255), viewport_rect, 2)
        pygame.draw.rect(minimap_surface, (255, 255, 255, 50), viewport_rect)
        
        # Blit to main surface
        surface.blit(minimap_surface, self.rect.topleft)
        
        # Border
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2, border_radius=5)
        
        # Title
        title = self.font.render("Minimap", True, UI_TEXT_COLOR)
        surface.blit(title, (self.rect.x + 5, self.rect.y - 20))

