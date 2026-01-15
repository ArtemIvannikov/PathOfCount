from logic import PathOfCounter
from overlay import Overlay
from game_detector import GameDetector
from PyQt6.QtWidgets import QApplication, QWidget
import config
import sys

if __name__ == '__main__':
	logic = PathOfCounter()
	current_game = GameDetector().get_active_game_for_id()
	logic.database_connect(config.PATH, current_game)
	app = QApplication(sys.argv)
	app.setStyleSheet(config.STYLE_SHEET)  
	window = Overlay(logic, current_game)
	window.show()
	sys.exit(app.exec())
