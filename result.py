import json

class Result:
	def __init__(self, success: bool, info='', data=None):
		self.success = success
		self.info = info
		self.data = data

	def to_json(self):
		return json.dumps(
			{
				'success': self.success,
				'info': self.info,
				'data': json.loads(self.data) if type(self.data) == str else self.data,
			}
		)

class FalseResult(Result):
	def __init__(self, info='invalid session! Please try to connect again!'):
		super().__init__(success=False, info=info)
