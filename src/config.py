from PyQt6.QtCore import Qt 

#database path
PATH = 'my_database.db'

#ICON PATH
PATH_TO_ICON = "C:/Users/Babazaki/Desktop/76666/PathOfCount/Icon.png"

#List Oof games
GAMES = {
	'PathOfExile.exe': 'Poe',
	'PathOfExile_x64.exe': 'Poe'

}

#Overlay size and pozition, and others
X = 200
Y = 760
H = 100
W = 100
TITLE = 'PathOfCount'
FLAGS = (Qt.WindowType.NoDropShadowWindowHint | 
		Qt.WindowType.FramelessWindowHint |
		Qt.WindowType.WindowStaysOnTopHint  

		)


STYLE_SHEET = '''
	QPushButton {
            border: none;
            background-color: transparent;
            color: #D8BFD8;
            padding: 20px;
            font-size: 18px;
            font-weight: bold;
            font-family: Fontin SmallCaps;
            padding: 0px;
        	min-height: 20px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QLabel {
            color: #D8BFD8;
            font-size: 18px;
            font-family: Fontin SmallCaps;
        }

        getText {
            background-color: rgba(0, 0, 0, 0);
        }

        QMenu {
           font-family: Fontin SmallCaps; 
        }
        /* Стили для QMenu */
    QMenu {
        background-color: #2b2b2b;
        color: #D8BFD8;
        border: 1px solid #555;
        font-family: Fontin SmallCaps;
        font-size: 14px;
    }
    QMenu::item:selected {
        background-color: #3d3d3d;
    }
    QMenu::separator {
        height: 1px;
        background: #555;
        margin: 4px 0px;
    }
    
    /* Стили для QInputDialog */
    QDialog {
        background-color: #2b2b2b;
        color: #D8BFD8;
        font-family: Fontin SmallCaps;
    }
    QLineEdit {
        background-color: #1a1a1a;
        color: #D8BFD8;
        border: 1px solid #555;
        padding: 5px;
        font-family: Fontin SmallCaps;
    }
    QSpinBox {
        background-color: #1a1a1a;
        color: #D8BFD8;
        border: 1px solid #555;
        padding: 5px;
        font-family: Fontin SmallCaps;
    }
    QDialogButtonBox QPushButton {
        background-color: #3d3d3d;
        border: 1px solid #555;
        padding: 5px 15px;
        min-width: 60px;
    }
    QDialogButtonBox QPushButton:hover {
        background-color: #4d4d4d;
    }
'''
	
# HOTKEYS = {
#     '<ctrl>+<alt>+k': self.kill_application,
#     'clickableness': 'ctrl+shift+alt+l',
#     'movebleness': 'ctrl+shift+alt+m',


# }    
