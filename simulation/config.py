"""
Configuration settings for the predator-prey simulation.
"""

# Determinism
RANDOM_SEED = 42

# World settings (optimized for performance - 2x bigger, GPU-friendly)
WORLD_WIDTH = 6400   # Big map but optimized for CPU rendering
WORLD_HEIGHT = 4800  # 2x original size - better performance
GRID_SIZE = 10
OBSTACLES_ENABLED = False
OBSTACLE_COUNT = 8   # Moderate obstacles
OBSTACLE_RADIUS = 25
ROCK_COUNT = 160     # 2x rocks (less draw calls)
ROCK_RESPAWN_RATE = 0.01
SHELTER_RADIUS = 30
WATER_ZONE_COUNT = 4          # Balanced water zones
WATER_ZONE_WIDTH = 320        # Moderate width
WATER_ZONE_HEIGHT = WORLD_HEIGHT
WATER_BLOOM_RATE = 0.10       # Balanced spawn rate
DISASTER_RADIUS = 400         # Scaled disaster radius
SEA_COLOR = (25, 70, 140)
RIVER_COLOR = (20, 100, 70)

# Episode / evolution
EPISODE_LENGTH_STEPS = 800
ARCHIVE_TOP_K = 5
MUTATION_SIGMA = 0.15
TOURNAMENT_SIZE = 3
MAX_EVENT_CASUALTY_FRACTION = 0.3  # cap per species when disasters hit
REPRODUCTION_BOOST = 1.2           # multiplier for next-gen child counts
COLLAPSE_RESET_ONLY = True         # if True, end generation only on collapse/extinction (not on step timer)
COLLAPSE_AGENT_FRACTION = 0.12     # collapse threshold vs initial agent count
COLLAPSE_MIN_AGENTS = 24           # hard floor for collapse threshold (2x for bigger map)
COLLAPSE_GRACE_STEPS = 90          # avoid instant resets at generation start

# Display settings (optimized for performance)
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 760
FPS = 60  # Can lower to 30 if still slow
STATS_PANEL_WIDTH = 450

# Colors (Dracula / Pastel Theme)
BLACK = (0, 0, 0)
WHITE = (248, 248, 242)  # Off-white
GREEN = (80, 250, 123)
RED = (255, 85, 85)
BLUE = (98, 114, 164)
YELLOW = (241, 250, 140)
GRAY = (68, 71, 90)
DARK_GRAY = (40, 42, 54)  # Background
LIGHT_GRAY = (98, 114, 164) # Comments/Selection
CYAN = (139, 233, 253)
PINK = (255, 121, 198)
PURPLE = (189, 147, 249)
ORANGE = (255, 184, 108)

# UI Theme
UI_BG_COLOR = (40, 42, 54)       # Dark background
UI_PANEL_BG = (68, 71, 90)       # Panel background
UI_TEXT_COLOR = (248, 248, 242)
UI_ACCENT_COLOR = (189, 147, 249) # Purple accent
UI_HOVER_COLOR = (255, 121, 198)  # Pink hover
UI_BORDER_COLOR = (98, 114, 164)

# Species initial counts (optimized 2x for performance)
INITIAL_SPECIES_COUNTS = {
    'grazer': 80,       # 2x - better performance
    'hunter': 36,       # 2x predators
    'scavenger': 24,    # 2x scavengers
    'protector': 20,    # 2x protectors
    'parasite': 20,     # 2x parasites
    'apex': 12,         # 2x apex predators
    'sea_hunter': 28,   # 2x sea hunters
}

# DNA ranges per species (min, max) used for mutation clamping
SPECIES_DNA_RANGES = {
    'grazer': {
        'speed': (0.6, 3.6),
        'vision': (70, 220),
        'size': (5, 11),
        'energy_efficiency': (0.6, 2.2),
        'cohesion': (0.0, 1.0),
        'dispersion': (0.0, 1.0),
        'carry_capacity': (8, 18),
        'bravery': (0.1, 0.9),
        'metabolism': (0.5, 1.5),
        'swim_factor': (0.2, 0.6),
        'rock_skill': (0.8, 1.2),
        'reproduction_factor': (0.9, 1.3),
    },
    'hunter': {
        'speed': (1.2, 4.3),
        'vision': (90, 250),
        'size': (6, 11),
        'energy_efficiency': (0.5, 1.8),
        'attack_range': (5, 13),
        'attack_power': (30, 55),
        'carry_capacity': (10, 20),
        'bravery': (0.3, 1.0),
        'metabolism': (0.6, 1.6),
        'swim_factor': (0.2, 0.6),
        'rock_skill': (0.9, 1.3),
        'reproduction_factor': (0.8, 1.2),
    },
    'scavenger': {
        'speed': (0.8, 3.3),
        'vision': (90, 230),
        'size': (5, 10),
        'energy_efficiency': (0.8, 2.5),
        'carcass_affinity': (0.5, 2.0),
        'carry_capacity': (8, 16),
        'bravery': (0.1, 0.7),
        'metabolism': (0.4, 1.4),
        'swim_factor': (0.2, 0.7),
        'rock_skill': (0.8, 1.1),
        'reproduction_factor': (0.9, 1.2),
    },
    'protector': {
        'speed': (0.8, 3.3),
        'vision': (100, 240),
        'size': (6, 10),
        'energy_efficiency': (0.7, 2.0),
        'stun_radius': (26, 70),
        'stun_cooldown': (60, 240),
        'carry_capacity': (12, 22),
        'bravery': (0.5, 1.0),
        'metabolism': (0.5, 1.5),
        'swim_factor': (0.2, 0.6),
        'rock_skill': (1.0, 1.4),
        'reproduction_factor': (0.8, 1.1),
    },
    'parasite': {
        'speed': (1.0, 3.3),
        'vision': (90, 230),
        'size': (4, 8),
        'energy_efficiency': (0.9, 2.5),
        'drain_rate': (0.4, 2.0),
        'attach_time': (80, 200),
        'carry_capacity': (6, 14),
        'bravery': (0.0, 0.6),
        'metabolism': (0.3, 1.2),
        'swim_factor': (0.3, 0.8),
        'rock_skill': (0.6, 1.0),
        'reproduction_factor': (0.9, 1.25),
    },
    'apex': {
        'speed': (1.5, 4.8),
        'vision': (110, 280),
        'size': (7, 12),
        'energy_efficiency': (0.5, 1.6),
        'attack_range': (6, 14),
        'attack_power': (45, 75),
        'carry_capacity': (12, 24),
        'bravery': (0.7, 1.0),
        'metabolism': (0.7, 1.7),
        'swim_factor': (0.2, 0.5),
        'rock_skill': (1.2, 1.6),
        'reproduction_factor': (0.7, 1.1),
    },
    'sea_hunter': {
        'speed': (1.0, 3.6),
        'vision': (100, 260),
        'size': (6, 11),
        'energy_efficiency': (0.7, 2.0),
        'attack_power': (28, 50),
        'carry_capacity': (10, 18),
        'water_bias': (0.6, 1.0),
        'bravery': (0.4, 0.9),
        'metabolism': (0.6, 1.5),
        'swim_factor': (0.8, 1.4),
        'rock_skill': (0.9, 1.2),
        'reproduction_factor': (0.8, 1.2),
    },
}

# Visual identity
SPECIES_STYLE = {
    'grazer': {'color': (80, 250, 123), 'shape': 'circle'},      # Green
    'hunter': {'color': (255, 85, 85), 'shape': 'triangle'},     # Red
    'scavenger': {'color': (255, 184, 108), 'shape': 'square'},  # Orange
    'protector': {'color': (139, 233, 253), 'shape': 'diamond'}, # Cyan
    'parasite': {'color': (189, 147, 249), 'shape': 'hex'},      # Purple
    'apex': {'color': (255, 255, 140), 'shape': 'triangle'},     # Yellow apex
    'sea_hunter': {'color': (120, 200, 255), 'shape': 'circle'}, # Blue sea clan
}
CLAN_ACCENTS = [
    (255, 255, 255),
    (210, 235, 255),
    (255, 230, 210),
    (200, 255, 220),
    (255, 220, 255),
    (220, 255, 255),
]
CLAN_TRAITS = [
    {"speed": 1.0, "vision": 1.0, "energy_efficiency": 1.0},        # neutral
    {"speed": 1.1, "vision": 0.95, "energy_efficiency": 0.95},      # swift
    {"speed": 0.95, "vision": 1.1, "energy_efficiency": 1.05},      # sentry
    {"speed": 1.0, "vision": 1.0, "energy_efficiency": 1.1},        # efficient
    {"speed": 1.05, "vision": 1.05, "energy_efficiency": 0.9},      # aggressive
]

# Food settings (optimized for performance - 2x scale)
FOOD_COUNT = 700       # 2x food - balanced for performance
FOOD_SIZE = 6
FOOD_ENERGY_VALUE = 35
FOOD_RESPAWN_RATE = 0.03  # Probability per frame
CARCASS_ENERGY_VALUE = 55
FOOD_COLOR = (139, 233, 145)   # Soft Green
CARCASS_COLOR = (255, 184, 108) # Soft Orange/Brown
FOOD_SIZE_RANGE = (4, 9)
FOOD_ENERGY_RANGE = (20, 45)
TREE_COUNT = 240       # 2x trees - less rendering overhead
TREE_SIZE_RANGE = (10, 18)
TREE_ENERGY_VALUE = 80

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
UI_SLIDER_WIDTH = 170
UI_SLIDER_HEIGHT = 26
UI_BUTTON_WIDTH = 120
UI_BUTTON_HEIGHT = 36
UI_FONT_SIZE = 18
UI_TITLE_FONT_SIZE = 24

# Simulation settings (optimized for CPU performance)
MAX_AGENTS = 1800  # 2x capacity - better performance on CPU
