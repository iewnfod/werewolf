rooms = {}

class Room:
	def __init__(self, room_id, player_num, player_kind):
		self.room_id = room_id
		self.player_num = int(player_num)
		self.player_kind = player_kind
		self.players = {i: None for i in range(1, player_num+1)}

	def load_data(self, data):
		self.player_num = data['player_num']
		self.player_kind = data['player_kind']
		self.room_id = data['room_id']

	def to_dict(self):
		return {
			"room_id": self.room_id,
			"player_num": self.player_num,
			"player_kind": self.player_kind,
			"players": self.players,
		}

	def add_player(self, player_uid):
		for i in range(1, self.player_num+1):
			if self.players[i] is None:
				self.players[i] = player_uid
				return True
		return False

def add_room(room: Room):
	rooms[room.room_id] = room

def get_room(room_id) -> Room:
	if room_id in rooms:
		return rooms[room_id]
	else:
		return None
