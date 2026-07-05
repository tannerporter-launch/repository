extends Node
## Autoload: LOCAL-ONLY gameplay telemetry (design constraint: never networked,
## no real personal data). Saved to user://telemetry_session.json.

var events: Array = []

func log_event(type: String, data := {}) -> void:
	var e := {"t": Time.get_ticks_msec() / 1000.0, "type": type}
	e.merge(data)
	events.append(e)
	if events.size() > 600: events.pop_front()

func save_local() -> void:
	var f := FileAccess.open("user://telemetry_session.json", FileAccess.WRITE)
	if f: f.store_string(JSON.stringify(events, "  "))

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST or what == NOTIFICATION_APPLICATION_PAUSED:
		save_local()
