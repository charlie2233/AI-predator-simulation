# AI Predator-Prey Simulation

An advanced 2D multi-agent simulation featuring evolutionary dynamics, multiple species, and real-time visualization. Watch as predators and prey evolve through genetic algorithms, adapting their traits for survival in a dynamic ecosystem.

## Features

### 🧬 Evolution System
- **Genetic Traits**: Each agent has unique genes controlling:
  - Speed (movement velocity)
  - Vision range (perception distance)
  - Energy efficiency (metabolism)
  - Size (physical dimensions)
- **Natural Selection**: Successful agents reproduce, passing traits to offspring
- **Mutation**: Random genetic variations introduce diversity
- **Crossover**: Sexual reproduction combines parent traits

### 🦎 Multiple Species
- **Herbivores** (Green): Peaceful prey that eat plants
- **Carnivores** (Red): Aggressive predators that hunt prey
- **Omnivores** (Yellow/Purple): Flexible species with mixed strategies

### 🎮 Interactive Control Panel
- **Play/Pause Controls**: Start, pause, and resume simulation
- **Speed Slider**: Adjust simulation speed (0.1x to 5x)
- **Reset Button**: Restart with fresh population
- **Real-time Statistics**: 
  - Population counts
  - Average trait values
  - Generation tracking
  - Time steps

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
├── agents/          # Agent implementations
│   ├── agent.py     # Base agent class
│   ├── prey.py      # Prey behavior
│   ├── predator.py  # Predator behavior
│   └── food.py      # Food items
├── evolution/       # Genetic algorithms
│   └── genetics.py  # Traits and evolution tracking
├── ui/              # User interface
│   ├── components.py      # UI widgets (buttons, sliders)
│   ├── control_panel.py   # Control panel
│   └── visualization.py   # Graphs and charts
├── config.py        # Configuration settings
├── world.py         # World environment
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
- **R**: Reset simulation
- **ESC**: Quit application

### UI Controls
- **Speed Slider**: Drag to adjust simulation speed
- **Pause Button**: Click to pause/resume
- **Reset Button**: Click to reset the simulation
- **Next Trait Button**: Cycle the trait histogram between speed, vision, energy efficiency, and size

## How It Works

### Simulation Mechanics
1. **Agents** move around the world with inherited traits
2. **Prey** seek food and flee from predators
3. **Predators** hunt prey to gain energy
4. **Energy** depletes over time; agents die if energy reaches zero
5. **Reproduction** occurs when agents have sufficient energy
6. **Offspring** inherit traits from parents with mutations
7. **Energy Costs** scale with agent size and speed, rewarding efficient genetic combinations

### Evolution Process
1. Agents with better-suited traits survive longer
2. Successful agents reproduce more frequently
3. Traits are passed to offspring through genetic inheritance
4. Random mutations create trait variations
5. Natural selection favors advantageous traits
6. Populations adapt to environmental pressures over generations

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
