class_name HUD
extends CanvasLayer
## Diegetic-leaning HUD: crosshair, focus label, whispered subtitles,
## brief system line, contextual action cluster, command layer, debug, report.

var logic: GameLogic
var dot: ColorRect
var focus_lbl: Label
var whisper_lbl: Label
var sys_lbl: Label
var cluster: VBoxContainer
var cmd_panel: PanelContainer
var cmd_edit: LineEdit
var debug_panel: PanelContainer
var debug_text: RichTextLabel
var term_panel: CenterContainer
var report_panel: CenterContainer
var whisper_timer: SceneTreeTimer

const ACTS := {
	"cup": [["Inspect", "inspect"], ["Pick up", "pickup"], ["Drink", "obey"], ["Break", "destroy"]],
	"cup_held": [["Drink", "obey"], ["Drop", "drop"]],
	"giant": [["Talk", "inspect"], ["Accuse", "deceive"], ["Attack", "attack"], ["Wait", "wait"]],
	"giant_eyes": [["Stare", "inspect"], ["STRIKE THE EYES", "attack"]],
	"child": [["Talk", "inspect"], ["Comfort", "help"], ["Give the cup", "give"]],
	"mirror": [["Look closer", "inspect"], ["Touch", "touch"], ["Pour the cup in", "sacrifice"], ["Break", "destroy"]],
	"door": [["Try the handle", "flee"], ["Inspect", "inspect"], ["Break it down", "destroy"]],
	"door_open": [["Step through", "through"]],
	"table": [["Inspect", "inspect"], ["Crawl under", "wait"]],
	"portal": [["Step through", "through"]],
	"papers": [["Read", "inspect"]],
	"none": [["Wait", "wait"]]
}

func build(game_logic: GameLogic) -> void:
	logic = game_logic
	# crosshair + focus label
	dot = ColorRect.new(); dot.color = Color(0.92, 0.94, 1.0, 0.75)
	dot.size = Vector2(5, 5)
	dot.set_anchors_preset(Control.PRESET_CENTER); dot.position -= Vector2(2.5, 2.5)
	add_child(dot)
	focus_lbl = _label(12, Color(0.86, 0.89, 0.96, 0.6))
	focus_lbl.set_anchors_preset(Control.PRESET_CENTER); focus_lbl.position = Vector2(-150, 22)
	focus_lbl.size = Vector2(300, 20); focus_lbl.horizontal_alignment = 1
	add_child(focus_lbl)
	# whisper + sysline
	whisper_lbl = _label(20, Color(0.91, 0.92, 0.96, 0.0))
	whisper_lbl.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	whisper_lbl.position += Vector2(-320, -130); whisper_lbl.size = Vector2(640, 90)
	whisper_lbl.horizontal_alignment = 1; whisper_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD
	add_child(whisper_lbl)
	sys_lbl = _label(11, Color(1.0, 0.72, 0.47, 0.0))
	sys_lbl.set_anchors_and_offsets_preset(Control.PRESET_CENTER_TOP)
	sys_lbl.position += Vector2(-250, 10); sys_lbl.size = Vector2(500, 20)
	sys_lbl.horizontal_alignment = 1
	add_child(sys_lbl)
	# sticks
	var l := VirtualStick.new(); l.position = Vector2(26, 0)
	l.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	l.position = Vector2(26, -166); add_child(l)
	var r := VirtualStick.new(); r.is_look = true
	r.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	r.position = Vector2(-166, -166); add_child(r)
	# cluster
	cluster = VBoxContainer.new()
	cluster.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	cluster.position = Vector2(-190, -420); cluster.size = Vector2(170, 240)
	cluster.alignment = BoxContainer.ALIGNMENT_END
	add_child(cluster)
	# command icon + panel
	var ci := Button.new(); ci.text = ">_"
	ci.set_anchors_preset(Control.PRESET_BOTTOM_LEFT); ci.position = Vector2(30, -230)
	ci.pressed.connect(open_cmd)
	add_child(ci)
	_build_cmd(); _build_debug(); _build_term(); _build_report()
	# wiring
	InputHub.focus_changed.connect(func(_i, l2): focus_lbl.text = l2; _cluster())
	GameState.whispered.connect(whisper)
	GameState.sysline.connect(sysline)
	GameState.cluster_dirty.connect(_cluster)
	GameState.terminated.connect(_on_term)
	GameState.report_ready.connect(_on_report)
	Profile.profile_changed.connect(_debug_refresh)
	GameState.state_changed.connect(func(_s): _debug_refresh())
	_cluster()

func _label(sz: int, col: Color) -> Label:
	var l := Label.new()
	l.add_theme_font_size_override("font_size", sz)
	l.add_theme_color_override("font_color", col)
	return l

func whisper(t: String) -> void:
	whisper_lbl.text = t
	whisper_lbl.add_theme_color_override("font_color", Color(0.91, 0.92, 0.96, 0.95))
	whisper_timer = get_tree().create_timer(1.6 + t.length() * 0.05)
	var mine := whisper_timer
	mine.timeout.connect(func():
		if whisper_timer == mine:
			whisper_lbl.add_theme_color_override("font_color", Color(0.91, 0.92, 0.96, 0.0)))

func sysline(t: String) -> void:
	sys_lbl.text = t
	sys_lbl.add_theme_color_override("font_color", Color(1.0, 0.72, 0.47, 0.9))
	get_tree().create_timer(2.6).timeout.connect(func():
		sys_lbl.add_theme_color_override("font_color", Color(1.0, 0.72, 0.47, 0.0)))

func _cluster() -> void:
	for c in cluster.get_children(): c.queue_free()
	var id := InputHub.focus_id
	var key := "none"
	if id.begins_with("cup"): key = "cup_held" if GameState.held == id else "cup"
	elif id == "door": key = "door_open" if GameState.door_open else "door"
	elif ACTS.has(id): key = id
	elif GameState.held != "": key = "cup_held"
	for pair in ACTS[key]:
		if pair[1] == "give" and GameState.held == "": continue
		if pair[1] == "sacrifice" and GameState.held == "": continue
		var b := Button.new(); b.text = pair[0]
		b.add_theme_font_size_override("font_size", 14)
		b.modulate = Color(1, 0.8, 0.76) if pair[1] in ["attack", "destroy"] else Color.WHITE
		var code: String = pair[1]
		b.pressed.connect(func(): _do(code))
		cluster.add_child(b)

func _do(code: String) -> void:
	var t := InputHub.focus_id
	match code:
		"pickup": logic.pick_up(t)
		"drop": logic.drop_cup()
		"touch": logic.touch_mirror()
		"through": logic.step_through(t)
		"give": logic.give_cup()
		_:
			var target := GameState.held if (code == "obey" and GameState.held != "") else t
			logic.dispatch({"intent": code, "target": target, "confidence": 0.92,
				"is_rule_breaking": Parser.is_rule_breaking(code, target), "raw": code}, false)
	_cluster()

func _build_cmd() -> void:
	cmd_panel = PanelContainer.new(); cmd_panel.visible = false
	cmd_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	cmd_panel.position += Vector2(-320, -140); cmd_panel.size = Vector2(640, 110)
	var v := VBoxContainer.new(); cmd_panel.add_child(v)
	var tag := _label(10, Color(1.0, 0.72, 0.47)); tag.text = "EXTERNAL INPUT CHANNEL — THE SIMULATION IS LISTENING"
	v.add_child(tag)
	var h := HBoxContainer.new(); v.add_child(h)
	cmd_edit = LineEdit.new(); cmd_edit.placeholder_text = "describe any action…  ('/debug' toggles dev panel)"
	cmd_edit.custom_minimum_size = Vector2(520, 36)
	cmd_edit.text_submitted.connect(func(_t): submit_cmd())
	h.add_child(cmd_edit)
	var go := Button.new(); go.text = "ACT"; go.pressed.connect(submit_cmd); h.add_child(go)
	add_child(cmd_panel)

func open_cmd() -> void:
	cmd_panel.visible = true
	Engine.time_scale = 0.15          # spec: time slows while typing
	cmd_edit.grab_focus()

func close_cmd() -> void:
	cmd_panel.visible = false
	Engine.time_scale = 1.0

func submit_cmd() -> void:
	var v := cmd_edit.text.strip_edges()
	cmd_edit.text = ""
	close_cmd()
	if v == "": return
	if v == "/debug": debug_panel.visible = not debug_panel.visible; _debug_refresh(); return
	Telemetry.log_event("command", {"raw": v.left(60)})
	logic.dispatch(Parser.parse(v), true)

func _input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed:
		if cmd_panel.visible and e.keycode == KEY_ESCAPE: close_cmd()
		elif not cmd_panel.visible and e.keycode in [KEY_C, KEY_SLASH]: open_cmd()
		elif e.keycode == KEY_E or e.keycode == KEY_SPACE:
			if cluster.get_child_count() > 0 and not cmd_panel.visible:
				cluster.get_child(0).emit_signal("pressed")
		elif e.keycode == KEY_QUOTELEFT:
			debug_panel.visible = not debug_panel.visible; _debug_refresh()

func _build_debug() -> void:
	debug_panel = PanelContainer.new(); debug_panel.visible = false
	debug_panel.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	debug_panel.position = Vector2(-290, 12); debug_panel.size = Vector2(276, 300)
	debug_text = RichTextLabel.new(); debug_text.bbcode_enabled = true
	debug_text.custom_minimum_size = Vector2(260, 290)
	debug_panel.add_child(debug_text)
	add_child(debug_panel)

func _debug_refresh() -> void:
	if not debug_panel.visible: return
	var s := "[b]STATE[/b] %s\n[b]PROFILE (DEV ONLY)[/b]\n" % GameState.state
	for k in Profile.P.keys():
		s += "%s %.2f  " % [k.left(3).to_upper(), Profile.P[k]]
	s += "\n[b]TELEMETRY[/b] %d events · local only" % Telemetry.events.size()
	debug_text.text = s

func _build_term() -> void:
	term_panel = _center_overlay()
	add_child(term_panel)

func _build_report() -> void:
	report_panel = _center_overlay()
	add_child(report_panel)

func _center_overlay() -> CenterContainer:
	var c := CenterContainer.new(); c.visible = false
	c.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var bg := ColorRect.new(); bg.color = Color(0.01, 0.01, 0.02, 0.94)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_STOP
	c.add_child(bg)
	return c

func _on_term(n: int, text: String) -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	for c in term_panel.get_children():
		if c is VBoxContainer: c.queue_free()
	var v := VBoxContainer.new(); v.alignment = BoxContainer.ALIGNMENT_CENTER
	var t1 := _label(13, Color(0.55, 0.6, 0.72)); t1.text = "TERMINATION %02d" % n; v.add_child(t1)
	var t2 := _label(34, Color(0.79, 0.42, 0.38)); t2.text = "terminated"; v.add_child(t2)
	var t3 := _label(14, Color(0.73, 0.65, 0.66)); t3.text = text
	t3.autowrap_mode = TextServer.AUTOWRAP_WORD; t3.custom_minimum_size = Vector2(460, 0); v.add_child(t3)
	var b := Button.new(); b.text = "OPEN YOUR EYES"
	b.pressed.connect(func(): term_panel.visible = false; logic.respawn()); v.add_child(b)
	term_panel.add_child(v)
	term_panel.visible = true

const TITLES := {
	"aggression": "THE DRAGON", "curiosity": "THE EXPLORER", "empathy": "THE HEALER",
	"compliance": "THE SOLDIER", "despair": "THE GHOST", "creativity": "THE INVENTOR"}

func _on_report() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	var v := VBoxContainer.new(); v.alignment = BoxContainer.ALIGNMENT_CENTER
	var d1 := Profile.dominant()
	var t1 := _label(12, Color(0.55, 0.6, 0.72)); t1.text = "SIMULATION ASSESSMENT — CLASSIFIED"; v.add_child(t1)
	var t2 := _label(40, Color(0.86, 0.9, 1.0)); t2.text = TITLES[d1]; v.add_child(t2)
	var st: Dictionary = GameState.stats
	var t3 := _label(13, Color(0.66, 0.7, 0.82))
	t3.text = "Terminated %d× · typed %d free commands · %d improvisations forced\nPATH: %s" % [
		st.deaths, st.typed, st.unscripted, " → ".join(PackedStringArray(st.path))]
	t3.horizontal_alignment = 1; v.add_child(t3)
	var t4 := _label(10, Color(0.45, 0.5, 0.62))
	t4.text = "fictional in-game assessment · gameplay behavior only · nothing leaves this device"
	v.add_child(t4)
	var b := Button.new(); b.text = "RUN IT AGAIN"
	b.pressed.connect(func(): get_tree().reload_current_scene(); Engine.time_scale = 1.0)
	v.add_child(b)
	report_panel.add_child(v)
	report_panel.visible = true
	Telemetry.save_local()
