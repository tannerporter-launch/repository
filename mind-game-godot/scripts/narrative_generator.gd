extends Node
## Autoload: rule-based surreal narrative (spec: minimal, unsettling, no mechanics talk).

const STEMS := {
	"attack": "You move against it. It does not scream — the room does.",
	"destroy": "It comes apart in slow, obedient pieces, then reconsiders.",
	"deceive": "You lie. The room believes you completely. That is the frightening part.",
	"sacrifice": "You give it away. The floor drinks the gesture.",
	"unknown": "The simulation has no rule for that. It writes one, humming."
}
const FRAG := {
	"aggression": "Something sharp takes root in the floor.",
	"curiosity": "A drawer, somewhere, opens one inch.",
	"empathy": "The light goes soft, like a held breath released.",
	"compliance": "A rule you never read thanks you.",
	"despair": "The color forgets itself a little.",
	"creativity": "An impossible corner appears, delighted."
}

func gen(action: Dictionary, stem_override := "") -> String:
	var stem: String = stem_override if stem_override != "" else STEMS.get(action.get("intent", "unknown"), STEMS.unknown)
	return stem + " " + FRAG[Profile.dominant()]
