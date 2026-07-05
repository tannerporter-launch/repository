extends Node
## Autoload: tag-based asset registry (data/assets.json).

var assets: Array = []
const OPPOSITE := {"violent": "gentle", "gentle": "violent", "void": "magical",
	"sacred": "surreal", "mechanical": "innocent"}

func _ready() -> void:
	var f := FileAccess.open("res://data/assets.json", FileAccess.READ)
	assets = JSON.parse_string(f.get_as_text())

func by_tag(tag: String) -> Array:
	return assets.filter(func(a): return tag in a.tags)

func by_state(state: String) -> Array:
	return assets.filter(func(a): return state in a.states or "*" in a.states)

func contrast(tags: Array) -> Array:
	var want: Array = []
	for t in tags:
		if OPPOSITE.has(t): want.append(OPPOSITE[t])
	return assets.filter(func(a):
		for t in a.tags:
			if t in want: return true
		return false)

func reconcile(tags: Array) -> Array:
	var same := assets.filter(func(a):
		for t in a.tags:
			if t in tags: return true
		return false)
	var out := same.duplicate()
	for a in contrast(tags):
		if not out.has(a): out.append(a)
	return out
