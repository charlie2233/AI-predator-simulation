# Usage Guide

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/charlie2233/AI-predator-simulation.git
cd AI-predator-simulation

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Simulation
```bash
# Launch with GUI (requires display)
python run_simulation.py

# Or run directly
python -m simulation.main
```

### 3. Run Headless Tests
```bash
# Test without GUI (useful for servers/CI) - runs a few generations
python test_headless.py

# Run for N generations
python test_headless.py 8
```

### 4. Generate Screenshots
```bash
# Generate a screenshot after 200 steps
python generate_screenshot.py output.png 200
```

## Controls

### Keyboard Shortcuts
- **SPACE** - Pause/Resume the simulation
- **R** - Reset current generation
- **ESC** - Quit the application

### Mouse Controls / Panel
- **Front Menu**: Start Game (new world), Continue (resume current run), Credits overlay
- **Speed**: Drag the speed slider (0.1x to 5.0x)
- **Episode Length**: Set steps per generation (applies on reset)
- **Mutation σ**: Tune mutation strength
- **Food Spawn**: Adjust food respawn probability
- **Initial Populations**: Numeric inputs per species (applies on reset)
- **World Size**: Width/height inputs (applies on reset)
- **Buttons**: Pause/Resume, Reset Generation, Reset All, Export Stats (CSV/JSON), Toggle Obstacles, Next Trait
- **Manual Events**: Arm Earthquake/Tsunami/Meteor and click on the world to trigger at that spot

## Understanding the Simulation

### Visual Elements

#### Agents
- **Grazer** - Green circles
- **Hunter** - Red triangles
- **Scavenger** - Brown squares
- **Protector** - Blue diamonds
- **Parasite** - Purple hexes
- **Light green/brown dots** - Food / carcasses
- **Gray circles/rings** - Rocks and shelters (shelters protect from disasters)
- **Clan accents** - Slight tints vary per clan within a species

#### Brightness
- Brighter colors indicate higher energy levels
- Dimmer colors indicate low energy (close to death)

### Control Panel

#### Statistics Section
- **Generation / Step** - Current generation and episode step
- **Populations** - Per-species counts
- **Food** - Current food items
- **Trait Graph** - Select trait to visualize for grazers

### Graphs

#### Population History
Shows real-time population changes for all species plus food (color-coded).

#### Events Feed
- Logs extinction recoveries, shelter builds, and random disasters (earthquake, tsunami, meteor).

#### Trait Distribution
Shows histogram of genetic trait values:
- Displays how traits are distributed across the population
- Useful for observing evolution patterns

## Configuration

### Basic Customization
Edit `simulation/config.py` to customize:

- `INITIAL_SPECIES_COUNTS` - starting populations
- `EPISODE_LENGTH_STEPS` - steps per generation
- `MUTATION_SIGMA` - mutation strength
- `FOOD_RESPAWN_RATE`, `FOOD_COUNT` - resource pacing
- `SPECIES_DNA_RANGES` - DNA limits per species
- `OBSTACLES_ENABLED`, `OBSTACLE_COUNT`, `OBSTACLE_RADIUS` - optional obstacles
- `ROCK_COUNT`, `ROCK_RESPAWN_RATE`, `SHELTER_RADIUS` - shelter resources and size
- `EVENT_PROBABILITIES`, `EVENT_SEVERITY`, `MAX_EVENT_CASUALTY_FRACTION` - disaster tuning

### Advanced Configuration
- Add/adjust species DNA ranges and colors (`SPECIES_DNA_RANGES`, `SPECIES_STYLE`).
- Tweak archive size (`ARCHIVE_TOP_K`) and selection (`TOURNAMENT_SIZE`) in `config.py`.

## Observing Evolution

### What to Look For

1. **Speed Evolution**
   - Prey tend to get faster to escape predators
   - Predators get faster to catch prey
   - Arms race between predator and prey speed

2. **Vision Evolution**
   - Prey develop better vision to detect predators early
   - Predators develop better vision to find prey

3. **Energy Efficiency**
   - Agents that use energy efficiently survive longer
   - Especially important during food scarcity

4. **Population Cycles**
   - Classic predator-prey oscillations (Lotka-Volterra)
   - Predator population follows prey with a delay
   - Both populations can go extinct if not balanced

### Tips for Interesting Results

1. **Start with unbalanced populations**
   - Try 100 prey and 5 predators
   - Observe how evolution stabilizes the system

2. **Increase mutation rate**
   - Set `MUTATION_RATE = 0.3` for faster evolution
   - More dramatic trait changes

3. **Limit food supply**
   - Reduce `FOOD_COUNT = 30`
   - Creates more competitive environment
   - Stronger selection pressure

4. **Adjust simulation speed**
   - Use the speed slider for real-time control
   - Speed up to see long-term trends
   - Slow down to observe individual behaviors

## Troubleshooting

### Simulation is too slow
- Reduce `MAX_AGENTS` in config.py
- Lower initial population counts
- Reduce `FPS` setting

### Populations go extinct quickly
- Increase initial prey count
- Decrease initial predator count
- Increase `FOOD_COUNT`
- Increase `FOOD_RESPAWN_RATE`

### No evolution visible
- Run for longer (1000+ steps)
- Increase `MUTATION_RATE`
- Increase `MUTATION_STRENGTH`

### Display issues (pygame errors)
- Run headless test instead: `python test_headless.py`
- Use screenshot generator: `python generate_screenshot.py`
- Check pygame installation: `pip install pygame --upgrade`

## Examples

### Example 1: Fast Evolution
```python
# In simulation/config.py
MUTATION_RATE = 0.25
MUTATION_STRENGTH = 0.20
FOOD_COUNT = 40  # Scarce resources
```

### Example 2: Large Population
```python
PREY_INITIAL_COUNT = 150
PREDATOR_INITIAL_COUNT = 30
FOOD_COUNT = 200
MAX_AGENTS = 800
```

### Example 3: Predator-Heavy
```python
PREY_INITIAL_COUNT = 30
PREDATOR_INITIAL_COUNT = 30
PREDATOR_ENERGY_DECAY = 0.3  # Less energy drain
```

## Advanced Features

### Custom Species
You can modify species behaviors in:
- `simulation/agents/prey.py` - Prey behavior
- `simulation/agents/predator.py` - Predator behavior

### New Traits
Add new genetic traits in:
- `simulation/evolution/genetics.py` - Add to GeneticTraits class

### Additional Visualizations
Create new graphs in:
- `simulation/ui/visualization.py` - Add new graph types

## Getting Help

### Common Questions

**Q: Why do all agents die?**
A: This is natural! Try adjusting reproduction thresholds or food availability.

**Q: How long should I run the simulation?**
A: At least 1000 steps to see meaningful evolution (5-10 minutes at normal speed).

**Q: Can I save/load simulations?**
A: Not currently implemented, but could be added as a feature.

**Q: How do I make predators smarter?**
A: Edit `simulation/agents/predator.py` to add more sophisticated hunting algorithms.

### Further Reading
- See README.md for architecture details
- Check simulation/config.py for all available settings
- Explore the source code - it's well-documented!

## Performance Tips

1. **For smooth 60 FPS:**
   - Keep total agents under 200
   - Reduce vision ranges
   - Lower FPS to 30 if needed

2. **For long simulations:**
   - Use headless mode
   - Disable graphs temporarily
   - Increase simulation speed

3. **For detailed observation:**
   - Pause frequently
   - Use speed slider at 0.1x-0.5x
   - Reduce population for easier tracking

## Contributing

Ideas for enhancements:
- Neural network-based agent AI
- Terrain/obstacle systems
- Day/night cycles
- Multiple food types
- Cooperative behaviors
- Save/load functionality

Feel free to fork and experiment!
