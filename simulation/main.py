"""
Enhanced main simulation with professional UI/UX.
Commercial-quality game implementation with full integration.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pygame
import math
from simulation.world import World
from simulation.ui.control_panel import ControlPanel
from simulation.ui.visualization import PopulationGraph, TraitGraph, LogPanel
from simulation.ui.main_menu import MainMenu
from simulation.ui.particles import ParticleEmitter, ScreenEffect
from simulation.ui.achievements import AchievementManager
from simulation.ui.minimap import Minimap
from simulation.ui.agent_inspector import AgentInspector, Tooltip
from simulation.ui.sound_manager import SoundManager
from simulation.ui.tutorial import TutorialManager, HelpMenu
from simulation.ui.settings_menu import SettingsMenu
from simulation.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    STATS_PANEL_WIDTH,
    FPS,
    BLACK,
    WHITE,
    SPECIES_STYLE,
    UI_BG_COLOR,
    UI_TEXT_COLOR,
    UI_BORDER_COLOR,
    UI_PANEL_BG,
    UI_ACCENT_COLOR,
    SEA_COLOR,
    RIVER_COLOR,
)


class EnhancedSimulation:
    """Enhanced simulation with commercial-quality UI/UX and full feature integration."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🧬 Evolution Sandbox - AI Ecosystem Simulator")

        self.world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.clock = pygame.time.Clock()
        self.save_path = os.path.join(os.getcwd(), "saves", "latest.json")
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT, {"save_path": self.save_path})

        self.viewport_width = WINDOW_WIDTH - STATS_PANEL_WIDTH
        
        # Core UI Panels
        self.control_panel = ControlPanel(self.viewport_width + 10, 10, STATS_PANEL_WIDTH - 20, WINDOW_HEIGHT - 20)
        self.population_graph = PopulationGraph(
            self.viewport_width + 10, 420, STATS_PANEL_WIDTH - 20, 140, species_names=list(SPECIES_STYLE.keys())
        )
        self.trait_graph = TraitGraph(self.viewport_width + 10, 580, STATS_PANEL_WIDTH - 20, 110, self._current_trait_title())
        self.log_panel = LogPanel(self.viewport_width + 10, 700, STATS_PANEL_WIDTH - 20, 50)

        # Advanced UI Components (optimized for CPU performance)
        self.main_menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.particle_emitter = ParticleEmitter(max_particles=500)  # Reduced from 2000 for better performance
        self.screen_effects = ScreenEffect()
        self.achievement_manager = AchievementManager()
        self.minimap = Minimap(20, WINDOW_HEIGHT - 170, 150, 150, WORLD_WIDTH, WORLD_HEIGHT)
        self.agent_inspector = AgentInspector(self.viewport_width - 270, 20, 250, 350)
        self.tooltip = Tooltip()
        self.sound_manager = SoundManager()
        self.tutorial_manager = TutorialManager()
        self.help_menu = HelpMenu()
        self.settings_menu = SettingsMenu()

        # Game State
        self.running = True
        self.paused = True
        self.started = False
        self.scene = "menu"  # menu | play | achievements
        self.update_counter = 0
        self.pending_event_type = None
        self.prev_episode_step = 0
        self.zoom = 0.6
        self.camera_offset = [0, 0]
        self.target_camera_offset = [0, 0]
        self.has_save = os.path.exists(self.save_path)
        self.selected_agent = None
        self.show_achievements_panel = False
        self.last_disaster_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Global keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                # Help menu toggle (works everywhere)
                if event.key == pygame.K_h and self.scene == "play":
                    self.help_menu.toggle()
                    continue
                
                # Tutorial handling
                if self.tutorial_manager.active:
                    self.tutorial_manager.handle_event(event)
                    continue
                
                # Settings menu
                if self.settings_menu.visible:
                    self.settings_menu.handle_event(event, self.sound_manager)
                    continue
                
                # Help menu
                if self.help_menu.visible:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_h:
                        self.help_menu.toggle()
                    continue
                
                # Main game controls
                if event.key == pygame.K_ESCAPE:
                    if self.agent_inspector.visible:
                        self.agent_inspector.deselect()
                    elif self.show_achievements_panel:
                        self.show_achievements_panel = False
                    elif self.scene == "menu":
                        self.running = False
                    else:
                        self.scene = "menu"
                        self.paused = True
                        self.main_menu.update()  # Reset menu animations
                elif event.key == pygame.K_SPACE and self.scene == "play":
                    self.paused = not self.paused
                    self.control_panel.paused = self.paused
                    self.control_panel.buttons["pause"].text = "Resume" if self.paused else "Pause"
                elif event.key == pygame.K_r and self.scene == "play":
                    self._reset_generation()
                elif event.key == pygame.K_a and self.scene == "play":
                    self.show_achievements_panel = not self.show_achievements_panel
                elif event.key == pygame.K_c and self.scene == "menu":
                    self.main_menu.show_credits = not self.main_menu.show_credits
            
            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.scene == "play":
                    # Check minimap interaction first
                    minimap_result = self.minimap.handle_event(
                        event, self.camera_offset, self.zoom,
                        self.viewport_width, WINDOW_HEIGHT
                    )
                    if minimap_result:
                        self.target_camera_offset = list(minimap_result)
                        continue
                    
                    # Check agent selection
                    if event.button == 1 and not self.pending_event_type:
                        clicked_agent = self._get_agent_at_pos(event.pos)
                        if clicked_agent:
                            self.agent_inspector.select_agent(clicked_agent)
                            self.selected_agent = clicked_agent
                            self.sound_manager.play_ui_click()
                            continue
                    
                    # Check world click for events
                    if event.button == 1 and self.pending_event_type:
                        self._handle_world_click(event)
                        continue
                
            # Scroll wheel zoom
            if event.type == pygame.MOUSEWHEEL and self.scene == "play":
                self._handle_zoom(event.y)
            
            # Handle UI-specific events
            if self.scene == "menu":
                self._handle_menu_event(event)
            elif self.scene == "play":
                self._handle_play_events(event)

    def _handle_play_events(self, event):
        """Handle events during gameplay."""
        actions = self.control_panel.handle_event(event)
        
        if actions.get("toggle_pause"):
            self.paused = self.control_panel.paused
        if actions.get("reset_gen"):
            self._reset_generation()
        if actions.get("reset_all"):
            self._reset_all()
        if actions.get("export"):
            self._export_stats()
        if actions.get("trait_changed"):
            self.trait_graph.title = self._current_trait_title()
            self.trait_graph.update(self.world.populations.get("grazer", []), self._current_trait())
        if "collapse_mode" in actions:
            self.world.collapse_only = actions["collapse_mode"]
        if actions.get("event_armed"):
            self.pending_event_type = actions["event_armed"]
            self.log_panel.push(f"⚡ Armed {self.pending_event_type}. Click world to trigger.")

    def _get_agent_at_pos(self, pos):
        """Get agent at screen position."""
        x, y = pos
        # Convert screen to world coordinates
        world_x = (x - self.camera_offset[0]) / self.zoom
        world_y = (y - self.camera_offset[1]) / self.zoom
        
        # Find closest agent within click radius
        click_radius = 20 / self.zoom
        closest_agent = None
        closest_dist = float('inf')
        
        for agent in self.world.get_all_agents():
            dx = agent.x - world_x
            dy = agent.y - world_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < click_radius and dist < closest_dist:
                closest_dist = dist
                closest_agent = agent
        
        return closest_agent

    def _handle_world_click(self, event):
        """Handle click on world for manual events."""
        x, y = event.pos
        # Adjust for zoom and offset
        world_x = (x - self.camera_offset[0]) / self.zoom
        world_y = (y - self.camera_offset[1]) / self.zoom
        
        if 0 <= world_x <= WORLD_WIDTH and 0 <= world_y <= WORLD_HEIGHT and self.pending_event_type:
            # Apply event
            self.world.apply_manual_event(self.pending_event_type, (world_x, world_y))
            self.log_panel.push(f"💥 {self.pending_event_type.title()} at ({int(world_x)}, {int(world_y)})")
            
            # Visual effects
            if self.pending_event_type == "meteor":
                self.particle_emitter.emit_meteor(x, y)
                self.screen_effects.trigger_shake(15, 30)
                self.screen_effects.trigger_flash((255, 100, 0), 100, 20)
            elif self.pending_event_type == "tsunami":
                self.particle_emitter.emit_wave(x, y)
                self.screen_effects.trigger_shake(10, 25)
                self.screen_effects.trigger_flash((50, 100, 200), 80, 15)
            elif self.pending_event_type == "earthquake":
                self.particle_emitter.emit_earthquake(x, y)
                self.screen_effects.trigger_shake(20, 40)
                self.screen_effects.trigger_flash((139, 90, 43), 70, 10)
            
            self.sound_manager.play_disaster()
            self.pending_event_type = None
            self.last_disaster_time = pygame.time.get_ticks()

    def update(self):
        """Update game state and all UI components."""
        # Update menu animations
        if self.scene == "menu":
            self.main_menu.update()
            return
        
        # Update tutorial
        if self.tutorial_manager.active:
            return
        
        # Update gameplay
        if self.scene == "play":
            # Update particle effects and screen effects
            self.particle_emitter.update()
            self.screen_effects.update()
            
            # Update agent inspector
            self.agent_inspector.update()
            
            # Update achievement notifications
            self.achievement_manager.update()
            
            # Update tooltip
            self.tooltip.update()
            
            # Smooth camera following
            if self.settings_menu.get_setting("camera_smoothing", True):
                smoothing = 0.15
                self.camera_offset[0] += (self.target_camera_offset[0] - self.camera_offset[0]) * smoothing
                self.camera_offset[1] += (self.target_camera_offset[1] - self.camera_offset[1]) * smoothing
            else:
                self.camera_offset = list(self.target_camera_offset)
            
            # Run simulation
            if not self.paused:
                speed = int(self.control_panel.simulation_speed)
                for _ in range(max(1, speed)):
                    self.world.update()
                    
                    # Add particle trails for moving agents (if enabled)
                    if self.settings_menu.get_setting("show_trails", False):
                        for agent in self.world.get_all_agents()[:20]:  # Reduced to 20 for better CPU performance
                            if hasattr(agent, 'vx') and hasattr(agent, 'vy'):
                                speed_magnitude = math.sqrt(agent.vx**2 + agent.vy**2)
                                if speed_magnitude > 0.5:
                                    species_name = agent.__class__.__name__.lower()
                                    color = SPECIES_STYLE.get(species_name, {}).get("color", WHITE)
                                    self.particle_emitter.emit_trail(
                                        agent.x * self.zoom + self.camera_offset[0],
                                        agent.y * self.zoom + self.camera_offset[1],
                                        color, intensity=0.2  # Lower intensity for less particles
                                    )
                
                self.update_counter += 1
                
                # Periodic updates
                if self.update_counter % 10 == 0:
                    self.population_graph.update(self.world)
                    selected_trait = self._current_trait()
                    self.trait_graph.title = self._current_trait_title()
                    self.trait_graph.update(self.world.populations.get("grazer", []), selected_trait)
                    self._pull_logs()
                    self._detect_generation_reset()
                
                # Check achievements every 30 frames
                if self.update_counter % 30 == 0:
                    self._check_achievements()
            
            # Update control panel
            self.control_panel.update(self.world)

    def draw(self):
        """Draw all visual elements with commercial quality."""
        self.screen.fill(UI_BG_COLOR)
        
        # Menu scene
        if self.scene == "menu":
            self._draw_menu_scene()
            pygame.display.flip()
            return
        
        # Gameplay scene
        if self.scene == "play":
            self._draw_game_world()
            self._draw_ui_panels()
            self._draw_overlays()
        
        pygame.display.flip()
    
    def _draw_game_world(self):
        """Draw the game world with all effects."""
        # Beautiful gradient background for world
        world_bg_top = (15, 20, 35)
        world_bg_bottom = (25, 30, 45)
        for y in range(WORLD_HEIGHT):
            ratio = y / WORLD_HEIGHT
            color = tuple(int(world_bg_top[i] + (world_bg_bottom[i] - world_bg_top[i]) * ratio) for i in range(3))
            pygame.draw.line(self.world_surface, color, (0, y), (WORLD_WIDTH, y))
        
        # Add subtle stars/particles in background
        import random
        random.seed(42)  # Consistent stars
        for _ in range(100):
            star_x = random.randint(0, WORLD_WIDTH)
            star_y = random.randint(0, WORLD_HEIGHT)
            brightness = random.randint(100, 200)
            pygame.draw.circle(self.world_surface, (brightness, brightness, brightness + 30), (star_x, star_y), 1)

        # Water zones overlay (sea vs river colors)
        for zx, zy, zw, zh, ztype in self.world.water_zones:
            water_rect = pygame.Rect(int(zx), int(zy), int(zw), int(zh))
            if ztype == "sea":
                color = SEA_COLOR
                accent = (min(255, SEA_COLOR[0] + 30), min(255, SEA_COLOR[1] + 30), min(255, SEA_COLOR[2] + 30))
            else:
                color = RIVER_COLOR
                accent = (min(255, RIVER_COLOR[0] + 40), min(255, RIVER_COLOR[1] + 40), min(255, RIVER_COLOR[2] + 40))
            pygame.draw.rect(self.world_surface, color, water_rect)
            for i in range(0, int(zh), 18):
                pygame.draw.line(self.world_surface, accent, (int(zx), int(zy + i)), (int(zx + zw), int(zy + i)), 1)

        # Draw world entities
        for food in self.world.food:
            food.draw(self.world_surface)
        for rock in self.world.rocks:
            rock.draw(self.world_surface)
        for shelter in self.world.shelters:
            shelter.draw(self.world_surface)
        
        # Draw vision ranges if enabled
        if self.settings_menu.get_setting("show_vision", False):
            for agent in self.world.get_all_agents()[:10]:  # Reduced to 10 for better performance
                vision_radius = int(agent.dna.genes.get('vision', 100))
                pygame.draw.circle(self.world_surface, (100, 100, 120, 30), 
                                 (int(agent.x), int(agent.y)), vision_radius, 1)
        
        for agent in self.world.get_all_agents():
            agent.draw(self.world_surface)

        # Apply screen shake
        shake_offset = self.screen_effects.get_shake_offset()
        camera_x = self.camera_offset[0] + shake_offset[0]
        camera_y = self.camera_offset[1] + shake_offset[1]
        
        # Scale and render world
        scaled_surface = pygame.transform.smoothscale(
            self.world_surface,
            (
                min(self.viewport_width, int(WORLD_WIDTH * self.zoom)),
                min(WINDOW_HEIGHT, int(WORLD_HEIGHT * self.zoom)),
            ),
        )
        
        # Clip world view to the viewport area
        self.screen.set_clip(pygame.Rect(0, 0, self.viewport_width, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (int(camera_x), int(camera_y)))
        
        # Draw border
        pygame.draw.rect(
            self.screen,
            UI_BORDER_COLOR,
            (
                int(camera_x),
                int(camera_y),
                min(self.viewport_width, int(WORLD_WIDTH * self.zoom)),
                min(WINDOW_HEIGHT, int(WORLD_HEIGHT * self.zoom)),
            ),
            2,
        )
        self.screen.set_clip(None)  # Reset clip for UI
    
    def _draw_ui_panels(self):
        """Draw all UI panels."""
        # Draw divider line
        pygame.draw.line(self.screen, UI_BORDER_COLOR, 
                        (self.viewport_width, 0), 
                        (self.viewport_width, WINDOW_HEIGHT), 3)
        
        # Main control panels
        self.control_panel.draw(self.screen)
        self.population_graph.draw(self.screen)
        self.trait_graph.draw(self.screen)
        self.log_panel.draw(self.screen)
        
        # Minimap (if enabled)
        if self.settings_menu.get_setting("show_minimap", True):
            self.minimap.draw(self.screen, self.world, self.camera_offset, 
                            self.zoom, self.viewport_width, WINDOW_HEIGHT)
        
        # Agent inspector
        if self.agent_inspector.visible:
            self.agent_inspector.draw(self.screen)
            self.agent_inspector.draw_marker(self.screen, self.camera_offset, self.zoom)
        
        # FPS counter (if enabled)
        if self.settings_menu.get_setting("show_fps", True):
            fps_font = pygame.font.Font(None, 20)
            fps_text = fps_font.render(f"FPS: {int(self.clock.get_fps())}", True, UI_TEXT_COLOR)
            fps_bg = pygame.Surface((fps_text.get_width() + 10, 25), pygame.SRCALPHA)
            fps_bg.fill((40, 42, 54, 200))
            self.screen.blit(fps_bg, (5, 5))
            self.screen.blit(fps_text, (10, 10))
        
        # Particles and effects
        particle_quality = self.settings_menu.get_setting("particle_quality", 1.0)
        if particle_quality > 0:
            self.particle_emitter.draw(self.screen)
        
        # Screen flash effect
        self.screen_effects.draw_flash(self.screen)
    
    def _draw_overlays(self):
        """Draw overlays like menus and notifications."""
        # Pending event overlay
        if self.pending_event_type:
            self._draw_event_overlay()
        
        # Active event notification
        if self.world.active_event_text:
            self._draw_active_event()
        
        # Achievement notifications
        if self.settings_menu.get_setting("show_notifications", True):
            self.achievement_manager.draw_notification(self.screen)
        
        # Achievements panel
        if self.show_achievements_panel:
            panel_x = self.viewport_width // 2 - 250
            panel_y = 100
            self.achievement_manager.draw_panel(self.screen, panel_x, panel_y, 500, 550)
        
        # Tooltip
        if self.settings_menu.get_setting("show_tooltips", True):
            self.tooltip.draw(self.screen)
        
        # Tutorial overlay
        if self.tutorial_manager.active:
            self.tutorial_manager.draw(self.screen)
        
        # Help menu
        if self.help_menu.visible:
            self.help_menu.draw(self.screen)
        
        # Settings menu
        if self.settings_menu.visible:
            self.settings_menu.draw(self.screen)
        
        # Controls hint
        if not self.tutorial_manager.shown_before and not self.tutorial_manager.active:
            self._draw_controls_hint()
    
    def _draw_menu_scene(self):
        """Draw the main menu."""
        self.main_menu.draw(self.screen, self.has_save)

    def run(self):
        """Main game loop with enhanced features."""
        print("=" * 70)
        print("🧬 EVOLUTION SANDBOX - AI Ecosystem Simulator")
        print("=" * 70)
        print("\n✨ Commercial Edition - Fully Enhanced")
        print("\n🎮 Controls:")
        print("  SPACE     - Pause/Resume")
        print("  R         - Reset generation")
        print("  H         - Help menu")
        print("  A         - Achievements")
        print("  ESC       - Menu / Back")
        print("\n🖱️  Mouse:")
        print("  Wheel     - Zoom in/out")
        print("  Click     - Select agent / Place event")
        print("  Minimap   - Jump to location")
        print("\n" + "=" * 70)
        print("\nStarting game... Have fun! 🎉\n")
        
        # Show tutorial on first run
        if not self.tutorial_manager.shown_before:
            self.scene = "menu"  # Start at menu, tutorial option available

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        # Cleanup
        print("\n👋 Thanks for playing Evolution Sandbox!")
        pygame.quit()
        sys.exit()

    def _current_trait(self):
        return self.control_panel.get_selected_trait()

    def _current_trait_title(self):
        trait_name = self._current_trait().replace("_", " ").title()
        return f"Grazer {trait_name} Distribution"

    def _pull_logs(self):
        """Pull extinction logs from world and display."""
        while self.world.extinction_log:
            msg = self.world.extinction_log.pop(0)
            self.log_panel.push(msg)
            # Play extinction sound
            if "extinct" in msg.lower():
                self.sound_manager.play_extinction()

    def _export_stats(self):
        """Export statistics to files."""
        out_json = os.path.join(os.getcwd(), "generation_stats.json")
        out_csv = os.path.join(os.getcwd(), "generation_stats.csv")
        self.world.stats.export_json(out_json)
        self.world.stats.export_csv(out_csv)
        self.log_panel.push("📊 Exported stats to CSV/JSON")

    def _reset_generation(self):
        """Reset current generation with effects."""
        self.world.reset_generation()
        self.population_graph.add_reset_mark()
        self.log_panel.push("🔄 Generation reset")
        self.sound_manager.play_evolution()
        self.screen_effects.trigger_flash((80, 250, 123), 60, 10)
    
    def _reset_all(self):
        """Reset entire simulation."""
        self.world.reset_all(self.control_panel.get_config_overrides())
        self.population_graph.add_reset_mark()
        self.log_panel.push("🔄 Full reset - New world created")
        self.sound_manager.play_evolution()
        self.screen_effects.trigger_flash((139, 233, 253), 80, 15)
        # Reset camera
        self.zoom = 0.6
        self.camera_offset = [0, 0]
        self.target_camera_offset = [0, 0]

    def _check_achievements(self):
        """Check and update achievements based on game state."""
        # Build game state for achievement checking
        all_agents = self.world.get_all_agents()
        game_state = {
            "generation": self.world.generation,
            "total_agents": len(all_agents),
            "extinctions": self.world.run_history.get("extinctions", 0),
            "species_alive": len([s for s, pop in self.world.populations.items() if len(pop) > 0]),
            "stable_generations": 0,  # Would need tracking
            "disasters_survived": getattr(self.world, "disasters_survived", 0),
            "max_speed": max([a.dna.genes.get('speed', 0) for a in all_agents], default=0),
            "max_vision": max([a.dna.genes.get('vision', 0) for a in all_agents], default=0),
            "max_size": max([a.dna.genes.get('size', 0) for a in all_agents], default=0),
            "max_episode_length": self.world.episode_step,
        }
        
        newly_unlocked = self.achievement_manager.check_achievements(game_state)
        
        # Play sound for new achievements
        if newly_unlocked and self.settings_menu.get_setting("show_notifications", True):
            self.sound_manager.play_achievement()
            for achievement in newly_unlocked:
                self.log_panel.push(f"🏆 Achievement: {achievement.title}")

    def _handle_menu_event(self, event):
        """Handle main menu interactions."""
        action = self.main_menu.handle_event(event, self.has_save)
        
        if action == "new_game":
            self._start_new_world()
            self.sound_manager.play_ui_click()
        elif action == "continue":
            if self._load_save():
                self.scene = "play"
                self.paused = False
                self.started = True
                self.sound_manager.play_ui_click()
        elif action == "tutorial":
            self.tutorial_manager.start()
            self.scene = "play"  # Show tutorial over gameplay
            self.sound_manager.play_ui_click()
        elif action == "settings":
            self.settings_menu.toggle()
            self.sound_manager.play_ui_click()
        elif action == "achievements":
            self.show_achievements_panel = True
            self.scene = "play"  # Show achievements panel
            self.sound_manager.play_ui_click()
        elif action == "quit":
            self.running = False

    def _start_new_world(self):
        """Start a new world simulation."""
        self.world.reset_all(self.control_panel.get_config_overrides())
        self.zoom = 0.6
        self.camera_offset = [0, 0]
        self.target_camera_offset = [0, 0]
        self.scene = "play"
        self.paused = False
        self.started = True
        self.has_save = True
        self.selected_agent = None
        self.agent_inspector.deselect()
        
        # Create welcome particles
        for _ in range(50):
            x = self.viewport_width // 2
            y = WINDOW_HEIGHT // 2
            self.particle_emitter.emit_sparkle(x, y, (139, 233, 253))
        
        self.log_panel.push("🌍 New world created - Let evolution begin!")

    def _draw_event_overlay(self):
        """Draw overlay when event is armed."""
        overlay = pygame.Surface((self.viewport_width, 50), pygame.SRCALPHA)
        overlay.fill((40, 42, 54, 220))
        
        # Pulsing border
        import pygame.time
        pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 0.5 + 0.5
        border_color = tuple(int(c * pulse) for c in UI_ACCENT_COLOR)
        pygame.draw.rect(overlay, border_color, (0, 0, self.viewport_width, 50), 3)
        
        font = pygame.font.Font(None, 26)
        icon = "⚡"
        msg = font.render(f"{icon} Armed: {self.pending_event_type.upper()} - Click world to deploy!", 
                         True, UI_ACCENT_COLOR)
        overlay.blit(msg, (10, 13))
        self.screen.blit(overlay, (0, 0))

    def _draw_active_event(self):
        """Draw big animated text for active disasters."""
        font = pygame.font.Font(None, 64)
        text = self.world.active_event_text
        
        # Pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() / 150)) * 0.15 + 0.85
        scaled_font = pygame.font.Font(None, int(64 * pulse))
        
        # Shadow
        shadow = scaled_font.render(text, True, (0, 0, 0))
        fg = scaled_font.render(text, True, (255, 85, 85))  # Red
        
        cx = self.viewport_width // 2
        cy = 80

        shadow_rect = shadow.get_rect(center=(cx + 3, cy + 3))
        fg_rect = fg.get_rect(center=(cx, cy))
        
        # Glow effect
        glow_surface = pygame.Surface((fg.get_width() + 40, fg.get_height() + 40), pygame.SRCALPHA)
        glow_alpha = int(100 * pulse)
        pygame.draw.rect(glow_surface, (255, 85, 85, glow_alpha), glow_surface.get_rect(), border_radius=20)
        self.screen.blit(glow_surface, (fg_rect.x - 20, fg_rect.y - 20))
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(fg, fg_rect)

    def _draw_controls_hint(self):
        """Draw helpful controls hint for new players."""
        hint_font = pygame.font.Font(None, 20)
        hints = [
            "💡 Tip: Press H for help",
            "🎮 SPACE: Pause | R: Reset",
            "🔍 Click agents to inspect",
        ]
        
        y_offset = 40
        for hint in hints:
            hint_surface = pygame.Surface((250, 25), pygame.SRCALPHA)
            hint_surface.fill((40, 42, 54, 180))
            text = hint_font.render(hint, True, UI_TEXT_COLOR)
            hint_surface.blit(text, (5, 3))
            self.screen.blit(hint_surface, (10, y_offset))
            y_offset += 30

    def _handle_zoom(self, direction):
        """Handle zoom in/out with smooth limits."""
        old_zoom = self.zoom
        self.zoom = max(0.25, min(2.5, self.zoom + direction * 0.1))
        
        # Adjust camera to zoom towards center
        if old_zoom != self.zoom:
            zoom_factor = self.zoom / old_zoom
            center_x = self.viewport_width / 2
            center_y = WINDOW_HEIGHT / 2
            
            self.target_camera_offset[0] = center_x - (center_x - self.camera_offset[0]) * zoom_factor
            self.target_camera_offset[1] = center_y - (center_y - self.camera_offset[1]) * zoom_factor
            
            # Clamp camera
            self.target_camera_offset[0] = max(-WORLD_WIDTH * self.zoom, 
                                              min(self.viewport_width, self.target_camera_offset[0]))
            self.target_camera_offset[1] = max(-WORLD_HEIGHT * self.zoom, 
                                              min(WINDOW_HEIGHT, self.target_camera_offset[1]))

    def _detect_generation_reset(self):
        """Detect when generation resets and trigger effects."""
        if self.world.episode_step == 0 and self.prev_episode_step > 0:
            self.population_graph.add_reset_mark()
            self.log_panel.push(f"🧬 Generation {self.world.generation} started")
            
            # Visual celebration
            for _ in range(30):
                x = self.viewport_width // 2
                y = WINDOW_HEIGHT // 2
                self.particle_emitter.emit_sparkle(x, y, (139, 233, 253))
            
            self.screen_effects.trigger_flash((139, 233, 253), 50, 10)
        
        self.prev_episode_step = self.world.episode_step

    def _load_save(self):
        """Load saved game state."""
        loaded = self.world.load_state(self.save_path)
        self.has_save = loaded
        if loaded:
            self.zoom = 0.6
            self.camera_offset = [0, 0]
            self.target_camera_offset = [0, 0]
            self.log_panel.push("💾 Game loaded successfully")
        return loaded


def main():
    """Main entry point for the simulation."""
    try:
        sim = EnhancedSimulation()
        sim.run()
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
