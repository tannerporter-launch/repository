extends Node
## Autoload: raw text -> {intent, target, confidence, is_rule_breaking, raw}.
## Data-driven from res://data/parser_rules.json (keyword + synonym matching).

var rules: Dictionary = {}

func _ready() -> void:
	rules = _load_json("res://data/parser_rules.json")

static func _load_json(path: String) -> Variant:
	var f := FileAccess.open(path, FileAccess.READ)
	return JSON.parse_string(f.get_as_text()) if f else {}

func parse(raw: String) -> Dictionary:
	var s := " " + raw.to_lower().strip_edges() + " "
	var target := ""
	for id in rules.targets.keys():
		for syn in rules.targets[id]:
			if s.contains(syn):
				target = id
				break
		if target != "": break
	var intent := "unknown"
	var best := 0.0
	for intent_name in rules.intents.keys():
		var def: Dictionary = rules.intents[intent_name]
		for kw in def.kw:
			if s.contains(kw) and def.w > best:
				best = def.w
				intent = intent_name
	var conf: float = (0.2 if intent == "unknown" else best) + (0.22 if target != "" else 0.0)
	return {
		"intent": intent, "target": target,
		"confidence": snappedf(minf(conf, 0.97), 0.01),
		"is_rule_breaking": is_rule_breaking(intent, target),
		"raw": raw.strip_edges()
	}

func is_rule_breaking(intent: String, target: String) -> bool:
	if GameState.state != "Giants_Drink":
		return intent in ["attack", "destroy", "deceive", "sacrifice"]
	var ex: Dictionary = rules.expected_in_giants_drink
	if intent == "obey" and target in ex.obey_targets_ok: return false
	return not (intent in ex.intents_ok)
