import psutil
import config

class GameDetector():
	def __init__(self):
		self.current_game = None

	def get_active_game_for_id(self):
		games = config.GAMES
		for process in psutil.process_iter(['name']):
			if process.info['name'] in games:
				self.current_game = games[process.info['name']]
				return self.current_game
		return 'TEST'