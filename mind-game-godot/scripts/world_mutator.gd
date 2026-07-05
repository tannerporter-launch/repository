class_name WorldMutator
extends Node
## Continuous trait-driven mutation + ending transformations (data/mutation_rules.json).
## The world changes; the player is never told why (spec: don't over-explain).

var R: Dictionary          # room refs
var env: Environment
var lamp: OmniLight3D
var rules: Dictionary
var half_w := RoomBuilder.ROOM.x / 2
var t := 0.0
var flick := 0.0
var unobs_child := 0.0
var unobs_cups := 0.0
var stare := 0.0
var player: FPPlayer
var anomaly: MeshInstance3D

func setup(refs: Dictionary, environment: Environment, main_lamp: OmniLight3D, p: FPPlayer) -> void:
	R = refs; env = environment; lamp = main_lamp; player = p
	var f := FileAccess.open("res://data/mutation_rules.json", FileAccess.READ)
	rules = JSON.parse_string(f.get_as_text())
	RuleBreaker.mutation_requested.connect(_on_mutations)

func _process(dt: float) -> void:
	if GameState.stats.t0 == 0: return
	t += dt
	var P: Dictionary = Profile.P
	if not GameState.ended and GameState.state == "Giants_Drink":
		# lighting temperament
		var warm := Color(1.0, 0.85, 0.65)
		var target := warm.lerp(Color(1.0, 0.56, 0.44), P.aggression * 0.8)
		target = target.lerp(Color(0.86, 0.91, 0.96), P.compliance * 0.5)
		lamp.light_color = lamp.light_color.lerp(target, dt * 0.6)
		lamp.light_energy = lerpf(lamp.light_energy, 2.2 * (1.0 - P.despair * 0.45), dt)
		env.fog_density = lerpf(env.fog_density, 0.03 + P.despair * 0.05, dt * 0.5)
		# aggression narrows the room
		half_w = lerpf(half_w, RoomBuilder.ROOM.x / 2 - P.aggression * 0.55, dt * 0.4)
		R.wall_l.position.x = -half_w - 0.2
		R.wall_r.position.x = half_w + 0.2
		# threshold props
		R.props.camera.visible = P.compliance > 0.5
		R.props.numbers.visible = P.compliance > 0.62
		R.props.peephole.visible = P.curiosity > 0.6
		# creativity: chair floats
		if P.creativity > 0.5:
			R.chair.position.y = lerpf(R.chair.position.y, 0.6 + sin(t * 0.7) * 0.1, dt)
			R.chair.rotation.y += dt * 0.15
	# walls breathe with tension
	var tension: float = maxf(P.aggression, maxf(P.despair, P.creativity))
	R.wall_l.scale.y = 1.0 + sin(t * 0.8) * 0.012 * tension
	R.wall_r.scale.y = R.wall_l.scale.y
	# things move when unobserved
	var fwd := -player.cam.global_transform.basis.z
	var to_child := (R.child.global_position - player.global_position).normalized()
	if fwd.dot(to_child) < 0.0:
		unobs_child += dt
		if unobs_child > 6.0:
			unobs_child = 0.0
			R.child.position.z = clampf(R.child.position.z + (1.1 if randf() < 0.5 else -1.1), -2.0, 4.0)
			Telemetry.log_event("moved", {"who": "child"})
	else: unobs_child = 0.0
	var to_table := (Vector3(0, 1, -6) - player.global_position).normalized()
	if fwd.dot(to_table) < 0.0:
		unobs_cups += dt
		if unobs_cups > 7.0:
			unobs_cups = 0.0
			var x := R.cup_left.position.x
			R.cup_left.position.x = R.cup_right.position.x
			R.cup_right.position.x = x
			Telemetry.log_event("moved", {"who": "cups"})
	else: unobs_cups = 0.0
	# eyes track player + staring is meaningful
	for e in [R.eye_l, R.eye_r]:
		e.look_at(player.cam.global_position, Vector3.UP)
	if InputHub.focus_id in ["giant", "giant_eyes"]:
		stare += dt
		if stare > 4.2:
			stare = 0.0
			Profile.bump({"curiosity": 0.04, "despair": 0.02})
			GameState.whisper("You stare. It stares back. You feel yourself being read.")
	else: stare = 0.0
	# child breathing / anomaly spin / portal pulse / lamp flicker
	R.child_body.scale.y = 0.9 + sin(t * 1.6) * 0.02
	if anomaly:
		anomaly.rotation.x += dt; anomaly.rotation.y += dt * 1.4
		anomaly.position.y = 1.4 + sin(t) * 0.08
	if R.portal.visible:
		R.portal_light.light_energy = 1.8 + sin(t * 3.0) * 0.6
	if flick > 0.0:
		flick -= dt
		lamp.light_energy = clampf(lamp.light_energy * (0.4 + randf() * 0.9), 0.15, 3.0)

func do_flicker(s: float) -> void: flick = maxf(flick, s)

func _on_mutations(muts: Array) -> void:
	for m in muts:
		if m == "flicker": do_flicker(1.0)
		if m.begins_with("spawn:") and anomaly == null:
			anomaly = MeshInstance3D.new()
			var b := BoxMesh.new(); b.size = Vector3(0.28, 0.28, 0.28)
			anomaly.mesh = b
			var mat := StandardMaterial3D.new()
			mat.albedo_color = Color(0.62, 0.91, 0.67)
			mat.emission_enabled = true; mat.emission = Color(0.16, 0.35, 0.2)
			anomaly.material_override = mat
			anomaly.position = Vector3(player.position.x * 0.5, 1.4, player.position.z - 2.0)
			get_parent().add_child(anomaly)

func apply_ending(state: String) -> void:
	GameState.set_state(state)
	var E: Dictionary = rules.endings.get(state, {})
	lamp.light_color = Color.html(E.get("light", "ffffff"))
	env.fog_density = E.get("fog", 0.05)
	for p in E.get("props", []):
		if R.props.has(p): R.props[p].visible = true
	do_flicker(2.0)
	GameState.sys("WORLD REBUILT FROM OBSERVED BEHAVIOR")
	var blurb := StateEngine.blurb(state)
	if blurb != "":
		await get_tree().create_timer(1.4).timeout
		GameState.whisper(blurb)

func open_portal(color: Color, to: String) -> void:
	GameState.portal_to = to
	R.portal.visible = true
	R.portal_light.light_color = color
	(R.portal_glow.material_override as StandardMaterial3D).emission = color
