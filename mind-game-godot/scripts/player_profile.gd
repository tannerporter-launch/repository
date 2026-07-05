extends Node
## Autoload: hidden 6-pillar profile. Fictional, gameplay-only (design constraint).

signal profile_changed

var P := {
	"aggression": 0.05, "compliance": 0.08, "curiosity": 0.08,
	"empathy": 0.06, "despair": 0.04, "creativity": 0.05
}

func bump(deltas: Dictionary) -> void:
	for k in deltas.keys():
		P[k] = clampf(P[k] + deltas[k], 0.0, 1.0)
	profile_changed.emit()

func dominant(exclude := "") -> String:
	var best := ""
	var bv := -1.0
	for k in P.keys():
		if k == exclude: continue
		if P[k] > bv: bv = P[k]; best = k
	return best

func from_delay(seconds: float) -> void:
	if seconds > 4.0: bump({"despair": 0.02})
	elif seconds < 0.8: bump({"aggression": 0.012})

func from_hover(target: String, dur: float) -> void:
	if dur > 0.45: bump({"curiosity": 0.03})
	Telemetry.log_event("hover", {"target": target, "dur": dur})

func snapshot() -> Dictionary: return P.duplicate()
