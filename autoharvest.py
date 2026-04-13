# autoharvest.py
# Continuously scans nearby farmland, BREAKS fully grown wheat (age=7),
# then replants by right-clicking on the empty farmland.
# IMPORTANT: Hold wheat seeds in your hand before running!
# Run: \autoharvest   |   Stop: \stop autoharvest

import minescript
import math
import time

# ─── CONFIG ───────────────────────────────────────────────────────────────────
SEARCH_RADIUS  = 5      # horizontal scan radius in blocks
SEARCH_DEPTH   = 4      # blocks below feet to check
SCAN_INTERVAL  = 1.0    # seconds between full re-scans when idle
LOOK_DURATION  = 0.1    # seconds to aim before acting
BREAK_HOLD     = 0.3    # how long to hold left-click to fully break wheat
CLICK_HOLD     = 0.05   # how long to hold right-click to plant
BETWEEN_BLOCKS = 0.15   # pause between each action
FARMLAND_BLOCK = "minecraft:farmland"
WHEAT_FULL     = "minecraft:wheat[age=7]"
AIR_BLOCK      = "minecraft:air"
# ──────────────────────────────────────────────────────────────────────────────


def find_all_farmland(px, py, pz):
    found = []
    ix, iy, iz = int(px), int(py), int(pz)
    for dx in range(-SEARCH_RADIUS, SEARCH_RADIUS + 1):
        for dz in range(-SEARCH_RADIUS, SEARCH_RADIUS + 1):
            for dy in range(-SEARCH_DEPTH, 2):
                bx = ix + dx
                by = iy + dy
                bz = iz + dz
                try:
                    block = minescript.getblock(bx, by, bz)
                except Exception:
                    continue
                if block and FARMLAND_BLOCK in block:
                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                    found.append(((bx, by, bz), dist))
    found.sort(key=lambda x: x[1])
    return found


def get_above(bx, by, bz):
    try:
        return minescript.getblock(bx, by + 1, bz)
    except Exception:
        return None


def look_at(px, py, pz, bx, by, bz, offset_y=1.0):
    dx = (bx + 0.5) - px
    dy = (by + offset_y) - (py + 1.62)
    dz = (bz + 0.5) - pz
    horiz = math.sqrt(dx*dx + dz*dz)
    yaw   = math.degrees(math.atan2(-dx, dz))
    pitch = math.degrees(math.atan2(-dy, horiz))
    minescript.player_set_orientation(yaw, pitch)


def aim(bx, by, bz, offset_y=1.0):
    """Aim at a block smoothly then do a final snap."""
    elapsed = 0.0
    while elapsed < LOOK_DURATION:
        px, py, pz = minescript.player_position()
        look_at(px, py, pz, bx, by, bz, offset_y)
        time.sleep(0.05)
        elapsed += 0.05
    px, py, pz = minescript.player_position()
    look_at(px, py, pz, bx, by, bz, offset_y)


def break_block():
    """Hold left-click long enough to fully break the wheat block."""
    minescript.press_key_bind("key.attack", True)
    time.sleep(BREAK_HOLD)
    minescript.press_key_bind("key.attack", False)


def right_click():
    """Short right-click to plant seeds."""
    minescript.press_key_bind("key.use", True)
    time.sleep(CLICK_HOLD)
    minescript.press_key_bind("key.use", False)


def main():
    minescript.echo(
        "§a[AutoHarvest] §fStarted! §eHold wheat seeds§f in hand. "
        "Stop with §c\\\\stop autoharvest"
    )
    time.sleep(0.8)

    total_harvested = 0
    total_planted   = 0

    while True:
        try:
            px, py, pz = minescript.player_position()
        except Exception:
            time.sleep(SCAN_INTERVAL)
            continue

        farmland = find_all_farmland(px, py, pz)

        harvest_list = []
        plant_list   = []

        for (pos, dist) in farmland:
            bx, by, bz = pos
            above = get_above(bx, by, bz)
            if above and WHEAT_FULL in above:
                harvest_list.append((pos, dist))
            elif above and AIR_BLOCK in above:
                plant_list.append((pos, dist))

        # ── Break & harvest fully grown wheat ────────────────────────────────
        for (bx, by, bz), dist in harvest_list:
            aim(bx, by + 1, bz, offset_y=0.5)   # aim at the wheat block
            break_block()                         # hold left-click to break it
            total_harvested += 1
            minescript.echo(
                f"§6[AutoHarvest] 🌾 §fBroke wheat at §b({bx}, {by+1}, {bz}) "
                f"§f[Total: §e{total_harvested}§f]"
            )
            time.sleep(BETWEEN_BLOCKS)

        # ── Plant on empty farmland ───────────────────────────────────────────
        for (bx, by, bz), dist in plant_list:
            above = get_above(bx, by, bz)
            if not (above and AIR_BLOCK in above):
                continue
            aim(bx, by, bz, offset_y=1.0)        # aim at top of farmland
            right_click()                         # right-click to plant
            total_planted += 1
            minescript.echo(
                f"§2[AutoHarvest] 🌱 §fPlanted at §b({bx}, {by}, {bz}) "
                f"§f[Total: §e{total_planted}§f]"
            )
            time.sleep(BETWEEN_BLOCKS)

        # ── Idle when nothing to do ───────────────────────────────────────────
        if not harvest_list and not plant_list:
            minescript.echo(
                f"§7[AutoHarvest] §fWaiting for wheat to grow... "
                f"Rescan in §e{SCAN_INTERVAL}s "
                f"§f(🌾§e{total_harvested} §fharvested | 🌱§e{total_planted} §fplanted)"
            )

        time.sleep(SCAN_INTERVAL)


main()