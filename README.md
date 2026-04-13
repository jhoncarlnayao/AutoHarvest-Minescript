# 🌾 AutoHarvest
> A Minescript Python script that automatically harvests fully grown wheat and replants seeds — like a real player.

---

## 📋 Requirements

- Minecraft Java Edition
- [Minescript](https://minescript.net) mod (Fabric or Forge)
- Wheat seeds in your hand before running

---

## 🚀 Installation

1. Download `autoharvest.py`
2. Drop it into your Minescript folder:
   ```
   .minecraft/minescript/autoharvest.py
   ```
3. Hold **wheat seeds** in your hand
4. Run it in-game:
   ```
   \autoharvest
   ```
5. Stop it anytime:
   ```
   \stop autoharvest
   ```

---

## ⚙️ Configuration

Edit these values at the top of `autoharvest.py`:

| Setting | Default | Description |
|---|---|---|
| `SEARCH_RADIUS` | `5` | How many blocks in each direction to scan |
| `SEARCH_DEPTH` | `4` | How many blocks below your feet to check |
| `SCAN_INTERVAL` | `1.0` | Seconds between re-scans when idle |
| `LOOK_DURATION` | `0.1` | Seconds spent aiming before clicking |
| `BREAK_HOLD` | `0.3` | How long to hold left-click to break wheat |
| `CLICK_HOLD` | `0.05` | How long to hold right-click to plant |
| `BETWEEN_BLOCKS` | `0.15` | Pause between each block action |

---

## 🔍 How It Works

### 1. Scan
Every `SCAN_INTERVAL` seconds, the script gets your position and loops through every block in a cube around you checking for `minecraft:farmland`.

### 2. Categorize
For each farmland block found, it checks the block directly above:

| Block Above | Action |
|---|---|
| `minecraft:air` | 🌱 Right-click to **plant** seeds |
| `minecraft:wheat[age=7]` | 🌾 Left-click hold to **harvest** |
| `minecraft:wheat[age=0–6]` | ⏳ Skip — still growing |

### 3. Aim
Uses `minescript.player_set_orientation(yaw, pitch)` to rotate the camera at the exact block using trigonometry from the player's eye position.

### 4. Break (Harvest)
Holds left-click for `0.3s` — long enough for Minecraft to fully break the wheat and drop items:
```python
minescript.press_key_bind("key.attack", True)
time.sleep(BREAK_HOLD)
minescript.press_key_bind("key.attack", False)
```

### 5. Plant
Short right-click to place seeds from your hand:
```python
minescript.press_key_bind("key.use", True)
time.sleep(CLICK_HOLD)
minescript.press_key_bind("key.use", False)
```

### 6. Loop
After processing all blocks, waits `SCAN_INTERVAL` seconds and repeats forever. Runs until you type `\stop autoharvest`.

---

## 💬 Chat Messages

| Message | Meaning |
|---|---|
| `🌾 Broke wheat at (x, y, z)` | Successfully harvested a fully grown wheat block |
| `🌱 Planted at (x, y, z)` | Planted wheat seeds on empty farmland |
| `Waiting for wheat to grow...` | Nothing to do right now, will rescan soon |

---

## 🛠️ Minescript Functions Used

| Function | Purpose |
|---|---|
| `minescript.player_position()` | Get player's current X Y Z coordinates |
| `minescript.getblock(x, y, z)` | Check what block is at a coordinate |
| `minescript.player_set_orientation(yaw, pitch)` | Rotate the player's camera |
| `minescript.press_key_bind(key, state)` | Simulate pressing/releasing a key |
| `minescript.echo(message)` | Print a coloured message in chat |

---

## 💡 Tips

- Stand in the **middle** of your farm for best coverage
- Increase `SEARCH_RADIUS` if your farm is wider than 5 blocks
- If wheat isn't breaking, increase `BREAK_HOLD` to `0.4` or `0.5`
- Make sure you have **enough seeds** in hand — the script uses your held item
- Works on **singleplayer and servers** — no cheats needed since it simulates real clicks
- Stay near the farm so dropped wheat and seeds are **auto-collected** by your player

---

## 📁 Files

```
autoharvest.py   — main script
```

---

*Happy farming! 🌾*
