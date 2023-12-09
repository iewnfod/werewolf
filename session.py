import time
import json
from room import get_room

class Session:
	def __init__(self, uid):
		self.uid = str(uid)
		self.start_time = time.time()
		self.duration = 86400000  # 24个小时

		self.data = {
			"uid": self.uid,  # session uid
			"room": None,  # 房间
			"room_id": None,  # 房间号
			"identity": None,  # 身份
			"status": None,  # 是否活着
		}

	def timeout(self):
		return time.time() - self.start_time > self.duration

	def load_json(self, json_data):
		data = json.loads(json_data)
		for k, v in data.items():
			if k == 'room':
				room = get_room(v['room_id'])
				room.load_data(v)
			self.data[k] = v

	def to_json(self):
		json_data = self.data.copy()
		json_data['room'] = json_data['room'].to_dict() if json_data['room'] is not None else None
		return json.dumps(json_data)
