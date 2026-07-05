class_name FPPlayer
extends CharacterBody3D
## First-person controller. Reads ONLY from InputHub (+ raw WASD merged in).
## Raycasts focus each physics frame -> InputHub.set_focus().

var yaw := PI
var pitch := 0.0
var speed := 2.5
var bob := 0.0
var cam: Camera3D

func _ready() -> void:
	var col := CollisionShape3D.new()
	var cap := CapsuleShape3D.new(); cap.radius = 0.35; cap.height = 1.6
	col.shape = cap; col.position.y = 0.8
	add_child(col)
	cam = Camera3D.new(); cam.position.y = 1.62; cam.fov = 75
	add_child(cam)
	position = Vector3(0, 0, 8.6)

func _unhandled_input(e: InputEvent) -> void:
	if e is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		InputHub.look_delta += e.relative * 0.0022
	if e is InputEventMouseButton and e.pressed and not OS.has_feature("mobile"):
		if GameState.stats.t0 > 0 and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	if e is InputEventKey and e.pressed and e.keycode == KEY_ESCAPE:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _physics_process(dt: float) -> void:
	if GameState.stats.t0 == 0: return
	# merge keyboard into the abstraction layer (no InputMap setup needed)
	var mv := InputHub.move
	mv.y += (1.0 if Input.is_key_pressed(KEY_W) else 0.0) - (1.0 if Input.is_key_pressed(KEY_S) else 0.0)
	mv.x += (1.0 if Input.is_key_pressed(KEY_D) else 0.0) - (1.0 if Input.is_key_pressed(KEY_A) else 0.0)
	mv = mv.limit_length(1.0)

	yaw -= InputHub.look.x * 2.3 * dt + InputHub.look_delta.x
	pitch = clampf(pitch - (InputHub.look.y * 1.8 * dt + InputHub.look_delta.y), -1.15, 1.15)
	InputHub.look_delta = Vector2.ZERO
	rotation = Vector3(0, yaw, 0)
	cam.rotation = Vector3(pitch, 0, 0)

	var wish := (transform.basis * Vector3(mv.x, 0, -mv.y))
	var slow := 0.55 if mv.length() < 0.75 else 1.0
	velocity = wish * speed * slow
	velocity.y = 0
	move_and_slide()

	# soft bounds (giant side gated until progression)
	var zmin := -7.35
	if GameState.door_open or GameState.ended or GameState.state != "Giants_Drink":
		zmin = -RoomBuilder.ROOM.z / 2 + 1.0
	position.z = clampf(position.z, zmin, RoomBuilder.ROOM.z / 2 - 0.5)
	position.x = clampf(position.x, -RoomBuilder.ROOM.x / 2 + 0.5, RoomBuilder.ROOM.x / 2 - 0.5)

	if mv.length() > 0.05: bob += dt * 6.0 * mv.length()
	cam.position.y = 1.62 + sin(bob * 2.0) * 0.028

	_update_focus()

const FOCUS_DIST := {"cup_left": 2.6, "cup_right": 2.6, "giant_eyes": 7.5, "giant": 12.0,
	"child": 3.2, "mirror": 3.2, "door": 3.4, "table": 3.0, "portal": 3.4, "papers": 2.4}

func _update_focus() -> void:
	var from := cam.global_position
	var to := from + (-cam.global_transform.basis.z) * 14.0
	var q := PhysicsRayQueryParameters3D.create(from, to)
	q.exclude = [get_rid()]
	var hit := get_world_3d().direct_space_state.intersect_ray(q)
	if hit and hit.collider.has_meta("iid"):
		var iid: String = hit.collider.get_meta("iid")
		var d: float = from.distance_to(hit.position)
		if d <= FOCUS_DIST.get(iid, 3.0):
			InputHub.set_focus(iid, hit.collider.get_meta("label", iid))
			return
	InputHub.set_focus("", "")
