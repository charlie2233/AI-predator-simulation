"""
Achievement and milestone system for the game.
"""
import pygame
import json
import os
from typing import Dict, List, Tuple
from collections import deque


class Achievement:
    """Single achievement definition."""
    
    def __init__(self, id, title, description, icon_color, condition_func, reward_text=""):
        self.id = id
        self.title = title
        self.description = description
        self.icon_color = icon_color
        self.condition_func = condition_func
        self.reward_text = reward_text
        self.unlocked = False
        self.unlock_time = 0
        self.progress = 0.0
    
    def check(self, game_state):
        """Check if achievement is unlocked."""
        if self.unlocked:
            return False
        
        result = self.condition_func(game_state)
        
        if isinstance(result, bool):
            if result:
                self.unlocked = True
                return True
        elif isinstance(result, float):
            self.progress = min(1.0, result)
            if self.progress >= 1.0:
                self.unlocked = True
                return True
        
        return False


class AchievementManager:
    """Manages all achievements and notifications."""
    
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.notification_queue = deque(maxlen=5)
        self.current_notification = None
        self.notification_timer = 0
        self.save_file = "saves/achievements.json"
        
        self._init_achievements()
        self._load_progress()
    
    def _init_achievements(self):
        """Initialize all achievement definitions."""
        
        # Population Achievements
        self.add_achievement(
            "first_gen", "First Generation", 
            "Complete your first generation",
            (80, 250, 123),
            lambda s: s.get("generation", 0) >= 2
        )
        
        self.add_achievement(
            "veteran", "Veteran Overseer",
            "Reach generation 10",
            (139, 233, 253),
            lambda s: s.get("generation", 0) >= 10
        )
        
        self.add_achievement(
            "master", "Master of Evolution",
            "Reach generation 50",
            (189, 147, 249),
            lambda s: s.get("generation", 0) >= 50
        )
        
        self.add_achievement(
            "population_boom", "Population Boom",
            "Have 200+ total agents alive",
            (80, 250, 123),
            lambda s: s.get("total_agents", 0) >= 200
        )
        
        self.add_achievement(
            "mega_city", "Mega City",
            "Have 500+ total agents alive",
            (255, 184, 108),
            lambda s: s.get("total_agents", 0) >= 500
        )
        
        # Extinction & Recovery
        self.add_achievement(
            "phoenix", "Phoenix Rising",
            "Recover a species from extinction",
            (255, 85, 85),
            lambda s: s.get("extinctions", 0) >= 1
        )
        
        self.add_achievement(
            "resilient", "Resilient Ecosystem",
            "Survive 5 extinctions",
            (255, 121, 198),
            lambda s: s.get("extinctions", 0) >= 5
        )
        
        # Diversity
        self.add_achievement(
            "diverse", "Diverse Ecosystem",
            "Have all 7 species alive simultaneously",
            (189, 147, 249),
            lambda s: s.get("species_alive", 0) >= 7
        )
        
        # Balance
        self.add_achievement(
            "balanced", "Perfect Balance",
            "Maintain stable populations for 10 generations",
            (139, 233, 253),
            lambda s: s.get("stable_generations", 0) >= 10
        )
        
        # Events
        self.add_achievement(
            "survivor", "Disaster Survivor",
            "Survive your first disaster event",
            (255, 184, 108),
            lambda s: s.get("disasters_survived", 0) >= 1
        )
        
        self.add_achievement(
            "apocalypse", "Apocalypse Survivor",
            "Survive 10 disaster events",
            (255, 85, 85),
            lambda s: s.get("disasters_survived", 0) >= 10
        )
        
        # Evolution
        self.add_achievement(
            "speedster", "Speed Evolution",
            "Evolve a species with 5.0+ speed",
            (255, 255, 140),
            lambda s: s.get("max_speed", 0) >= 5.0
        )
        
        self.add_achievement(
            "eagle_eye", "Eagle Eye",
            "Evolve a species with 300+ vision",
            (139, 233, 253),
            lambda s: s.get("max_vision", 0) >= 300
        )
        
        self.add_achievement(
            "titan", "Titan",
            "Evolve a species with size 12+",
            (255, 121, 198),
            lambda s: s.get("max_size", 0) >= 12
        )
        
        # Time
        self.add_achievement(
            "marathon", "Marathon Runner",
            "Run a single generation for 2000+ steps",
            (189, 147, 249),
            lambda s: s.get("max_episode_length", 0) >= 2000
        )
    
    def add_achievement(self, id, title, description, color, condition, reward=""):
        """Add an achievement to the system."""
        achievement = Achievement(id, title, description, color, condition, reward)
        self.achievements[id] = achievement
    
    def check_achievements(self, game_state):
        """Check all achievements against current game state."""
        newly_unlocked = []
        
        for achievement in self.achievements.values():
            if achievement.check(game_state):
                newly_unlocked.append(achievement)
                self.notification_queue.append(achievement)
        
        if newly_unlocked:
            self._save_progress()
        
        return newly_unlocked
    
    def update(self):
        """Update notification display."""
        if self.notification_timer > 0:
            self.notification_timer -= 1
            if self.notification_timer == 0:
                self.current_notification = None
        
        if self.current_notification is None and self.notification_queue:
            self.current_notification = self.notification_queue.popleft()
            self.notification_timer = 180  # 3 seconds at 60 FPS
    
    def draw_notification(self, surface):
        """Draw achievement notification popup."""
        if self.current_notification is None:
            return
        
        # Create notification box
        width = 400
        height = 100
        x = surface.get_width() - width - 20
        y = 20
        
        # Animation: slide in/out
        progress = min(1.0, (180 - self.notification_timer) / 30.0)
        if self.notification_timer < 30:
            progress = self.notification_timer / 30.0
        
        x = int(surface.get_width() - (width + 20) * progress)
        
        # Background with glow
        notification_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Outer glow
        glow_rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(notification_surface, (*self.current_notification.icon_color, 50), 
                        glow_rect, border_radius=15)
        
        # Main box
        main_rect = pygame.Rect(3, 3, width - 6, height - 6)
        pygame.draw.rect(notification_surface, (40, 42, 54, 240), main_rect, border_radius=12)
        pygame.draw.rect(notification_surface, self.current_notification.icon_color, 
                        main_rect, 3, border_radius=12)
        
        # Icon
        icon_size = 60
        icon_x = 15
        icon_y = (height - icon_size) // 2
        pygame.draw.circle(notification_surface, self.current_notification.icon_color,
                          (icon_x + icon_size // 2, icon_y + icon_size // 2), icon_size // 2)
        
        # Trophy icon
        font_large = pygame.font.Font(None, 48)
        trophy_text = font_large.render("🏆", True, (40, 42, 54))
        notification_surface.blit(trophy_text, (icon_x + 8, icon_y + 5))
        
        # Text
        font_title = pygame.font.Font(None, 24)
        font_desc = pygame.font.Font(None, 18)
        
        title_text = font_title.render("Achievement Unlocked!", True, (255, 184, 108))
        name_text = font_title.render(self.current_notification.title, True, (248, 248, 242))
        desc_text = font_desc.render(self.current_notification.description, True, (150, 150, 160))
        
        notification_surface.blit(title_text, (icon_x + icon_size + 15, 10))
        notification_surface.blit(name_text, (icon_x + icon_size + 15, 35))
        notification_surface.blit(desc_text, (icon_x + icon_size + 15, 65))
        
        surface.blit(notification_surface, (x, y))
    
    def draw_panel(self, surface, x, y, width, height):
        """Draw achievements panel."""
        font_title = pygame.font.Font(None, 28)
        font_item = pygame.font.Font(None, 20)
        
        # Background
        pygame.draw.rect(surface, (40, 42, 54), (x, y, width, height), border_radius=10)
        pygame.draw.rect(surface, (98, 114, 164), (x, y, width, height), 2, border_radius=10)
        
        # Title
        title = font_title.render("Achievements", True, (189, 147, 249))
        surface.blit(title, (x + 20, y + 15))
        
        # Stats
        total = len(self.achievements)
        unlocked = sum(1 for a in self.achievements.values() if a.unlocked)
        stats = font_item.render(f"{unlocked}/{total} Unlocked", True, (150, 150, 160))
        surface.blit(stats, (x + width - 150, y + 20))
        
        # List achievements
        scroll_y = y + 60
        for achievement in list(self.achievements.values())[:8]:  # Show first 8
            alpha = 255 if achievement.unlocked else 80
            
            # Icon
            pygame.draw.circle(surface, (*achievement.icon_color, alpha),
                             (x + 35, scroll_y + 15), 12)
            
            # Text
            color = (248, 248, 242) if achievement.unlocked else (100, 100, 110)
            name = font_item.render(achievement.title, True, color)
            surface.blit(name, (x + 60, scroll_y + 5))
            
            if achievement.unlocked:
                check = font_item.render("✓", True, (80, 250, 123))
                surface.blit(check, (x + width - 40, scroll_y + 5))
            elif achievement.progress > 0:
                prog_text = font_item.render(f"{int(achievement.progress * 100)}%", 
                                            True, (150, 150, 160))
                surface.blit(prog_text, (x + width - 60, scroll_y + 5))
            
            scroll_y += 35
            if scroll_y > y + height - 40:
                break
    
    def get_stats(self):
        """Get achievement statistics."""
        total = len(self.achievements)
        unlocked = sum(1 for a in self.achievements.values() if a.unlocked)
        return {
            "total": total,
            "unlocked": unlocked,
            "percentage": (unlocked / total * 100) if total > 0 else 0
        }
    
    def _save_progress(self):
        """Save achievement progress to file."""
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
        
        data = {
            aid: {
                "unlocked": achievement.unlocked,
                "progress": achievement.progress
            }
            for aid, achievement in self.achievements.items()
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save achievements: {e}")
    
    def _load_progress(self):
        """Load achievement progress from file."""
        if not os.path.exists(self.save_file):
            return
        
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            
            for aid, progress in data.items():
                if aid in self.achievements:
                    self.achievements[aid].unlocked = progress.get("unlocked", False)
                    self.achievements[aid].progress = progress.get("progress", 0.0)
        except Exception as e:
            print(f"Failed to load achievements: {e}")
    
    def reset_all(self):
        """Reset all achievements (for testing)."""
        for achievement in self.achievements.values():
            achievement.unlocked = False
            achievement.progress = 0.0
        self._save_progress()

