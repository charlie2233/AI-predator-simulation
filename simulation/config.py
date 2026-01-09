"""
Configuration settings for the predator-prey simulation.
"""

# World settings
WORLD_WIDTH = 800
WORLD_HEIGHT = 600
GRID_SIZE = 10

# Display settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 60
STATS_PANEL_WIDTH = 400

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Prey settings
PREY_INITIAL_COUNT = 50
PREY_SIZE = 4
PREY_MAX_SPEED = 3.0
PREY_MIN_SPEED = 1.0
PREY_VISION_RANGE = 80
PREY_INITIAL_ENERGY = 100
PREY_MAX_ENERGY = 150
PREY_REPRODUCTION_ENERGY = 120
PREY_REPRODUCTION_COST = 60
PREY_ENERGY_DECAY = 0.3

# Predator settings
PREDATOR_INITIAL_COUNT = 15
PREDATOR_SIZE = 6
PREDATOR_MAX_SPEED = 4.0
PREDATOR_MIN_SPEED = 1.5
PREDATOR_VISION_RANGE = 120
PREDATOR_INITIAL_ENERGY = 150
PREDATOR_MAX_ENERGY = 200
PREDATOR_REPRODUCTION_ENERGY = 180
PREDATOR_REPRODUCTION_COST = 80
PREDATOR_ENERGY_DECAY = 0.5
PREDATOR_HUNT_ENERGY_GAIN = 50

# Food settings
FOOD_COUNT = 80
FOOD_SIZE = 3
FOOD_ENERGY_VALUE = 30
FOOD_RESPAWN_RATE = 0.02  # Probability per frame

# Evolution settings
MUTATION_RATE = 0.1  # Probability of mutation per trait (0.0-1.0)
MUTATION_STRENGTH = 0.15  # Standard deviation of mutation as fraction of current value (0.0-1.0)
TRAIT_MIN_VALUES = {
    'speed': 0.5,
    'vision': 20,
    'energy_efficiency': 0.5,
    'size': 2
}
TRAIT_MAX_VALUES = {
    'speed': 8.0,
    'vision': 200,
    'energy_efficiency': 2.0,
    'size': 10
}

# Species types
SPECIES_TYPES = {
    'herbivore': {
        'color': (50, 200, 50),
        'diet': 'plants',
        'base_speed': 2.5
    },
    'carnivore': {
        'color': (200, 50, 50),
        'diet': 'meat',
        'base_speed': 3.5
    },
    'omnivore': {
        'color': (200, 200, 50),
        'diet': 'both',
        'base_speed': 3.0
    }
}

# UI settings
UI_PADDING = 10
UI_SLIDER_WIDTH = 150
UI_SLIDER_HEIGHT = 20
UI_BUTTON_WIDTH = 100
UI_BUTTON_HEIGHT = 30
UI_FONT_SIZE = 16
UI_TITLE_FONT_SIZE = 20

# Simulation settings
MAX_AGENTS = 500
