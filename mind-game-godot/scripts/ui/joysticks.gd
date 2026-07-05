class_name VirtualStick
extends Control
## Glass-style virtual joystick. Writes into InputHub (abstraction layer).

@export var is_look := false     # false = move (left), true = look (right)
var touch_index := -1
var center := Vector2.ZERO
var knob := Vector2.ZERO
const R := 56.0

func _ready() -> void:
	custom_minimum_size = Vector2(140, 140)
	mouse_filter = Control.MOUSE_FILTER_STOP

func _gui_input(e: InputEvent) -> void:
	if e is InputEventScreenTouch:
		if e.pressed and touch_index == -1:
			touch_index = e.index
			center = size / 2.0
			_apply(e.position)
		elif not e.pressed and e.index == touch_index:
			_release()
	elif e is InputEventScreenDrag and e.index == touch_index:
		_apply(e.position)

func _apply(p: Vector2) -> void:
	var v := (p - center).limit_length(R)
	knob = v
	var out := v / R
	if is_look: InputHub.look = out
	else: InputHub.move = Vector2(out.x, -out.y)
	queue_redraw()

func _release() -> void:
	touch_index = -1
	knob = Vector2.ZERO
	if is_look: InputHub.look = Vector2.ZERO
	else: InputHub.move = Vector2.ZERO
	queue_redraw()

func _draw() -> void:
	var c := size / 2.0
	var live := touch_index != -1
	draw_arc(c, R, 0, TAU, 48, Color(0.93, 0.95, 1.0, 0.5 if live else 0.28), 1.5, true)
	draw_circle(c + knob, 24, Color(0.93, 0.95, 1.0, 0.22 if live else 0.14))
	draw_arc(c + knob, 24, 0, TAU, 32, Color(0.94, 0.96, 1.0, 0.55 if live else 0.4), 1.5, true)
