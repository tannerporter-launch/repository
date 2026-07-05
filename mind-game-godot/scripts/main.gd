extends Node3D
## Bootstrap: environment + lights + room + player + mutator + logic + HUD.
## Pipeline (spec): Input -> Parser -> Telemetry -> Profile -> StateEngine
##                  -> RuleBreaker/Logic -> WorldMutator -> world.

var refs: Dictionary
var mut: WorldMutator
var logic: GameLogic
var hud: HUD
var lamp: OmniLight3D

func _ready() -> void:
	randomize()
	# environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.02, 0.024, 0.028)
	env.fog_enabled = true
	env.fog_light_color = Color(0.03, 0.035, 0.04)
	env.fog_density = 0.03
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.glow_enabled = true
	var we := WorldEnvironment.new(); we.environment = env
	add_child(we)
	# lights
	var hemi := DirectionalLight3D.new()
	hemi.light_energy = 0.12; hemi.rotation_degrees = Vector3(-55, 30, 0)
	add_child(hemi)
	lamp = OmniLight3D.new()
	lamp.light_color = Color(1.0, 0.85, 0.65); lamp.light_energy = 2.2
	lamp.omni_range = 16; lamp.shadow_enabled = true
	lamp.position = Vector3(0, 4.3, -6)
	add_child(lamp)
	# world + systems
	refs = RoomBuilder.build(self)
	var player := FPPlayer.new(); add_child(player)
	mut = WorldMutator.new(); add_child(mut)
	mut.setup(refs, env, lamp, player)
	logic = GameLogic.new(); add_child(logic)
	logic.setup(refs, mut, player)
	hud = HUD.new(); add_child(hud)
	hud.build(logic)
	_title()

func _title() -> void:
	var c := CenterContainer.new()
	c.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var bg := ColorRect.new(); bg.color = Color(0, 0, 0, 0.9)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	c.add_child(bg)
	var v := VBoxContainer.new(); v.alignment = BoxContainer.ALIGNMENT_CENTER
	var t := Label.new(); t.text = "THE  MIND  GAME"
	t.add_theme_font_size_override("font_size", 44); v.add_child(t)
	var s := Label.new()
	s.text = "Left stick moves · right stick looks · buttons act · >_ types anything.\nNothing is forbidden. Everything is observed."
	s.horizontal_alignment = 1; v.add_child(s)
	var b := Button.new(); b.text = "WAKE UP INSIDE"
	c.add_child(v)
	v.add_child(b)
	hud.add_child(c)
	b.pressed.connect(func():
		c.queue_free()
		GameState.stats.t0 = Time.get_ticks_msec() / 1000.0
		await get_tree().create_timer(1.2).timeout
		GameState.whisper('"Drink, little mouse. One cup is honey… the other, oblivion. Choose."'))
