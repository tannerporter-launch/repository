extends Node
## Autoload: unscripted actions never fail — they mutate the world (spec §5).

signal mutation_requested(mutations: Array)

func handle(action: Dictionary) -> Dictionary:
	GameState.stats.unscripted += 1
	var d := Profile.dominant()
	var updates := {"creativity": 0.08, d: 0.04}
	Profile.bump(updates)
	var tags: Array = ["surreal"]
	var pool := Registry.reconcile(tags)
	var asset: Dictionary = pool[randi() % pool.size()] if pool.size() > 0 else {"id": "anomaly_cube"}
	var muts := ["spawn:" + str(asset.id), "flicker", "muffle"]
	mutation_requested.emit(muts)
	var result := {
		"new_world_state": GameState.state,
		"narrative_response": Narrative.gen(action),
		"world_mutations": muts,
		"profile_updates": updates
	}
	GameState.sys("UNSCRIPTED ACTION — RECONCILING")
	GameState.whisper(result.narrative_response)
	Telemetry.log_event("rule_break", {"intent": action.get("intent", "?")})
	return result
