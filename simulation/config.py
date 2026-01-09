"""
Configuration settings for the predator-prey simulation.
"""

# Determinism
RANDOM_SEED = 42

# World settings (can be overridden from control panel on reset)
WORLD_WIDTH = 800
WORLD_HEIGHT = 600
GRID_SIZE = 10
OBSTACLES_ENABLED = False
OBSTACLE_COUNT = 4
OBSTACLE_RADIUS = 25
ROCK_COUNT = 35
ROCK_RESPAWN_RATE = 0.01
SHELTER_RADIUS = 30

# Episode / evolution
EPISODE_LENGTH_STEPS = 800
ARCHIVE_TOP_K = 5
MUTATION_SIGMA = 0.15
TOURNAMENT_SIZE = 3
MAX_EVENT_CASUALTY_FRACTION = 0.3  # cap per species when disasters hit

# Display settings
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 760
FPS = 60
STATS_PANEL_WIDTH = 450

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

# Species initial counts (overridable via control panel)
INITIAL_SPECIES_COUNTS = {
    'grazer': 40,
    'hunter': 18,
    'scavenger': 12,
    'protector': 10,
    'parasite': 10,
}

# DNA ranges per species (min, max) used for mutation clamping
SPECIES_DNA_RANGES = {
    'grazer': {
        'speed': (0.6, 3.8),
        'vision': (60, 200),
        'size': (3, 8),
        'energy_efficiency': (0.6, 2.2),
        'cohesion': (0.0, 1.0),
        'dispersion': (0.0, 1.0),
    },
    'hunter': {
        'speed': (1.2, 4.5),
        'vision': (80, 240),
        'size': (4, 9),
        'energy_efficiency': (0.5, 1.8),
        'attack_range': (4, 12),
    },
    'scavenger': {
        'speed': (0.8, 3.5),
        'vision': (80, 220),
        'size': (3, 7),
        'energy_efficiency': (0.8, 2.5),
        'carcass_affinity': (0.5, 2.0),
    },
    'protector': {
        'speed': (0.8, 3.5),
        'vision': (90, 220),
        'size': (4, 8),
        'energy_efficiency': (0.7, 2.0),
        'stun_radius': (20, 60),
        'stun_cooldown': (60, 240),
    },
    'parasite': {
        'speed': (1.0, 3.5),
        'vision': (80, 220),
        'size': (2, 5),
        'energy_efficiency': (0.9, 2.5),
        'drain_rate': (0.4, 2.0),
        'attach_time': (80, 200),
    },
}

# Visual identity
SPECIES_STYLE = {
    'grazer': {'color': (140, 225, 160), 'shape': 'circle'},
    'hunter': {'color': (245, 145, 145), 'shape': 'triangle'},
    'scavenger': {'color': (215, 180, 150), 'shape': 'square'},
    'protector': {'color': (160, 195, 255), 'shape': 'diamond'},
    'parasite': {'color': (220, 150, 245), 'shape': 'hex'},
}
CLAN_ACCENTS = [
    (255, 255, 255),
    (210, 235, 255),
    (255, 230, 210),
]

# Food settings
FOOD_COUNT = 90
FOOD_SIZE = 3
FOOD_ENERGY_VALUE = 30
FOOD_RESPAWN_RATE = 0.025  # Probability per frame
CARCASS_ENERGY_VALUE = 50

# Random events (per-step probability per type)
EVENT_PROBABILITIES = {
    'earthquake': 0.0008,
    'tsunami': 0.0005,
    'meteor': 0.0006,
}
EVENT_SEVERITY = {
    'earthquake': 0.8,
    'tsunami': 1.0,
    'meteor': 1.3,
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
