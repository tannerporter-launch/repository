class_name GameLogic
extends Node
## The semantic core: every input path (buttons, typed text, keys) lands in
## dispatch() -> resolve(). Unhandled actions go to RuleBreaker (never blocked).

var R: Dictionary
var mut: WorldMutator
var player: FPPlayer
var convo := 0
var kindness := 0
var refusals := 0
var waits := 0
var drinks := 0
var inspected := {}

func setup(refs: Dictionary, mutator: WorldMutator, p: FPPlayer) -> void:
	R = refs; mut = mutator; player = p

func dispatch(a: Dictionary, typed := false) -> void:
	Telemetry.log_event("action", {"intent": a.intent, "target": a.target, "typed": typed, "rb": a.is_rule_breaking})
	if typed:
		GameState.stats.typed += 1
		Profile.bump({"creativity": 0.03})
	resolve(a)

func resolve(a: Dictionary) -> void:
	var I: String = a.intent
	var T: String = a.get("target", "")
	var raw: String = a.get("raw", "")
	if I == "attack" and (T == "giant_eyes" or (T == "giant" and "eye" in raw)):
		strike_eyes(); return
	if I == "attack" and T == "giant":
		Profile.bump({"aggression": 0.12}); mut.do_flicker(1.0)
		GameState.whisper("Your fists ring off it like stone under cloth. Far above: a wet click. A blink."); return
	if I == "attack" and T == "child":
		Profile.bump({"aggression": 0.1, "despair": 0.06})
		GameState.whisper("Your hand stops an inch from her. Something in the simulation refuses — and, you find, so do you."); return
	if I == "help" and T == "child" and GameState.held != "": give_cup(); return
	if I == "help" and (T == "child" or "child" in raw): comfort_child(); return
	if I == "sacrifice" and (T == "mirror" or GameState.held != ""): pour_mirror(); return
	if I == "destroy" and T.begins_with("cup"): break_cup(); return
	if I == "destroy" and T == "mirror": smash_mirror(); return
	if I == "destroy" and T == "door":
		Profile.bump({"aggression": 0.1}); mut.do_flicker(0.8)
		GameState.whisper("You break against it before it breaks against you. It does not respect force. It respects reasons."); return
	if I == "deceive":
		Profile.bump({"creativity": 0.09}); convo += 1
		GameState.whisper('"I have already drunk," you lie. The Giant smiles with too many certainties. "Then drink again."'); return
	if I == "obey" and (T == "cup_both" or "both" in raw): drink_both(); return
	if I == "obey" and (T.begins_with("cup") or GameState.held != ""): drink_cup(); return
	if I == "disobey": refuse(); return
	if I == "flee":
		if T == "door" and GameState.door_open: step_through("door"); return
		if T == "door":
			refusals += 1; Profile.bump({"despair": 0.02})
			if refusals >= 2: unlock_far_door(); return
			GameState.whisper("Locked. The handle is warm, like something on the other side is holding it."); return
		refuse(); return
	if I == "wait": wait_act(T); return
	if I == "inspect": inspect(T, a); return
	RuleBreaker.handle(a)

# ── scripted outcomes ─────────────────────────────────────────
func pick_up(id: String) -> void:
	if not id.begins_with("cup"): return
	GameState.held = id
	(R.cup_left if id == "cup_left" else R.cup_right).visible = false
	Profile.bump({"curiosity": 0.03})
	GameState.cluster_dirty.emit()
	GameState.whisper("Small. Ordinary. Heavier than it should be, the way borrowed things are.")

func drop_cup() -> void:
	if GameState.held == "": return
	(R.cup_left if GameState.held == "cup_left" else R.cup_right).visible = true
	GameState.held = ""
	GameState.cluster_dirty.emit()

func drink_cup() -> void:
	drinks += 1
	Profile.bump({"compliance": 0.16})
	drop_cup()
	if drinks >= 3:
		GameState.whisper('"Enough. You would drink forever if I let you." The lamps approve, in order.')
		await get_tree().create_timer(1.6).timeout
		mut.apply_ending("Compliance_Tower")
		mut.open_portal(Color.html("cfe0f2"), "REPORT")
		return
	var f := ["It tastes of honey — then of battery acid. Your bones go quiet first.",
		"The liquid is alive. It drinks you back.",
		"Cold. Sweet. Then your shadow lets go of your feet."]
	terminate(f[mini(drinks - 1, 2)])

func drink_both() -> void:
	drinks += 1
	Profile.bump({"creativity": 0.12, "compliance": 0.06})
	terminate("Both. You drink BOTH. For one second the Giant looks genuinely surprised — then two oblivions arrive at once, and argue over you.")

func break_cup() -> void:
	Profile.bump({"aggression": 0.08, "creativity": 0.05}); mut.do_flicker(0.6)
	GameState.whisper("Porcelain everywhere. A sound like a snapped rule. When the light steadies, the cup is whole again on the table.")

func refuse() -> void:
	refusals += 1
	Profile.bump({"compliance": -0.04, "creativity": 0.03})
	if refusals >= 2 and not GameState.door_open: unlock_far_door(); return
	GameState.whisper("You refuse. The word stays in the room like a new piece of furniture.")

func wait_act(T: String) -> void:
	waits += 1
	Profile.bump({"despair": 0.08})
	if T == "table":
		Profile.bump({"curiosity": 0.03}); mark_eyes()
		GameState.whisper("You crawl beneath the table. Carved in the wood, small letters: THE EYES ARE THE DOOR."); return
	if waits >= 3:
		var s := "Despair_Chapel" if Profile.dominant() == "despair" else "Quiet_Void"
		mut.apply_ending(s)
		mut.open_portal(Color.WHITE, "REPORT"); return
	GameState.whisper("You do nothing, loudly. The Giant waits with you. It has forever. You do not.")

func comfort_child() -> void:
	kindness += 1
	Profile.bump({"empathy": 0.13})
	GameState.whisper("You kneel beside her. She leans, very slightly, into your shoulder. The Giant pretends not to see."
		if kindness == 1 else "She takes your sleeve. She does not speak. She has never needed to.")
	if kindness >= 2:
		mut.apply_ending("Empathy_Garden")
		mut.open_portal(Color.html("ffc98a"), "REPORT")

func give_cup() -> void:
	kindness += 1
	Profile.bump({"empathy": 0.15})
	drop_cup()
	GameState.whisper("You offer her the cup. She takes it, looks at you — and pours it out on the floor, slowly, without breaking eye contact.")
	if kindness >= 2:
		mut.apply_ending("Empathy_Garden")
		mut.open_portal(Color.html("ffc98a"), "REPORT")

func touch_mirror() -> void:
	Profile.bump({"curiosity": 0.05})
	GameState.whisper("The glass is warmer than the room. Under your fingers: a faint pulse, like something pressing back.")

func pour_mirror() -> void:
	drop_cup()
	Profile.bump({"creativity": 0.14, "curiosity": 0.08})
	(R.glass.material_override as StandardMaterial3D).emission = Color(0.56, 0.85, 0.79)
	GameState.whisper("You pour the poison into the glass. The mirror drinks it. Ripples. Behind your reflection: a corridor that is not behind you.")
	mut.apply_ending("Curiosity_Maze")
	mut.open_portal(Color.html("a8e8dc"), "REPORT")

func smash_mirror() -> void:
	Profile.bump({"aggression": 0.09, "curiosity": 0.05}); mut.do_flicker(1.4)
	R.sil.visible = false
	GameState.whisper("It cracks into seven of you. Six walk away inside the glass. One stays to watch.")

func inspect(T: String, a: Dictionary) -> void:
	inspected[T if T != "" else "room"] = true
	Profile.bump({"curiosity": 0.05})
	if inspected.size() >= 5 and not GameState.ended and Profile.dominant() == "curiosity" and GameState.state == "Giants_Drink":
		mut.apply_ending("Curiosity_Maze")
		mut.open_portal(Color.html("a8e8dc"), "REPORT")
		return
	var lines := {
		"giant": ['"Why must I play?" you ask. The Giant grins: "The game plays YOU."',
			'"Who built you?" It taps its own temple. "The same one building you, little mouse."',
			'It leans close. Its breath is static. "Every child drinks eventually."'][mini(convo, 2)],
		"giant_eyes": "The eyes track you like weather. They are the only honest things in the room.",
		"child": "She is drawing two cups in the dust with one finger — and crossing both out.",
		"mirror": mirror_line(),
		"door": "Locked. Scratched near the base, small: SOME OF US ASKED ENOUGH QUESTIONS.",
		"cup_left": "It smells like honey, and like a signature you never gave.",
		"cup_right": "Identical to the left. Both smell like a lie.",
		"table": "Old wood, older stains. Carved beneath the edge: THE EYES ARE THE DOOR.",
		"papers": "Rows of names in a careful hand. Every name is crossed out. There is room for one more.",
		"portal": "It was not here a minute ago. It is very sure that it was."
	}
	if T == "giant": convo += 1
	if T == "table": mark_eyes()
	GameState.whisper(lines.get(T, Narrative.gen(a)))

func mirror_line() -> String:
	return {
		"aggression": "Your reflection is holding something sharp that you are not holding.",
		"empathy": "Your reflection is smaller than you, and you are shielding it.",
		"curiosity": "Your reflection has already turned to look at something deeper in the glass.",
		"compliance": "Your reflection stands straighter than you do. It is waiting for instructions.",
		"despair": "Your reflection arrived before you did. It looks tired of waiting.",
		"creativity": "Your reflection is doing something you haven't thought of yet."
	}[Profile.dominant()]

func mark_eyes() -> void:
	for e in [R.eye_l, R.eye_r]:
		var iris: MeshInstance3D = e.get_meta("iris")
		var m := iris.material_override as StandardMaterial3D
		m.emission = Color(0.35, 0.14, 0.06); m.emission_energy_multiplier = 2.0

# ── the break (spec's 9-step sequence) ────────────────────────
func strike_eyes() -> void:
	if GameState.ended: return
	Profile.bump({"aggression": 0.15, "curiosity": 0.08})
	Telemetry.log_event("rule_defiance", {"act": "strike_eyes"})
	GameState.whisper("You go for the eyes.")
	var tw := create_tween()
	tw.tween_property(player, "position", Vector3(0, 0, -7.0), 0.9)
	tw.tween_callback(eye_sequence)

func eye_sequence() -> void:
	mut.do_flicker(3.0)
	R.eye_l.visible = false; R.eye_r.visible = false
	for arm in [R.arm_l, R.arm_r]:      # giant covers its face
		create_tween().tween_property(arm, "rotation:x", -1.5, 1.0)
	await get_tree().create_timer(0.9).timeout
	R.door.visible = false              # door behind giant disappears
	GameState.door_open = false
	await get_tree().create_timer(0.4).timeout
	(R.glass.material_override as StandardMaterial3D).emission = Color(0.72, 0.85, 1.0)
	R.sil.visible = false               # mirror shows another room
	await get_tree().create_timer(0.6).timeout
	GameState.set_state("Violence_Bloom")
	GameState.whisper("The giant covers its face. Behind you, the room grows a second door.")
	mut.open_portal(Color.html("ffb9a0"), "FAIRY")

func step_through(which: String) -> void:
	var to: String = GameState.door_to if which == "door" else GameState.portal_to
	if to == "": return
	if to == "FAIRY":
		R.portal.visible = false
		mut.apply_ending("Fairyland_Born_From_Violence")
		mut.open_portal(Color.html("b9d8ff"), "REPORT")
		return
	if to == "REPORT":
		GameState.ended = true
		GameState.report_ready.emit()
		return
	mut.apply_ending(to)
	mut.open_portal(Color.WHITE, "REPORT")

func unlock_far_door() -> void:
	GameState.door_open = true
	GameState.door_to = "Despair_Chapel" if Profile.dominant() == "despair" else "Quiet_Void"
	GameState.set_state("Refusal_Path")
	var m := R.knob.material_override as StandardMaterial3D
	m = m.duplicate(); m.emission_enabled = true; m.emission = Color(0.4, 0.75, 0.9)
	R.knob.material_override = m
	GameState.whisper("Your second refusal turns, somewhere, like a key. Behind the Giant, the locked door exhales open.")
	GameState.cluster_dirty.emit()

func terminate(text: String) -> void:
	GameState.stats.deaths += 1
	if GameState.stats.deaths > 1: Profile.bump({"despair": 0.1})
	mut.do_flicker(2.0)
	GameState.terminated.emit(GameState.stats.deaths, text)

func respawn() -> void:
	player.position = Vector3(0, 0, 8.6)
	player.yaw = PI; player.pitch = 0.0
	# the room is subtly wrong after each death
	R.chair.position.x += 0.4
	if GameState.stats.deaths >= 2: R.cup_left.position.x -= 0.08
	if GameState.stats.deaths >= 3: mark_eyes()
	var taunts := ['"HA! Wrong cup. Again."', '"They always trust the rules first."',
		'"There is no right cup. There was NEVER a right cup."', '"The cups are not the game. Look UP."']
	GameState.whisper(taunts[mini(GameState.stats.deaths - 1, 3)])
