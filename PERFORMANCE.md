# ⚡ Performance Optimization Guide

## 🎮 **GPU Note: RTX 5080 Users**

### **Important: Pygame is CPU-Based**
Unfortunately, **Pygame cannot utilize your RTX 5080 GPU** for rendering. Pygame uses software rendering (CPU-only), which means even with a powerful GPU, the simulation runs on your CPU.

**Why This Matters:**
- 🖥️ Large world rendering = more CPU work
- 🎨 Particle effects = CPU calculations
- 👥 More agents = more CPU overhead
- 📊 All drawing operations use CPU, not GPU

---

## ⚙️ **Optimizations Made**

### **Map Size** (Balanced for CPU)
- **Before**: 9600×7200 (caused slowdown)
- **Now**: 6400×4800 (2x original, optimized)
- ✅ Still much bigger, but CPU-friendly

### **Particle System**
- **Max Particles**: 2000 → **500** (4x less overhead)
- **Trail Agents**: 50 → **20** (less calculations)
- **Trail Intensity**: 0.3 → **0.2** (fewer particles)

### **Vision Range Display**
- **Agents Shown**: 20 → **10** (less circle drawing)

### **Population Scaling**
- 2x populations instead of 3x
- **Total Starting Agents**: ~220 (manageable)
- **Max Capacity**: 1800 (balanced)

### **Resource Scaling**
- **Food**: 700 (2x original)
- **Trees**: 240 (2x original)
- **Rocks**: 160 (2x original)

---

## 🚀 **Performance Tips**

### **1. In-Game Settings** (Press ⚙️ from menu)

#### **Graphics Tab - Turn OFF These:**
- ❌ **Show Agent Trails** (biggest performance hit)
- ❌ **Show Vision Ranges** (circle drawing is slow)
- 🔽 **Particle Quality** → Set to **Low** (0.5)

#### **Keep These ON (minimal impact):**
- ✅ Show Minimap (very light)
- ✅ Show FPS Counter (helps monitor)

#### **Gameplay Tab:**
- ✅ **Smooth Camera** → Turn OFF for instant response
- ✅ **Show Notifications** → Keep ON (no impact)

---

### **2. During Gameplay**

#### **Speed Settings:**
- 🎚️ **Simulation Speed**: Keep at **1.0x**
  - Going above 1.5x makes CPU work harder
  - 2x+ will cause lag with many agents

#### **Zoom Level:**
- 🔍 **Zoom Out** (scroll down) for better performance
  - Less detail to render
  - Smoother movement
  - Better overview

#### **God Mode Events:**
- ⚡ Use events **sparingly**
  - Each disaster spawns many particles
  - Can cause temporary FPS drop
  - Wait for particles to fade before next event

---

### **3. Population Management**

#### **In Control Panel:**
- 📉 **Lower Initial Populations** if still slow:
  - Grazer: 80 → 50
  - Hunter: 36 → 20
  - Scavenger: 24 → 15
  - Others: reduce by ~30%

#### **Reset Settings:**
- 🔄 Use **Reset All** to apply new population settings
- ⚙️ Adjust in "Evolution" tab before reset

---

### **4. System-Level Optimizations**

#### **Close Other Programs:**
- 🚫 Close Chrome/browsers (RAM hogs)
- 🚫 Close video editors
- 🚫 Close other games
- ✅ Run only Python + game

#### **Python Optimization:**
```bash
# Use PyPy for better performance (optional)
# PyPy JIT compiles Python for faster execution
pip install pypy
pypy3 PLAY.py
```

#### **Monitor Performance:**
- 👁️ Watch FPS counter (top left)
- 🎯 **Target**: 60 FPS
- ⚠️ **Acceptable**: 30-60 FPS
- 🔴 **Too slow**: Below 30 FPS

---

## 📊 **Performance Expectations**

### **With RTX 5080 + Good CPU:**
- **Expected FPS**: 60 (smooth)
- **Agent Count**: Up to 500 comfortably
- **Particle Effects**: Medium quality
- **Trails**: OFF recommended

### **If You Still Get Lag:**

#### **Option 1: Reduce World Size**
Edit `simulation/config.py`:
```python
WORLD_WIDTH = 4800   # Smaller world
WORLD_HEIGHT = 3600  # 1.5x original
```

#### **Option 2: Lower FPS Cap**
Edit `simulation/config.py`:
```python
FPS = 30  # Half the frame rate for better stability
```

#### **Option 3: Disable Starfield**
Comment out in `simulation/main.py` (lines ~175):
```python
# Add subtle stars/particles in background
# import random
# random.seed(42)  # Consistent stars
# for _ in range(100):
#     ... (comment out entire star drawing loop)
```

#### **Option 4: Simplify Water**
Edit `simulation/config.py`:
```python
WATER_ZONE_COUNT = 2  # Fewer water zones
```

---

## 🔬 **Benchmarking**

### **Test Your Performance:**

1. **Start New Game** with default settings
2. **Watch FPS** for 1 minute
3. **Note FPS** when population reaches 200+
4. **Trigger Meteor** event and check FPS drop

### **Acceptable Results:**
- ✅ **Idle**: 60 FPS
- ✅ **200 agents**: 45-60 FPS
- ✅ **During meteor**: Brief drop to 40 FPS, recovers

### **Need More Optimization:**
- ❌ **Idle**: Below 45 FPS
- ❌ **200 agents**: Below 30 FPS
- ❌ **During meteor**: Freezes or below 20 FPS

---

## 💡 **Why Pygame is CPU-Limited**

### **Technical Explanation:**

1. **No GPU Acceleration**:
   - Pygame uses SDL (Simple DirectMedia Layer)
   - SDL 1.2/2.0 = Software rendering
   - All pixels drawn by CPU
   - GPU just displays final frame

2. **Python Overhead**:
   - Python is interpreted (slower than C++)
   - Game logic runs in Python (CPU-bound)
   - No multi-threading for rendering
   - Single-core performance matters most

3. **What Your RTX 5080 Does**:
   - ✅ Displays the final frame (minimal work)
   - ❌ Doesn't compute particles
   - ❌ Doesn't draw shapes
   - ❌ Doesn't handle collisions
   - **GPU usage**: ~5-10% (basically idle)

---

## 🚀 **Future GPU Support?**

### **Alternative Rendering Engines:**

If you want GPU-accelerated evolution simulation:

1. **PyGame + ModernGL** (advanced)
   - Requires rewrite of rendering
   - GPU shaders for particles
   - 10-100x faster rendering

2. **Pyglet + OpenGL** (moderate effort)
   - GPU-based sprite rendering
   - Better performance

3. **Unity/Unreal** (complete rewrite)
   - Full GPU utilization
   - Professional game engine
   - Can handle 10,000+ agents

**For now**, this Pygame version is optimized as much as possible for CPU rendering.

---

## 📈 **Current Status**

### **Optimized Settings:**
✅ World: 6400×4800 (2x original)  
✅ Particles: 500 max (reduced)  
✅ Populations: 2x scale (balanced)  
✅ Trails: Limited to 20 agents  
✅ Vision: Limited to 10 agents  
✅ CPU-optimized rendering  

### **Expected Performance:**
- **Good CPU**: 60 FPS with 300+ agents
- **Average CPU**: 40-50 FPS with 200 agents
- **Older CPU**: 30-40 FPS with 150 agents

---

## 🎮 **Recommended Settings for Your RTX 5080**

Since your GPU won't help, optimize for your **CPU**:

### **Best Settings:**
```
Graphics:
- Particle Quality: Medium (1.0)
- Agent Trails: OFF
- Vision Ranges: OFF
- Minimap: ON
- FPS Counter: ON

Gameplay:
- Simulation Speed: 1.0x
- Camera Smoothing: OFF
- Auto-Pause: OFF

World:
- Use default 6400×4800
- Population: Default (220 total)
```

### **If Still Slow:**
```
Graphics:
- Particle Quality: Low (0.5)
- Everything else: OFF

World Size:
- Reduce to 4800×3600 in config.py
```

---

## 🎯 **Summary**

- 🖥️ Pygame = CPU-only (GPU doesn't help)
- ✅ World optimized to 6400×4800
- ✅ Particles reduced to 500
- ✅ Trails and vision limited
- 🎚️ Turn OFF trails for best performance
- 🔽 Set particle quality to Low if needed
- 📊 Monitor FPS (aim for 30-60)

**Your RTX 5080 is amazing, but Pygame can't use it. Focus on CPU optimization!** 🚀

---

**Need help?** Check in-game settings (⚙️) or adjust `simulation/config.py` directly.

