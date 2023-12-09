import flask
import uuid

from log import Log
from session import Session
from room import get_room, add_room, Room
from result import Result, FalseResult

app = flask.Flask("Werewolf")
sessions = {'0': Session('0')}
logger = Log("./werewolf_server.log")

def check_session() -> bool:
	try:
		uid = flask.request.cookies.get("uid")
		if uid in sessions:
			return True
		else:
			logger.add_log(f"invalid uid `{uid}`")
			return False
	except:
		return False

def new_session() -> Session:
	uid = str(uuid.uuid1())
	while uid in sessions:
		uid = str(uuid.uuid1())
	sessions[uid] = Session(uid)
	return sessions[uid]

def send_html(file_name):
	return flask.send_from_directory("templates", file_name)

def get_json_data(key):
	return flask.request.json[key] if key in flask.request.json else None

def add_player_into_room(uid, room_id):
	room = get_room(room_id)
	if room.add_player(uid) is False:
		return False
	sessions[uid].data['room'] = room
	sessions[uid].data['room_id'] = room_id
	logger.add_log(f"session `{uid}` join room `{room_id}`")
	return True

# gui
@app.route("/")
def root():
	return send_html("root.html")

@app.route("/index")
def index():
	return send_html("index.html")

@app.route("/create")
def create():
	return send_html("create.html")

@app.route("/join")
def join():
	return send_html("join.html")

@app.route("/room")
def room():
	return send_html("room.html")

# js & css
@app.route("/js/<js_file_path>")
def js(js_file_path):
	return flask.send_from_directory("templates/js", js_file_path)

@app.route("/css/<css_file_path>")
def css(css_file_path):
	return flask.send_from_directory("templates/css", css_file_path)

# api
@app.route("/api/connect")
def connect():
	# 如果有合法的，那就返回先有的
	if check_session() is True:
		uid = flask.request.cookies.get("uid")
		return Result(True, data=sessions[uid].to_json()).to_json()
	# 否则新建一个
	session = new_session()
	logger.add_log(f"new session with uid `{session.uid}`")
	return Result(True, data=session.to_json()).to_json()

@app.route("/api/create_room", methods=["POST"])
def create_room():
	if check_session() is False: return FalseResult().to_json()
	# 创建房号
	room_id = str(uuid.uuid1())[:4]
	# 读取数据
	player_num = get_json_data("player_num")
	player_kind = get_json_data("player_kind")
	uid = flask.request.cookies.get("uid")
	if player_num is None or player_kind is None:
		logger.add_log(f"session `{uid}` failed to create room because of invalid player_num or player_kind")
		return FalseResult('invalid player_num or player_kind').to_json()
	# 创建房间
	room = Room(room_id, player_num, player_kind)
	add_room(room)
	# 加入创建
	if add_player_into_room(uid, room_id) is False:
		logger.add_log(f'failed to join session `{uid}` into room `{room_id}`')
		return FalseResult('failed to join into room').to_json()
	# 返回
	logger.add_log(f"create room with room_id `{room_id}` by session `{uid}`")
	return Result(True, data=sessions[uid].to_json()).to_json()

@app.route("/api/join_room", methods=["GET"])
def join_room():
	if check_session() is False: return FalseResult().to_json()
	room_id = flask.request.values.get("room_id")
	uid = flask.request.cookies.get("uid")
	if add_player_into_room(uid, room_id) is False:
		return FalseResult('failed to join into room').to_json()
	else:
		return Result(True, data=sessions[uid].to_json()).to_json()

@app.route("/api/update_session", methods=["POST"])
def update_session():
	if check_session() is False: return FalseResult().to_json()
	uid = flask.request.cookies.get("uid")
	sessions[uid].load_json(flask.request.values.get("session"))
	logger.add_log(f"update session `{uid}`")

@app.route("/api/get_session", methods=["POST"])
def get_session():
	if check_session() is False: return FalseResult().to_json()
	uid = flask.request.cookies.get("uid")
	return Result(True, data=sessions[uid].to_json()).to_json()

@app.route("/api/check_room_id", methods=["GET"])
def check_room_id():
	if check_session() is False: return FalseResult().to_json()
	room_id = flask.request.cookies.get("room_id")
	if get_room(room_id) is None:
		return FalseResult('invalid room_id').to_json()
	else:
		return Result(True).to_json()

@app.route("/api/check_session", methods=["GET"])
def check_session_api():
	if check_session() is False: return FalseResult().to_json()
	else: return Result(True).to_json()

# main
if __name__ == "__main__":
	app.run('0.0.0.0', 8091)
