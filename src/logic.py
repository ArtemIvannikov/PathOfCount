import os
import sqlite3
from sqlite3 import Error
import psutil

import config
import game_detector


class PathOfCounter():
    def __init__(self):
        pass

    def database_connect(self, path, game_name):
        self.database_connection = None
        try:
            self.database_connection = sqlite3.connect(config.PATH)
            print(1)
        except Error:
            print(f"111 '{Error}'")

        self.cursor = self.database_connection.cursor()

        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {game_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name VARCHAR NOT NULL DEFAULT 'item',
                amount INTEGER NOT NULL DEFAULT 0) 
            ''')

        self.database_connection.commit() 
        self.cursor.execute(f'''
            SELECT * FROM {game_name}
            ''')

        return self.cursor, self.database_connection



    def create_an_countable_items(self, game_name, new_item_name):
        if new_item_name == '':
            new_item_name = 'item'

        self.cursor.execute(f'''
            INSERT INTO {game_name} (item_name, amount)
            VALUES (?, 0)''', (new_item_name,))
        self.database_connection.commit()
        return self.cursor.lastrowid

    def delete_an_countable_items(self, game_name, item_id):
        self.cursor.execute(f'''
            DELETE FROM {game_name} 
            WHERE id = {item_id}''')
        self.database_connection.commit()

    def rename_an_countable_items(self, game_name, item_id, entered_new_item_name):
        if entered_new_item_name == '':
            entered_new_item_name = 'item'

        self.cursor.execute(f'''
            UPDATE {game_name}
            SET item_name = ? 
            WHERE id = ?''', (entered_new_item_name, item_id))
        self.database_connection.commit()

    def change_amount_of_countable_items(self, operation_type, game_name, item_id, entered_amount):
        match operation_type:
            case '+':
                self.cursor.execute(f'''
                    UPDATE {game_name}
                    SET amount = amount + {entered_amount}
                    WHERE id = {item_id}''')
                self.database_connection.commit()
            case '-':
                self.cursor.execute(f'''
                    UPDATE {game_name}
                    SET amount = amount - {entered_amount}
                    WHERE id = {item_id}''')
                self.database_connection.commit()
            case 'custom':
                self.cursor.execute(f'''
                    UPDATE {game_name}
                    SET amount = {entered_amount}
                    WHERE id = {item_id}''')
                self.database_connection.commit()

    def select_all_countable_items(self, game_name):
        return list(self.cursor.execute(f''' 
            SELECT * FROM {game_name}
            '''))

    def get_current_item_by_id(self, game_name, item_id):
        return self.cursor.execute(f'''
            SELECT * FROM {game_name} WHERE id = {item_id}
            ''').fetchone()


            
f = PathOfCounter()
f.database_connect(config.PATH, 'Poe')
# f.create_an_countable_items('Poe')
#f.change_amount_of_countable_items('custom', 'Poe', 3)
#f.delete_an_countable_items('Poe', 3)
#f.cursor.execute(f'''
#            SELECT * FROM 'Poe'
#            ''')
#rows = f.cursor.fetchall()
#rint(rows)

print(*f.select_all_countable_items('Poe'))
print(f.get_current_item_by_id('Poe', 4))