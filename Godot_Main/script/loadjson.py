from godot import exposed, export
from godot import *
import json


@exposed
class loadjson(Node):

	# member variables here, example:
	def load_json(self, text):
		return json.load(text)
