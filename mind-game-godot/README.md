# THE MIND GAME — Godot 4 Prototype (v3 port)

First-person adaptive psychological simulation. Ports the HTML v3 prototype to
Godot 4.3+ with the spec's full module architecture.

## Run it
1. Install **Godot 4.3+** (godotengine.org — standard build).
2. Godot → Import → select this folder's `project.godot` → Open.
3. Press **F5**. Desktop testing works out of the box
   (`emulate_touch_from_mouse` is on, so you can drag the virtual sticks with the mouse).

## Controls
- **Mobile:** left stick = move (inner ring = slow walk) · right stick = look ·
  contextual buttons appear per focused object · `>_` opens typed commands (time slows).
- **Desktop:** WASD + mouse-look (click to capture, Esc releases) ·
  E / Space = top contextual action · C or / = command layer · ` = debug panel.
- `/debug` typed in the command layer also toggles the dev panel.

## Test checklist (verifies the adaptive engine)
- Drink a cup → termination loop, escalating taunts; 3 drinks → Compliance_Tower.
- Refuse / try the door twice → far door unlocks → Refusal_Path → Quiet_Void or Despair_Chapel.
- Comfort the child twice, or give her a cup → Empathy_Garden.
- Pour a cup into the mirror (pick up cup, look at mirror) → Curiosity_Maze.
- Type `attack the giant's eyes` → 9-step defiance sequence → Fairyland_Born_From_Violence.
- Look away from the table/child for ~6s → objects move.
- Type nonsense ("juggle the giant") → RuleBreaker improvises, spawns anomaly, never blocks.

## Mobile export
Project → Export → Android/iOS preset. Set orientation **Landscape** in the preset.
Rendering method is already `mobile`.

## Architecture (autoloads = spec modules)
Input (sticks/keys/mouse/typed) → **InputHub** → `player.gd` + `hud.gd`
→ **Parser** (parser_rules.json) → `game_logic.gd` → **Profile** / **Telemetry**
→ **StateEngine** (world_states.json) / **RuleBreaker** → `world_mutator.gd`
(mutation_rules.json + **Registry**/assets.json) → world. **Narrative** writes the whispers.

Telemetry is local-only (`user://telemetry_session.json`). Profiling is fictional,
gameplay-behavior-only, hidden from the player except in the dev panel (spec constraints).

## Future upgrades
- **Ollama LLM improvisation:** `scripts/ollama_bridge.gd` is ready — add as autoload,
  call `OllamaBridge.improvise(action)` from RuleBreaker (falls back to rule-based).
- Replace procedural room with authored PBR scenes (Quixel/Polyhaven materials).
- Planar mirror via SubViewport reflection; wall breathing via vertex shader.
- WFC / noise zone generation for full multi-room states.
- SQLite telemetry (godot-sqlite addon) replacing the JSON file.
- Spatial audio buses: lowpass "muffle" bus effect on rule-defiance.

## Known scope cuts vs HTML v3
Audio synth, film grain, and some prop variety are stubbed — Godot buses and a
CanvasLayer shader cover these in a polish pass.
