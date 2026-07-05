extends Node
## OPTIONAL (spec "future upgrades"): route rule-breaking actions through a
## local LLM via Ollama for improvised narrative. Disabled by default — the
## rule-based Narrative generator is the fallback and requires no network.
## Enable: add as autoload, then in RuleBreaker call OllamaBridge.improvise().

const URL := "http://localhost:11434/api/generate"
const MODEL := "phi3"   # or mistral / llama3

signal improvised(text: String)

func improvise(action: Dictionary) -> void:
	var http := HTTPRequest.new(); add_child(http)
	http.request_completed.connect(func(_r, code, _h, body):
		if code == 200:
			var j = JSON.parse_string(body.get_string_from_utf8())
			improvised.emit(j.get("response", "").strip_edges())
		else:
			improvised.emit(Narrative.gen(action))   # graceful fallback
		http.queue_free())
	var prompt := "You are the narrator of a surreal psychological simulation. In <=2 unsettling poetic sentences, describe the world reconciling this unscripted player action: %s (dominant trait: %s). No meta talk." % [action.get("raw", "?"), Profile.dominant()]
	var body := JSON.stringify({"model": MODEL, "prompt": prompt, "stream": false})
	http.request(URL, ["Content-Type: application/json"], HTTPClient.METHOD_POST, body)
