# 🧬 Evolution Sandbox - AI Ecosystem Simulator

### **Commercial-Quality Game with Professional UI/UX**

An advanced 2D multi-agent simulation featuring evolutionary dynamics, multiple species, and stunning real-time visualization. Watch as predators and prey evolve through genetic algorithms, adapting their traits for survival in a dynamic ecosystem. Now enhanced with **commercial-grade UI, particle effects, achievements, tutorials, and much more!**

![Version](https://img.shields.io/badge/version-2.0_Commercial-brightgreen)
![Python](https://img.shields.io/badge/python-3.7+-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ What's New in Commercial Edition

### 🎨 **Professional UI/UX**
- **Animated Main Menu** with smooth transitions and particle effects
- **Real-time Graphs** for population dynamics and trait evolution
- **Interactive Minimap** for quick navigation
- **Agent Inspector** with detailed DNA visualization
- **Achievement System** with 15+ unlockable achievements
- **Settings Menu** with graphics, audio, and gameplay options
- **Tutorial System** with step-by-step guides

### 🎮 **Enhanced Gameplay**
- **Particle Effects** for all major events
- **Screen Shake & Flash** effects for disasters
- **Sound Manager** (ready for audio integration)
- **Tooltips & Help System** for accessibility
- **Smooth Camera** with zoom and pan controls
- **Agent Selection** with detailed inspection
- **Manual Event Triggering** (God Mode)

### 📊 **Advanced Features**
- **Achievement Tracking** with persistent save
- **Statistics Export** to CSV/JSON
- **Save/Load System** for game states
- **Performance Optimizations** for 500+ agents
- **Configurable Settings** with live updates
- **Professional Error Handling**

---

## 🎯 Core Features

### 🧬 **Advanced Evolution System**
- **Episode-based Evolution** with fitness-based selection
- **Genetic DNA System** with 12+ inheritable traits per species
- **Tournament Selection** + blended crossover for reproduction
- **Adaptive Mutation** with configurable sigma parameter
- **Archive Recovery System** prevents total extinction
- **Real-time Trait Visualization** with histogram graphs
- **Generational Statistics** tracking and export

### 🦎 **Seven Unique Species**

| Species | Color | Role | Special Ability |
|---------|-------|------|-----------------|
| 🌿 **Grazer** | Green | Herbivore | Herd behavior, plant eating |
| 🦊 **Hunter** | Red | Predator | High-speed chasing, deadly attacks |
| 🦅 **Scavenger** | Orange | Opportunist | Carcass preference, flexible diet |
| 🛡️ **Protector** | Cyan | Defender | Stun pulse, grazer protection |
| 🦠 **Parasite** | Purple | Drainer | Energy drain, host attachment |
| 👑 **Apex** | Yellow | Top Predator | Superior stats, apex hunter |
| 🐟 **Sea Hunter** | Blue | Aquatic | Water bias, swimming advantage |

Each species evolves unique traits:
- **Speed** - Movement velocity
- **Vision** - Detection range
- **Size** - Physical dimensions
- **Energy Efficiency** - Survival endurance
- **Bravery** - Risk-taking behavior
- **Metabolism** - Energy consumption rate
- ...and many species-specific traits!

### 🎮 **Interactive Control Panel**
- ⏯️ **Play/Pause Controls** - Start, pause, and resume simulation
- 🎚️ **Speed Slider** - Adjust simulation speed (0.1x to 5x)
- 👥 **Population Config** - Set initial populations per species
- 🧬 **Evolution Settings** - Mutation rate, episode length, collapse mode
- 🌍 **World Config** - Dimensions, food spawn rate, obstacles
- 📊 **Live Statistics** - Population counts, generation tracking, time steps
- 🔄 **Action Buttons** - Reset Generation, Reset All, Export Stats
- 📈 **Trait Graphs** - Cycle through different genetic trait distributions

### 📊 **Professional Visualization**
- **Dynamic Population Graphs** 
  - Real-time line charts for all species
  - Generation reset markers
  - Food availability tracking
  - Color-coded by species

- **Trait Distribution Histograms**
  - Live genetic trait visualization
  - 15-bin resolution for accuracy
  - Species-specific color coding
  - Min/max value labels

- **Agent Rendering**
  - Energy-based brightness
  - Species-specific shapes (circles, triangles, squares, diamonds, hexagons)
  - Clan accent colors for visual variety
  - Vision range overlays (optional)
  - Movement trail particles (optional)

- **Interactive Minimap**
  - Full world overview
  - Real-time agent positions
  - Camera viewport indicator
  - Click to navigate
  - Species density visualization

- **Agent Inspector Panel**
  - Detailed DNA/gene visualization
  - Health and age statistics
  - Trait bars with color coding
  - Species-specific abilities
  - Follow mode for camera tracking

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

---

## 🚀 Installation

### **Requirements**
- Python 3.7 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended for large simulations)
- Graphics card with OpenGL support (for smooth rendering)

### **Quick Setup**

1. **Clone the repository:**
```bash
git clone https://github.com/charlie2233/AI-predator-simulation.git
cd AI-predator-simulation
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Launch the game:**
```bash
python3 PLAY.py
```

Or use the traditional launcher:
```bash
python3 run_simulation.py
```

---

## 🎮 Controls & Usage

### **Keyboard Controls**

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume simulation |
| **R** | Reset current generation |
| **H** | Toggle help menu |
| **A** | Show achievements panel |
| **ESC** | Return to menu / Close panels |
| **C** | Show credits (in menu) |
| **Arrow Keys** | Navigate tutorial (when active) |

### **Mouse Controls**

| Input | Action |
|-------|--------|
| **Left Click** | Select agent for inspection |
| **Left Click** | Place armed disaster event |
| **Scroll Wheel** | Zoom in/out |
| **Click Minimap** | Jump to location |
| **Click UI** | Interact with buttons/sliders |
| **Hover** | Show tooltips (if enabled) |

### **Main Menu Options**

- 🎮 **New Game** - Start fresh simulation with default or custom settings
- ▶️ **Continue** - Resume from last saved state
- 📚 **Tutorial** - Interactive 9-step tutorial for new players
- ⚙️ **Settings** - Configure graphics, audio, and gameplay
- 🏆 **Achievements** - View progress and unlocked achievements
- 🚪 **Quit** - Exit the game

### **Control Panel Features**

#### **World Tab**
- **Speed Slider**: 0.1x to 5x simulation speed
- **Food Spawn Rate**: Control resource availability
- **World Dimensions**: Set arena size (applies on reset)
- **God Mode Events**: Trigger earthquakes, tsunamis, or meteors
- **Toggle Obstacles**: Enable/disable environmental obstacles

#### **Evolution Tab**
- **Mutation Sigma (σ)**: Control genetic variation rate
- **Episode Steps**: Set generation length
- **Population Counts**: Configure starting populations per species
- **Trait Viewer**: Cycle through genetic trait distributions
- **Collapse Mode**: Toggle between timed and extinction-based resets

#### **Action Buttons**
- ⏯️ **Pause/Resume**: Control simulation flow
- 🔄 **Reset Generation**: Restart current episode with evolution
- 🔁 **Reset All**: Complete restart with new world
- 📊 **Export Stats**: Save data to CSV/JSON files

---

## 🏆 Achievements System

Unlock **15+ achievements** by reaching milestones and accomplishing goals:

### **Population Milestones**
- 🌱 **First Generation** - Complete your first generation
- 🎖️ **Veteran Overseer** - Reach generation 10
- 👑 **Master of Evolution** - Reach generation 50
- 📈 **Population Boom** - Have 200+ agents alive
- 🏙️ **Mega City** - Have 500+ agents alive

### **Resilience & Recovery**
- 🔥 **Phoenix Rising** - Recover a species from extinction
- 💪 **Resilient Ecosystem** - Survive 5 extinctions
- 🌊 **Disaster Survivor** - Survive your first disaster
- 💥 **Apocalypse Survivor** - Survive 10 disasters

### **Evolution Excellence**
- ⚡ **Speed Evolution** - Evolve a species with 5.0+ speed
- 👁️ **Eagle Eye** - Evolve 300+ vision range
- 🦕 **Titan** - Evolve size 12+
- ⏱️ **Marathon Runner** - Run 2000+ step generation

### **Balance & Diversity**
- 🌈 **Diverse Ecosystem** - Keep all 7 species alive simultaneously
- ⚖️ **Perfect Balance** - Maintain stable populations for 10 generations

*Achievements are automatically saved and persist between sessions!*

---

## ⚙️ Settings Menu

### **Graphics Settings**
- Show Agent Trails - Display movement particle trails
- Show Vision Ranges - Visualize detection circles
- Show Minimap - Toggle minimap visibility
- Show FPS Counter - Display performance metrics
- Particle Quality - Adjust visual effects detail (Low/Medium/High)

### **Audio Settings**
- Background Music - Toggle music on/off
- Music Volume - Adjust music level (0-100%)
- Sound Effects - Toggle SFX on/off
- SFX Volume - Adjust sound effects level (0-100%)

*Note: Sound files not included - system ready for audio integration*

### **Gameplay Settings**
- Auto-Pause on Events - Pause when disasters occur
- Show Tooltips - Display hover information
- Show Notifications - Achievement and event popups
- Smooth Camera - Enable/disable camera interpolation

---

## 📚 Tutorial System

**Interactive 9-Step Tutorial** covers:
1. Welcome & Overview
2. World Environment Basics
3. Species Roles & Behaviors
4. Evolution System Mechanics
5. Camera & Navigation Controls
6. Control Panel Functions
7. God Mode Events
8. Achievements & Goals
9. Ready to Play!

Tutorial can be accessed from main menu or skipped for experienced players.

---

## 🎨 Visual Effects

### **Particle Systems**
- ☄️ **Meteor Impact** - Fire and smoke particles
- 🌊 **Tsunami Wave** - Water splash effects
- 🌍 **Earthquake** - Dirt and debris particles
- ✨ **Sparkle Effects** - Generation transitions and achievements
- 💨 **Movement Trails** - Agent path visualization (optional)

### **Screen Effects**
- **Screen Shake** - Intensity-based camera shake for disasters
- **Flash Effects** - Color-coded flashes for major events
- **Glow Effects** - UI element highlights and selection
- **Smooth Animations** - Button hovers and menu transitions

---

## 💾 Save & Data Management

### **Auto-Save**
- Game state automatically saved to `saves/latest.json`
- Resume anytime from main menu "Continue" option
- Achievements saved separately in `saves/achievements.json`

### **Statistics Export**
Export detailed generation data:
- **CSV Format**: `generation_stats.csv` - Easy analysis in Excel/Python
- **JSON Format**: `generation_stats.json` - Programmatic access

Includes:
- Generation numbers
- Population counts per species
- Average traits per generation
- Extinction events
- Food availability trends

---

## 🎯 How It Works

### **Simulation Mechanics**
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

---

## 📊 Evolution Examples

### **Typical Evolution Patterns**

#### **Herbivores (Grazers, Scavengers)**
- ⚡ **Speed**: Increases to escape predators
- 👁️ **Vision**: Improves for early threat detection
- 🔋 **Energy Efficiency**: Optimizes for longer survival
- 🤝 **Cohesion**: Balances flocking behavior for safety

#### **Predators (Hunters, Apex, Sea Hunters)**
- ⚡ **Speed**: Increases for successful chases
- 👁️ **Vision**: Extends for prey location
- 💪 **Size**: Grows for combat advantage
- ⚔️ **Attack Power**: Strengthens for kills

#### **Support Roles (Protectors, Parasites)**
- **Protectors**: Evolve stronger stun abilities and bravery
- **Parasites**: Optimize drain rates and attachment time

### **Population Dynamics**

The ecosystem demonstrates **Lotka-Volterra dynamics**:

```
Prey Population Growth → Predator Population Growth → 
Prey Decline → Predator Decline → Cycle Repeats
```

**Observable Patterns:**
- 📈 Predator-prey populations oscillate with phase lag
- 🌿 Food availability drives herbivore populations
- 🔄 Extinction and recovery cycles are natural
- 🎯 Multiple species create complex food webs
- ⚖️ Balance emerges from chaos over many generations

### **Interesting Scenarios**

1. **Predator Arms Race**: Hunters and Grazers compete in speed evolution
2. **Parasite Pandemic**: Parasites can dominate if prey becomes too slow
3. **Protector Shield**: Successful defenders enable grazer population booms
4. **Scavenger Opportunism**: Thrive during high-conflict eras
5. **Extinction Cascades**: Removal of one species affects entire ecosystem

---

## 🎬 Getting Started Guide

### **First Time Playing?**

1. **Launch the game** using `python3 PLAY.py`
2. **Select "Tutorial"** from the main menu for guided introduction
3. **Experiment** with different settings in the control panel
4. **Watch** the population graphs to understand dynamics
5. **Try events** by arming disasters and clicking the world
6. **Inspect agents** by clicking on them to see their DNA
7. **Check achievements** to track your progress

### **Recommended Settings for Beginners**

- **Simulation Speed**: 1.0x (default)
- **Episode Length**: 800 steps
- **Mutation Sigma**: 0.15 (moderate evolution)
- **Mode**: Collapse (automatic reset on extinction)
- **Initial Populations**: Use defaults

### **Advanced Play**

- **Fast Evolution**: Increase mutation sigma to 0.3+, shorten episodes
- **Stable Ecosystems**: Lower mutation, increase episode length
- **Chaos Mode**: Trigger frequent disasters, high mutation
- **Species Focus**: Start with only 2-3 species, watch specialization

---

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

## 🔧 Troubleshooting

### **Installation Issues**

**Problem**: `pip install` fails
```bash
# Try upgrading pip first
python3 -m pip install --upgrade pip

# Install with user flag
pip install --user -r requirements.txt

# Or use pip3 explicitly
pip3 install -r requirements.txt
```

**Problem**: Pygame installation fails
```bash
# macOS
brew install pygame
pip3 install pygame

# Ubuntu/Debian
sudo apt-get install python3-pygame
pip3 install pygame

# Windows
python -m pip install pygame --upgrade
```

**Problem**: NumPy compatibility errors
```bash
pip install numpy --upgrade
# Or specify compatible version
pip install numpy==1.24.0
```

### **Performance Issues**

**Low FPS / Laggy**
- ⚙️ Open Settings → Graphics
- 🔽 Reduce Particle Quality to Low
- ❌ Disable Agent Trails
- ❌ Disable Vision Ranges
- 📉 Lower initial population counts in Control Panel
- 🐌 Reduce simulation speed if running > 2x

**Game Crashes / Freezes**
- Check system RAM usage (reduce MAX_AGENTS in config.py)
- Update graphics drivers
- Disable particle effects in settings
- Reduce world dimensions in control panel

**Slow Evolution**
- ⬆️ Increase simulation speed slider
- 🔄 Shorten episode length
- 📈 Increase mutation sigma for faster trait changes

### **Gameplay Issues**

**Can't Continue Game**
- Ensure `saves/` directory exists
- Check `saves/latest.json` is not corrupted
- Start new game if save is invalid

**Achievements Not Unlocking**
- Achievements check every 30 frames
- Some require specific conditions (check descriptions)
- Progress saved automatically when unlocked

**Events Not Triggering**
- Arm event first by clicking button in God Mode section
- Then click on world view (not UI panels)
- Check pending event banner at top of screen

**Camera Stuck/Weird**
- Press R to reset generation (resets camera)
- Adjust zoom with scroll wheel
- Click minimap to jump to specific location
- Disable camera smoothing in settings for instant movement

### **UI Issues**

**Text Too Small**
- Modify `UI_FONT_SIZE` in `simulation/config.py`
- Increase window resolution (edit `WINDOW_WIDTH/HEIGHT`)

**Panels Overlapping**
- Ensure window size is at least 1300x760
- Reduce `STATS_PANEL_WIDTH` in config if needed

**Missing UI Elements**
- Check all files in `simulation/ui/` exist
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

---

## 🎨 Customization & Modding

### **Adding New Species**

1. Create new file in `simulation/species/`
```python
from simulation.agents.agent import Agent

class YourSpecies(Agent):
    def __init__(self, x, y, dna=None, clan=0):
        super().__init__(x, y, dna, clan)
        # Custom initialization
    
    def update(self, context):
        # Custom behavior
        pass
    
    @staticmethod
    def fitness(agent):
        # Fitness calculation
        return agent.energy
```

2. Add DNA ranges in `simulation/config.py`:
```python
SPECIES_DNA_RANGES = {
    'yourspecies': {
        'speed': (1.0, 4.0),
        'vision': (80, 200),
        # ... more traits
    }
}
```

3. Add visual style:
```python
SPECIES_STYLE = {
    'yourspecies': {'color': (R, G, B), 'shape': 'circle'},
}
```

4. Register in `simulation/world.py`

### **Tweaking Parameters**

Edit `simulation/config.py`:
- `EPISODE_LENGTH_STEPS` - Generation length
- `MUTATION_SIGMA` - Evolution speed
- `FOOD_COUNT` - Resource availability
- `INITIAL_SPECIES_COUNTS` - Starting populations
- Window dimensions, colors, UI sizes, etc.

### **Creating Custom Events**

Add to `simulation/world.py`:
```python
def custom_event(self, location):
    x, y = location
    radius = 200
    # Your event logic
    self.log_event("Custom Event Triggered!")
```

---

## 🤝 Contributing

Contributions are **highly welcome**! Areas for enhancement:

### **Immediate Opportunities**
- 🎵 Add background music and sound effects
- 🧠 Neural network decision making
- 🌦️ Weather and seasonal systems
- 🗺️ Advanced terrain generation
- 📱 Mobile/web port
- 🌐 Multiplayer/shared ecosystems

### **How to Contribute**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Credits & Acknowledgments

### **Original Design & Development**
- **charlie2233** - Core simulation and evolutionary algorithms

### **Commercial Edition Enhancements**
- AI-Enhanced UI/UX Design
- Professional game systems integration
- Achievement and tutorial systems
- Particle effects and visual polish

### **Inspired By**
- 🧬 Evolutionary algorithms and artificial life research
- 📊 Lotka-Volterra predator-prey models  
- 🎮 Commercial simulation games (SimLife, Creatures, etc.)
- 🔬 Biological ecosystem studies

### **Built With**
- **Python 3** - Core language
- **Pygame** - Graphics and game loop
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization support (for exports)

### **Special Thanks**
- Evolutionary algorithm research community
- Artificial life enthusiasts
- Open source contributors

---

## 📞 Support & Community

### **Getting Help**
- 📖 Read the in-game tutorial (Tutorial button in main menu)
- ❓ Press **H** during gameplay for help
- 🐛 Report bugs via GitHub Issues
- 💬 Join discussions in GitHub Discussions

### **Share Your Results**
- 📸 Screenshot interesting evolution patterns
- 📊 Export and share statistical data
- 🏆 Show off your achievements
- 🎥 Record gameplay videos

---

## 🎉 Have Fun!

Enjoy watching evolution unfold in real-time! Experiment with different settings, trigger disasters, and see how your digital ecosystem adapts and thrives.

**Remember**: Every extinction is a learning opportunity, and every generation brings new surprises!

---

<div align="center">

**🧬 Evolution Sandbox - Where Life Evolves Before Your Eyes 🧬**

*Commercial Edition v2.0*

Made with ❤️ and 🧬

[⭐ Star this repo](https://github.com/charlie2233/AI-predator-simulation) | [🐛 Report Bug](https://github.com/charlie2233/AI-predator-simulation/issues) | [💡 Request Feature](https://github.com/charlie2233/AI-predator-simulation/issues)

</div>
