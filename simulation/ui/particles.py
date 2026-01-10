"""
Particle system for visual effects.
"""
import pygame
import random
import math
from typing import List, Tuple


class Particle:
    """Single particle with physics."""
    
    def __init__(self, x, y, vx, vy, color, size, lifetime, fade=True, gravity=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.fade = fade
        self.gravity = gravity
        self.alpha = 255
        
    def update(self):
        """Update particle position and lifetime."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        
        if self.fade:
            self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        return self.lifetime > 0
    
    def draw(self, surface):
        """Draw the particle."""
        if self.alpha <= 0:
            return
            
        # Create a surface with alpha channel
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        
        # Draw the particle with alpha
        color_with_alpha = (*self.color[:3], self.alpha)
        pygame.draw.circle(particle_surface, color_with_alpha, 
                          (int(self.size), int(self.size)), int(self.size))
        
        surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


class ParticleEmitter:
    """Manages a collection of particles."""
    
    def __init__(self, max_particles=1000):
        self.particles: List[Particle] = []
        self.max_particles = max_particles
        
    def emit(self, x, y, count, color, speed_range=(1, 3), size_range=(2, 5), 
             lifetime_range=(30, 60), angle_range=(0, 360), gravity=0.0, fade=True):
        """Emit particles from a point."""
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
                
            angle = random.uniform(angle_range[0], angle_range[1]) * math.pi / 180
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            
            particle = Particle(x, y, vx, vy, color, size, lifetime, fade, gravity)
            self.particles.append(particle)
    
    def emit_explosion(self, x, y, color, intensity=1.0):
        """Create an explosion effect."""
        count = int(30 * intensity)
        self.emit(x, y, count, color, 
                 speed_range=(3 * intensity, 8 * intensity),
                 size_range=(3, 8),
                 lifetime_range=(20, 50),
                 gravity=0.1)
    
    def emit_trail(self, x, y, color, intensity=1.0):
        """Create a trailing effect."""
        count = int(3 * intensity)
        self.emit(x, y, count, color,
                 speed_range=(0.2, 1),
                 size_range=(1, 3),
                 lifetime_range=(10, 25),
                 fade=True)
    
    def emit_sparkle(self, x, y, color):
        """Create a sparkle effect."""
        self.emit(x, y, 5, color,
                 speed_range=(0.5, 2),
                 size_range=(2, 4),
                 lifetime_range=(15, 30))
    
    def emit_meteor(self, x, y):
        """Create a meteor impact effect."""
        # Fire colors
        colors = [
            (255, 100, 0),   # Orange
            (255, 200, 0),   # Yellow-orange
            (255, 50, 0),    # Red-orange
            (200, 200, 200), # Smoke gray
        ]
        for color in colors:
            self.emit(x, y, 20, color,
                     speed_range=(5, 15),
                     size_range=(4, 10),
                     lifetime_range=(30, 60),
                     gravity=0.15)
    
    def emit_wave(self, x, y):
        """Create a tsunami wave effect."""
        water_colors = [
            (25, 70, 140),
            (50, 100, 170),
            (200, 220, 255),
        ]
        for color in water_colors:
            self.emit(x, y, 25, color,
                     speed_range=(3, 10),
                     size_range=(5, 12),
                     lifetime_range=(40, 70),
                     angle_range=(-45, 45),
                     gravity=0.08)
    
    def emit_earthquake(self, x, y):
        """Create an earthquake effect."""
        earth_colors = [
            (139, 90, 43),   # Brown
            (160, 110, 60),  # Light brown
            (100, 70, 40),   # Dark brown
        ]
        for color in earth_colors:
            self.emit(x, y, 20, color,
                     speed_range=(2, 8),
                     size_range=(3, 8),
                     lifetime_range=(25, 50),
                     gravity=0.2)
    
    def update(self):
        """Update all particles."""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, surface):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)
    
    def clear(self):
        """Remove all particles."""
        self.particles.clear()


class ScreenEffect:
    """Full-screen visual effects like screen shake, flash, etc."""
    
    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
        self.flash_alpha = 0
        self.flash_color = (255, 255, 255)
        self.flash_duration = 0
        
    def trigger_shake(self, intensity=10, duration=20):
        """Trigger screen shake effect."""
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def trigger_flash(self, color=(255, 255, 255), intensity=128, duration=10):
        """Trigger screen flash effect."""
        self.flash_color = color
        self.flash_alpha = intensity
        self.flash_duration = duration
    
    def update(self):
        """Update effects."""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            if self.shake_duration == 0:
                self.shake_intensity = 0
        
        if self.flash_duration > 0:
            self.flash_duration -= 1
            self.flash_alpha = int((self.flash_duration / 10) * 128)
    
    def get_shake_offset(self):
        """Get current screen shake offset."""
        if self.shake_duration > 0:
            x = random.randint(-self.shake_intensity, self.shake_intensity)
            y = random.randint(-self.shake_intensity, self.shake_intensity)
            return (x, y)
        return (0, 0)
    
    def draw_flash(self, surface):
        """Draw flash effect on surface."""
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash_surface.fill((*self.flash_color, self.flash_alpha))
            surface.blit(flash_surface, (0, 0))

