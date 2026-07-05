class_name RoomBuilder
extends RefCounted
## Builds the Giant's Drink room procedurally and returns named refs.
## (Prototype choice: code-built scene = zero broken .tscn deps.
##  Replace pieces with authored scenes/PBR assets later.)

const ROOM := Vector3(9, 5.6, 24)   # w, h, l  (player starts +z, giant at -z)

static func _mat(color: Color, rough := 0.9, metal := 0.0, emiss := Color.BLACK) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color; m.roughness = rough; m.metallic = metal
	if emiss != Color.BLACK:
		m.emission_enabled = true; m.emission = emiss; m.emission_energy_multiplier = 1.2
	# worn-surface noise
	var n := NoiseTexture2D.new(); n.noise = FastNoiseLite.new(); n.noise.frequency = 0.12
	m.roughness_texture = n
	return m

static func _box(parent: Node, size: Vector3, pos: Vector3, mat: Material, iid := "", label := "") -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var b := BoxMesh.new(); b.size = size; mi.mesh = b
	mi.material_override = mat; mi.position = pos
	parent.add_child(mi)
	if iid != "": _collider(mi, size, iid, label)
	return mi

static func _collider(mi: MeshInstance3D, size: Vector3, iid: String, label: String) -> void:
	var body := StaticBody3D.new()
	var cs := CollisionShape3D.new(); var sh := BoxShape3D.new(); sh.size = size
	cs.shape = sh; body.add_child(cs); mi.add_child(body)
	body.set_meta("iid", iid); body.set_meta("label", label)

static func build(root: Node3D) -> Dictionary:
	var R := {}
	var wall := _mat(Color(0.62, 0.63, 0.6)); var floor_m := _mat(Color(0.42, 0.42, 0.41), 0.97)
	var wood := _mat(Color(0.45, 0.35, 0.25), 0.85); var metal := _mat(Color(0.55, 0.58, 0.62), 0.55, 0.6)
	var skin := _mat(Color(0.55, 0.52, 0.47), 0.92); var cloth := _mat(Color(0.23, 0.26, 0.32), 0.95)

	_box(root, Vector3(ROOM.x + 2, 0.3, ROOM.z + 2), Vector3(0, -0.15, 0), floor_m)
	_box(root, Vector3(ROOM.x + 2, 0.3, ROOM.z + 2), Vector3(0, ROOM.y + 0.15, 0), _mat(Color(0.4, 0.41, 0.39)))
	R.wall_l = _box(root, Vector3(0.4, ROOM.y, ROOM.z + 2), Vector3(-ROOM.x / 2 - 0.2, ROOM.y / 2, 0), wall)
	R.wall_r = _box(root, Vector3(0.4, ROOM.y, ROOM.z + 2), Vector3(ROOM.x / 2 + 0.2, ROOM.y / 2, 0), wall)
	_box(root, Vector3(ROOM.x + 2, ROOM.y, 0.4), Vector3(0, ROOM.y / 2, -ROOM.z / 2 - 0.2), wall)
	_box(root, Vector3(ROOM.x + 2, ROOM.y, 0.4), Vector3(0, ROOM.y / 2, ROOM.z / 2 + 0.2), wall)

	# long table + cups
	var table := Node3D.new(); table.position = Vector3(0, 0, -6); root.add_child(table)
	_box(table, Vector3(4.6, 0.14, 1.5), Vector3(0, 1.02, 0), wood, "table", "THE TABLE")
	for off in [Vector2(-2.1, -0.6), Vector2(2.1, -0.6), Vector2(-2.1, 0.6), Vector2(2.1, 0.6)]:
		_box(table, Vector3(0.12, 1, 0.12), Vector3(off.x, 0.5, off.y), wood)
	R.cup_left = _make_cup(root, Vector3(-0.55, 1.09, -5.72), "cup_left", "LEFT CUP")
	R.cup_right = _make_cup(root, Vector3(0.55, 1.09, -5.72), "cup_right", "RIGHT CUP")

	# GIANT
	var giant := Node3D.new(); giant.position = Vector3(0, 0, -9.4); root.add_child(giant)
	R.giant = giant
	var torso := MeshInstance3D.new(); var tm := CylinderMesh.new()
	tm.top_radius = 1.15; tm.bottom_radius = 1.5; tm.height = 2.6
	torso.mesh = tm; torso.material_override = cloth; torso.position.y = 2.5; giant.add_child(torso)
	_collider(torso, Vector3(2.6, 2.6, 2.6), "giant", "THE GIANT")
	var head := MeshInstance3D.new(); var hm := SphereMesh.new(); hm.radius = 0.95; hm.height = 1.9
	head.mesh = hm; head.material_override = skin; head.position.y = 4.5; giant.add_child(head)
	_collider(head, Vector3(1.9, 1.9, 1.9), "giant_eyes", "ITS EYES")
	R.head = head
	R.eye_l = _make_eye(giant, Vector3(-0.34, 4.55, 0.78))
	R.eye_r = _make_eye(giant, Vector3(0.34, 4.55, 0.78))
	R.arm_l = _make_arm(giant, -1, cloth, skin)
	R.arm_r = _make_arm(giant, 1, cloth, skin)

	# locked door behind giant
	var door := Node3D.new(); door.position = Vector3(0, 0, -ROOM.z / 2 + 0.05); root.add_child(door)
	_box(door, Vector3(1.5, 3, 0.22), Vector3(0, 1.5, 0), metal, "door", "THE LOCKED DOOR")
	R.door = door
	R.knob = _box(door, Vector3(0.12, 0.12, 0.12), Vector3(0.55, 1.4, 0.14), metal)

	# silent child (corner) — breathing handled by mutator
	var child := Node3D.new(); child.position = Vector3(-ROOM.x / 2 + 0.9, 0, 2.5)
	child.rotation.y = 0.7; root.add_child(child); R.child = child
	var cb := MeshInstance3D.new(); var cbm := SphereMesh.new(); cbm.radius = 0.34; cbm.height = 0.62
	cb.mesh = cbm; cb.material_override = _mat(Color(0.35, 0.38, 0.44)); cb.position.y = 0.34; child.add_child(cb)
	_collider(cb, Vector3(0.8, 1.2, 0.8), "child", "THE CHILD")
	R.child_body = cb
	var ch := MeshInstance3D.new(); var chm := SphereMesh.new(); chm.radius = 0.2; chm.height = 0.4
	ch.mesh = chm; ch.material_override = skin; ch.position = Vector3(0, 0.72, 0.1); child.add_child(ch)

	# mirror on right wall (fake reflection: silhouette panel — upgrade path: planar probe)
	var mirror := Node3D.new(); mirror.position = Vector3(ROOM.x / 2 - 0.06, 1.7, -1)
	mirror.rotation.y = -PI / 2; root.add_child(mirror); R.mirror = mirror
	_box(mirror, Vector3(1.5, 2.2, 0.1), Vector3.ZERO, wood, "mirror", "THE MIRROR")
	var glass := _mat(Color(0.07, 0.09, 0.12), 0.1, 0.85, Color(0.04, 0.06, 0.09))
	R.glass = _box(mirror, Vector3(1.28, 1.96, 0.02), Vector3(0, 0, 0.06), glass)
	R.sil = _box(mirror, Vector3(0.5, 1.2, 0.01), Vector3(0.1, -0.1, 0.08),
		_mat(Color(0.17, 0.2, 0.26), 1.0))

	# props: fallen chair, papers
	R.chair = _box(root, Vector3(0.5, 0.5, 0.5), Vector3(2.6, 0.3, 1.8), wood)
	R.chair.rotation = Vector3(1.3, 0.9, 0)
	_box(root, Vector3(0.35, 0.01, 0.5), Vector3(-1.8, 0.02, 0.5), _mat(Color(0.79, 0.76, 0.68)), "papers", "OLD PAPERS")

	# exit portal (hidden until an ending)
	var portal := Node3D.new(); portal.position = Vector3(0, 0, ROOM.z / 2 - 0.1)
	portal.rotation.y = PI; portal.visible = false; root.add_child(portal); R.portal = portal
	_box(portal, Vector3(1.6, 3.1, 0.2), Vector3(0, 1.55, 0), metal, "portal", "THE NEW DOOR")
	var glow_m := _mat(Color.WHITE, 0.3, 0, Color.WHITE)
	R.portal_glow = _box(portal, Vector3(1.3, 2.8, 0.02), Vector3(0, 1.55, 0.12), glow_m)
	var pl := OmniLight3D.new(); pl.light_energy = 2.0; pl.position = Vector3(0, 1.6, 0.6)
	portal.add_child(pl); R.portal_light = pl

	# mutation prop groups
	R.props = {}
	for group_name in ["numbers", "camera", "peephole", "plants", "teeth", "candles"]:
		var g := Node3D.new(); g.visible = false; root.add_child(g); R.props[group_name] = g
	_fill_props(R)
	return R

static func _make_cup(root: Node, pos: Vector3, iid: String, label: String) -> MeshInstance3D:
	var mi := MeshInstance3D.new(); var c := CylinderMesh.new()
	c.top_radius = 0.075; c.bottom_radius = 0.06; c.height = 0.16
	mi.mesh = c; mi.material_override = _mat(Color(0.85, 0.82, 0.77), 0.4)
	mi.position = pos; root.add_child(mi)
	_collider(mi, Vector3(0.2, 0.24, 0.2), iid, label)
	return mi

static func _make_eye(giant: Node, pos: Vector3) -> MeshInstance3D:
	var e := MeshInstance3D.new(); var s := SphereMesh.new(); s.radius = 0.17; s.height = 0.34
	e.mesh = s; e.material_override = _mat(Color(0.91, 0.89, 0.85), 0.25)
	e.position = pos; giant.add_child(e)
	var iris := MeshInstance3D.new(); var im := SphereMesh.new(); im.radius = 0.07; im.height = 0.14
	iris.mesh = im
	iris.material_override = _mat(Color(0.16, 0.2, 0.27), 0.2, 0, Color(0.03, 0.06, 0.1))
	iris.position.z = 0.13; e.add_child(iris)
	e.set_meta("iris", iris)
	return e

static func _make_arm(giant: Node, side: int, cloth: Material, skin: Material) -> Node3D:
	var a := Node3D.new(); a.position = Vector3(0, 3.4, 0.4); giant.add_child(a)
	var up := MeshInstance3D.new(); var um := CapsuleMesh.new(); um.radius = 0.28; um.height = 1.7
	up.mesh = um; up.material_override = cloth
	up.rotation.z = side * 0.5; up.position = Vector3(side * 0.8, -0.6, 0); a.add_child(up)
	var hand := MeshInstance3D.new(); var hm := SphereMesh.new(); hm.radius = 0.3; hm.height = 0.6
	hand.mesh = hm; hand.material_override = skin
	hand.position = Vector3(side * 1.6, -1.9, 1.5); a.add_child(hand)
	return a

static func _fill_props(R: Dictionary) -> void:
	# numbered plaques (compliance)
	for i in range(4):
		for side in [-1, 1]:
			var l := Label3D.new()
			l.text = "%02d" % (i + 1 + (0 if side < 0 else 4))
			l.font_size = 120; l.modulate = Color(0.82, 0.86, 0.92)
			l.position = Vector3(side * (ROOM.x / 2 - 0.06), 2.1, 3 - i * 3.4)
			l.rotation.y = side * -PI / 2
			R.props.numbers.add_child(l)
	# camera (compliance)
	var cam := MeshInstance3D.new(); var cm := BoxMesh.new(); cm.size = Vector3(0.3, 0.16, 0.22)
	cam.mesh = cm; cam.material_override = _mat(Color(0.5, 0.53, 0.58), 0.5, 0.6)
	cam.position = Vector3(ROOM.x / 2 - 0.35, ROOM.y - 0.4, 4); cam.rotation.y = -2.3
	R.props.camera.add_child(cam)
	# peephole light shaft (curiosity)
	var peep := MeshInstance3D.new(); var pm := SphereMesh.new(); pm.radius = 0.07; pm.height = 0.14
	peep.mesh = pm; peep.material_override = _mat(Color(0.75, 0.9, 1), 0.2, 0, Color(0.7, 0.9, 1))
	peep.position = Vector3(-ROOM.x / 2 + 0.06, 1.6, -2.8)
	R.props.peephole.add_child(peep)
	var shaft := SpotLight3D.new(); shaft.light_color = Color(0.75, 0.9, 1)
	shaft.light_energy = 3.0; shaft.spot_angle = 12
	shaft.position = peep.position; shaft.rotation.y = -PI / 2
	R.props.peephole.add_child(shaft)
	# plants (empathy / fairyland)
	for i in range(12):
		var s := MeshInstance3D.new(); var sm := SphereMesh.new()
		sm.radius = 0.05 + randf() * 0.05; sm.height = sm.radius * 2
		s.mesh = sm
		s.material_override = _mat(Color(0.45, 0.69, 0.42), 0.8, 0, Color(0.08, 0.2, 0.08))
		s.position = Vector3(randf_range(-3, 3), 1.12 if i < 6 else 0.06,
			randf_range(-6.8, -5.6) if i < 6 else randf_range(-7, 7))
		R.props.plants.add_child(s)
	# teeth (violence fairyland)
	for i in range(9):
		var t := MeshInstance3D.new(); var tm2 := CylinderMesh.new()
		tm2.top_radius = 0.0; tm2.bottom_radius = 0.16 + randf() * 0.14
		tm2.height = 0.9 + randf() * 1.3
		t.mesh = tm2; t.material_override = _mat(Color(0.91, 0.92, 0.95), 0.35)
		var up := i % 2 == 0
		t.position = Vector3(randf_range(-3.5, 3.5), (ROOM.y - tm2.height / 2) if up else tm2.height / 2, randf_range(-11, -2))
		if up: t.rotation.x = PI
		R.props.teeth.add_child(t)
	# candles (despair)
	for i in range(6):
		var c := Node3D.new()
		c.position = Vector3(-ROOM.x / 2 + 0.5 + randf() * 0.6, 1.1, -8 + i * 2.6)
		var w := MeshInstance3D.new(); var wm := CylinderMesh.new()
		wm.top_radius = 0.03; wm.bottom_radius = 0.035; wm.height = 0.22
		w.mesh = wm; w.material_override = _mat(Color(0.85, 0.8, 0.72), 0.8); c.add_child(w)
		var fl := OmniLight3D.new(); fl.light_color = Color(1, 0.69, 0.38)
		fl.light_energy = 0.6; fl.omni_range = 3; fl.position.y = 0.2; c.add_child(fl)
		R.props.candles.add_child(c)
