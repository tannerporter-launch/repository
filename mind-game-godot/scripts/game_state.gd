extends Node
## Autoload: global run state, stats, and cross-system signals.

signal state_changed(state: String)
signal whispered(text: String)
signal sysline(text: String)
signal cluster_dirty
signal terminated(n: int, text: String)
signal report_ready

var state: String = "Giants_Drink"
var ended := false
var held := ""                      # "", "cup_left", "cup_right"
var door_open := false
var door_to := ""
var portal_to := ""

var stats := {
	"deaths": 0, "unscripted": 0, "typed": 0,
	"decisions": [], "t0": 0.0, "path": ["GIANTS_DRINK"]
}

func set_state(s: String) -> void:
	state = s
	stats.path.append(s.to_upper())
	state_changed.emit(s)

func whisper(t: String) -> void: whispered.emit(t)
func sys(t: String) -> void: sysline.emit(t)
