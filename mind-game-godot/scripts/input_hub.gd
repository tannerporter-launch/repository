extends Node
## Autoload: INPUT ABSTRACTION LAYER (spec).
## Touch sticks / WASD / mouse / buttons / typed text all write here;
## the player controller + game logic only ever read from here.

signal focus_changed(id: String, label: String)

var move := Vector2.ZERO        # left stick / WASD (x strafe, y forward)
var look := Vector2.ZERO        # right stick rate
var look_delta := Vector2.ZERO  # mouse relative
var focus_id := ""
var focus_label := ""

func set_focus(id: String, label: String) -> void:
	if id == focus_id: return
	focus_id = id
	focus_label = label
	focus_changed.emit(id, label)
