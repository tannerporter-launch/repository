extends Node
## Autoload: world-state registry + routing (data/world_states.json).

var states: Dictionary = {}
const NEXT := {"Obedience_Path": "Compliance_Tower", "Violence_Bloom": "Fairyland_Born_From_Violence"}

func _ready() -> void:
	var f := FileAccess.open("res://data/world_states.json", FileAccess.READ)
	states = JSON.parse_string(f.get_as_text())

func label(s: String) -> String: return states.get(s, {}).get("label", s)
func blurb(s: String) -> String: return states.get(s, {}).get("blurb", "")

func resolve_next(from_state: String) -> String:
	if NEXT.has(from_state): return NEXT[from_state]
	if from_state == "Refusal_Path":
		return "Despair_Chapel" if Profile.dominant() == "despair" else "Quiet_Void"
	return "REPORT"
