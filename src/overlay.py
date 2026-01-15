import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QMenu
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
import config
from pynput import keyboard as kb



class Overlay(QWidget):
    signal_kill = pyqtSignal()
    signal_clickableness = pyqtSignal()
    signal_movebleness = pyqtSignal()

    def __init__(self, logic, current_game):
        super().__init__()
        self.logic = logic
        self.current_game = current_game
        self.amount_labels = {}
        self.active_counter_id = None
        self.click_through = False
        self.movable = False
        self.drag_position = None

        self.init_ui()

        self.signal_kill.connect(self._kill_application)
        self.signal_clickableness.connect(self._change_clickableness)
        self.signal_movebleness.connect(self._change_movebleness)

        self.setup_hotkeys()

    def setup_hotkeys(self):
        hotkeys = kb.GlobalHotKeys({
            '<ctrl>+<alt>+k': self.kill_application,
            '<ctrl>+<alt>+l': self.change_clickableness,
            '<ctrl>+<alt>+m': self.change_movebleness,
            '<ctrl>+<alt>+л': self.kill_application,
            '<ctrl>+<alt>+д': self.change_clickableness,
            '<ctrl>+<alt>+ь': self.change_movebleness,
                })
        hotkeys.start()

    # def mousePressEvent(self, event):
        # self.drag_position = QPoint(0, 50)
        # print(f"✓ Drag position: {self.drag_position}")
        # if self.movable and event.button() == Qt.MouseButton.LeftButton:
        #     # Проверяем, что клик НЕ по виджету (кнопке)
        #     widget_at_pos = self.childAt(event.pos())
            
        #     if widget_at_pos is None:  # Клик на пустом месте
        #         self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().center()
        #         print(f"✓ Drag position: {self.drag_position}")
        #         event.accept()
        #     # else:
        #     #     # Если кликнули на кнопку - игнорируем
        #     #     super().mousePressEvent(event)
        # else:
        #     super().mousePressEvent(event)
        

    def mouseMoveEvent(self, event):
        if self.movable and event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept() 

    def _kill_application(self):
        self.close()
        QApplication.quit()

    def kill_application(self):
        self.signal_kill.emit()

    def _change_movebleness(self):
        self.movable = not self.movable

        if self.movable and self.click_through:
            self.signal_clickableness.emit()



        if self.movable:
            self.drag_position = QPoint(50, 50)
            self.hide()
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

            self.setStyleSheet(config.STYLE_SHEET + """
                #MainOverlay {
                    background-color: rgb(255, 99, 71);
                }
            """)


        else:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setStyleSheet(config.STYLE_SHEET)
        
        self.show()
        self.repaint()
    
    def change_movebleness(self):
        self.signal_movebleness.emit()
 
    def _change_clickableness(self):
        self.click_through = not self.click_through

        if self.click_through:
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowType.WindowTransparentForInput
            )
            self.setWindowOpacity(0.5)  

        else:
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowType.WindowTransparentForInput
            )
            self.setWindowOpacity(1.0)

        self.show()

        current_pos = self.pos()
        self.move(current_pos)

    def change_clickableness(self):
        self.signal_clickableness.emit()

    def init_ui(self):
        self.setObjectName("MainOverlay")
        self.setGeometry(config.X, config.Y, config.W, config.H)
        self.setWindowTitle(config.TITLE)
        self.setWindowFlags(config.FLAGS)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True) #ЭТО СЕРЬЕЗНЕЙШАЯ ПРОБЛЕМА, НЕВОЗМОЖНО ПОНЯТЬ МОТИВАЦИЮ СОЗДАТЕЛЕЙ ЭТОГО АТТРИБУТА

        self.setStyleSheet(config.STYLE_SHEET)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.create_buttons()

    def refresh_ui(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

        self.amount_labels.clear()
        self.create_buttons()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def create_buttons(self):
        items = self.logic.select_all_countable_items(self.current_game)
        print(items)

        main_layout = QHBoxLayout()

        if items:

            if self.active_counter_id == None:
                self.active_counter_id = items[0][0]
                print(self.active_counter_id)

            active_item = None
            for item in items:
                if item[0] == self.active_counter_id:
                    active_item = item
                    break

            if active_item == None:
                active_item = items[0]
                self.active_counter_id = active_item[0]


            item = active_item
            item_id = item[0]
            item_name = item[1]
            amount = item[2]

            

            label_button = QPushButton(f'{item_name}')
            label_button.clicked.connect(lambda pos: self.show_item_context_menu(pos, item_id))
            main_layout.addWidget(label_button)

            button_minus = QPushButton(' <  ')
            button_minus.clicked.connect(lambda _, item_id = item_id: self.on_minus_clicked(item_id))
            main_layout.addWidget(button_minus)

            amount_button = QPushButton(f' {amount} ')
            amount_button.clicked.connect(lambda _, item_id = item_id: self.on_custom_clicked(item_id))
            self.amount_labels[item_id] = amount_button
            main_layout.addWidget(amount_button)

            button_plus = QPushButton('  > ')
            button_plus.clicked.connect(lambda _, item_id = item_id: self.on_plus_clicked(item_id))
            main_layout.addWidget(button_plus)

        side_layout = QVBoxLayout()

        button_select = QPushButton('☰')
        button_select.clicked.connect(self.show_counter_selector)
        side_layout.addWidget(button_select)

        button_menu = QPushButton('⚙')
        button_menu.clicked.connect(self.show_menu_selector)
        side_layout.addWidget(button_menu)
        
        main_layout.addLayout(side_layout)
        self.layout.addLayout(main_layout)
            

    def on_plus_clicked(self, item_id):
        self.logic.change_amount_of_countable_items('+', self.current_game, item_id, 1)

        item = self.logic.get_current_item_by_id(self.current_game, item_id)
        new_amount = item[2]
        self.amount_labels[item_id].setText(f'{new_amount}')

    def on_minus_clicked(self, item_id):
        self.logic.change_amount_of_countable_items('-', self.current_game, item_id, 1)

        item = self.logic.get_current_item_by_id(self.current_game, item_id)
        new_amount = item[2]
        self.amount_labels[item_id].setText(f'{new_amount}')

    def on_custom_clicked(self, item_id):
        entered_amount, ok = QInputDialog.getInt(
        self,  # родительское окно
        'Custom value',  # заголовок
        'Enter value',  # текст
        # 0,  # начальное значение
        # -9999999,  # минимум
        # 9999999  # максимум
        flags=Qt.WindowType.FramelessWindowHint
        )
        
        if ok:
            self.logic.change_amount_of_countable_items('custom', self.current_game, item_id, entered_amount)

        item = self.logic.get_current_item_by_id(self.current_game, item_id)
        new_amount = item[2]
        self.amount_labels[item_id].setText(f'{new_amount}')

    def on_remove_clicked(self, item_id):
        self.logic.delete_an_countable_items(self.current_game, item_id)
        self.refresh_ui()


    def show_item_context_menu(self, pos, item_id):
        menu = QMenu()

        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")

        action = menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

        if action == rename_action:

            entered_new_item_name, ok = QInputDialog.getText(
            self,  # родительское окно
            'New name',  # заголовок
            'Enter name',  # текст
            # 0,  # начальное значение
            # -9999999,  # минимум
            # 9999999  # максимум
            flags=Qt.WindowType.FramelessWindowHint
            )
            
            if ok:
                self.logic.rename_an_countable_items(self.current_game, item_id, entered_new_item_name)
                self.refresh_ui()

        elif action == delete_action:
            self.on_remove_clicked(item_id)

    def show_counter_selector(self):
        menu = QMenu(self)

        add_new_action = menu.addAction("➕ Add new")
        menu.addSeparator()

        items = self.logic.select_all_countable_items(self.current_game)

        action_map = {}

        for item in items:
            item_id = item[0]
            item_name = item[1]

            action = menu.addAction(item_name)
            action.setCheckable(True)

            if item_id == self.active_counter_id:
                action.setChecked(True)

            action_map[action] = item_id

        selected_action = menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

        if selected_action == add_new_action:
            new_item_name, ok = QInputDialog.getText(
            self,  # родительское окно
            'New name',  # заголовок
            'Enter name',  # текст
            # 0,  # начальное значение
            # -9999999,  # минимум
            # 9999999  # максимум
            flags=Qt.WindowType.FramelessWindowHint
            )
            
            if ok:
                new_id = self.logic.create_an_countable_items(self.current_game, new_item_name)
                print(new_id)
                self.switch_to_counter(new_id)

        elif selected_action in action_map:
            selected_id = action_map[selected_action]
            self.switch_to_counter(selected_id)


    def show_menu_selector(self):
        menu = QMenu()

        click_through_text = "✓ Клик-сквозь" if self.click_through else "Клик-сквозь"
        change_clickableness_action = menu.addAction(click_through_text)

        movable_text = "✓ Режим перемещения" if self.movable else "Режим перемещения"
        change_movebleness_action = menu.addAction(movable_text)

        kill_action = menu.addAction("Quit")

        action = menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

        if action == kill_action:
            self.kill_application()
        elif action == change_movebleness_action:
            self.change_movebleness()
        elif action == change_clickableness_action:
            self.change_clickableness()

    def switch_to_counter(self, item_id):
        self.active_counter_id = item_id
        self.refresh_ui()

