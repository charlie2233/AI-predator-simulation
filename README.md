# AI Predator-Prey Simulation

An advanced 2D multi-agent simulation featuring evolutionary dynamics, multiple species, and real-time visualization. Watch as predators and prey evolve through genetic algorithms, adapting their traits for survival in a dynamic ecosystem.

## Features

### 🧬 Evolution System
- **Episode-based Evolution**: Runs in fixed-length episodes/generations with end-of-episode fitness
- **Dict DNA**: Numeric genes for speed, vision, energy efficiency, size, and role-specific knobs (stun radius, drain rate, cohesion/dispersion)
- **Selection + Crossover**: Tournament selection + blended crossover each generation
- **Mutation**: Gaussian mutation per gene with tunable sigma
- **Archive Recovery**: Extinction triggers repopulation from archived top-K DNA with higher mutation

### 🦎 Multiple Species
- **Grazer (Prey)**: Eats plants; balances cohesion vs dispersion
- **Hunter (Predator)**: Chases grazers/scavengers; can be stunned by protectors
- **Scavenger**: Prefers carcasses; opportunistic hunting
- **Protector**: Escorts grazers; short-range stun/repel pulse
- **Parasite**: Attaches to hosts, drains energy, slows them down

### 🎮 Interactive Control Panel
- **Play/Pause Controls**: Start, pause, and resume simulation
- **Speed Slider**: Adjust simulation speed (0.1x to 5x)
- **Population Inputs**: Set initial pop per species, world size, episode length
- **Mutation/Food Sliders**: Tune mutation sigma and food respawn rate
- **Buttons**: Reset Generation, Reset All, Export Stats (CSV/JSON), Toggle Obstacles
- **Real-time Statistics**: Population counts, generation tracking, time steps
- **Trait & Event Feed**: Cycle trait histogram, view extinction/recovery/disaster logs

### 📊 Advanced Visualization
- **Color-coded Agents**: 
  - Brightness indicates energy levels
  - Different shapes for predators (triangles) vs prey (circles)
  - Species-specific colors
- **Population History Graph**: Track population changes over time
- **Trait Distribution Charts**: Visualize genetic evolution
- **Statistics Panel**: Real-time data display

### 🏗️ Modular Architecture
```
simulation/
├── agents/          # Base agent + shared items
│   ├── agent.py     # Base agent class with DNA + metrics
│   └── food.py      # Food / carcass items
├── species/         # Species-specific behaviors
│   ├── grazer.py    # Plant eater
│   ├── hunter.py    # Predator
│   ├── scavenger.py # Carrion-loving omnivore
│   ├── protector.py # Escort + stun
│   └── parasite.py  # Attachment + drain
├── evolution/       # Genetic algorithms
│   ├── dna.py       # Dict-based DNA container
│   └── evolution.py # Selection, reproduction, archive
├── ui/              # User interface
│   ├── components.py      # UI widgets (buttons, sliders, numeric inputs)
│   ├── control_panel.py   # Control panel + config overrides
│   └── visualization.py   # Graphs and charts
├── stats.py         # Generation logging + export
├── config.py        # Configuration settings
├── world.py         # World environment + generational evolution
└── main.py          # Main simulation loop
```

## Installation

### Requirements
- Python 3.7 or higher
- pip (Python package manager)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/charlie2233/AI-predator-simulation.git
cd AI-predator-simulation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Simulation
```bash
python run_simulation.py
```

Or directly:
```bash
python -m simulation.main
```

### Controls
- **SPACE**: Pause/Resume simulation
- **R**: Reset current generation
- **ESC**: Quit application

### UI Controls
- **Front Menu**: Start Game (new world), Continue (resume current), Credits overlay
- **Speed Slider**: Drag to adjust simulation speed
- **Population Inputs**: Set starting population per species (applies on reset)
- **World Size Inputs**: Adjust width/height (applies on reset)
- **Episode Length / Mutation σ / Food Spawn**: Tune evolution and resource pacing
- **Toggle Obstacles**: Spawn/clear simple avoidance obstacles
- **Buttons**: Start, Pause/Resume, Reset Generation, Reset All, Export Stats, Next Trait

## How It Works

### Simulation Mechanics
1. **Agents** move around the world with inherited DNA (dict of numeric genes)
2. **Grazer** seek food and balance cohesion vs dispersion
3. **Hunters** chase prey; **Protectors** can stun them; **Scavengers** prefer carcasses; **Parasites** attach and drain
4. **Energy** depletes over time with speed/size trade-offs; eating replenishes energy
5. **Episodes** run for fixed steps; fitness computed per agent based on role metrics
6. **Next Generation** is built via tournament selection, crossover, and mutation
7. **Archive Recovery** repopulates extinct species from top-K DNA with boosted mutation
8. **World Elements**: Rocks can be turned into shelters (grazers/protectors). Shelters protect from disasters.
9. **Random Events**: Earthquakes/tsunamis/meteors hit occasionally; damage is capped per species to avoid wipes. Shelters mitigate damage.
10. **Clans**: Each agent gets a clan accent color for quick grouping within a species.

### Evolution Process
1. Agents with better-suited traits survive longer
2. Successful agents reproduce more frequently
3. Traits are passed to offspring through genetic inheritance
4. Random mutations create trait variations
5. Natural selection favors advantageous traits
6. Populations adapt to environmental pressures over generations

### Generations & Evolution
- Each episode runs for `EPISODE_LENGTH_STEPS` ticks (configurable in the UI).
- At episode end, every agent receives a role-specific fitness (kills, stuns, attachments, survival time, energy gained).
- Tournament selection builds the parent pool, crossover blends DNA, mutation perturbs genes (sigma slider in UI).
- An archive keeps top-K DNA per species; extinction instantly repopulates from the archive with higher mutation.
- Stats are logged per generation and can be exported to `generation_stats.json` / `.csv` from the UI.

### Adding a New Species
1. Create a new file in `simulation/species/` inheriting from `simulation.agents.agent.Agent`.
2. Define its DNA ranges in `SPECIES_DNA_RANGES` (simulation/config.py) and add a color/shape entry in `SPECIES_STYLE`.
3. Implement `update(self, context)` behavior and a `@staticmethod fitness(agent)` function.
4. Register the class in `SPECIES_CLASS` inside `simulation/world.py` and set an initial count in `INITIAL_SPECIES_COUNTS`.

### Key Config + UI Controls
- `EPISODE_LENGTH_STEPS`, `MUTATION_SIGMA`, `FOOD_RESPAWN_RATE`, `INITIAL_SPECIES_COUNTS`, `OBSTACLES_ENABLED` in `config.py`.
- UI sliders/inputs let you override episode length, mutation sigma, food spawn rate, world size, and per-species starting populations at reset.
- Buttons: Pause/Resume, Reset Generation, Reset All, Export Stats (CSV/JSON), Trait graph cycle, Toggle obstacles.

### Configuration
Edit `simulation/config.py` to customize:
- World dimensions
- Initial populations
- Energy parameters
- Mutation rates
- Trait ranges
- Reproduction thresholds
- Visual settings

## Examples

### Typical Evolution Patterns
- **Prey** tend to evolve:
  - Higher speeds (to escape predators)
  - Better vision (to detect threats earlier)
  - Improved energy efficiency (to survive longer)

- **Predators** tend to evolve:
  - Higher speeds (to catch prey)
  - Extended vision (to locate prey)
  - Larger size (for better hunting)

### Population Dynamics
- Predator-prey populations oscillate (Lotka-Volterra dynamics)
- Food availability affects prey population
- Predator population follows prey population with a lag
- Extinction and recovery cycles are common

## Technical Details

### Dependencies
- **pygame**: Graphics and game loop
- **numpy**: Numerical computations
- **matplotlib**: Data visualization support

### Performance
- Optimized for 500+ agents simultaneously
- 60 FPS target frame rate
- Efficient collision detection
- Spatial optimization for agent interactions

## Troubleshooting

### Installation Issues
```bash
# If pygame fails to install
pip install pygame --upgrade

# For numpy issues
pip install numpy --upgrade
```

### Performance Issues
- Reduce initial population counts in `config.py`
- Lower the MAX_AGENTS setting
- Decrease simulation speed using the slider

## Contributing
Contributions are welcome! Areas for enhancement:
- Additional species types
- More genetic traits
- Advanced behavior algorithms
- Neural network integration
- Save/load simulation states
- Terrain and obstacles
- Climate/seasonal effects

## License
See LICENSE file for details.

## Author
charlie2233

## Acknowledgments
- Inspired by evolutionary algorithms and artificial life simulations
- Based on Lotka-Volterra predator-prey models
- Built with Python and Pygame
