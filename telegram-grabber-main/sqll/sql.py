import sqlite3


class SQL:
    def __init__(self, database):
        """Подключение к БД"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table_config()
        self.create_table_database()

    def create_table_config(self):
        """Создание таблицы для хранения каналов"""
        with self.connection:
            return self.cursor.execute("CREATE TABLE IF NOT EXISTS config ('donor', 'moder', 'channel')")

    def create_table_database(self):
        """Создание таблицы для хранения информации о постах"""
        with self.connection:
            return self.cursor.execute("CREATE TABLE IF NOT EXISTS DataBase ('username', 'message_id')")

    def message_id_exists(self, username, message_id: int):
        """Проверка есть ли message_id в БД"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM DataBase WHERE username=? AND message_id=?",
                                        (username, message_id,)).fetchall()
            return bool(len(result))

    def add_message_id(self, username, message_id):
        """Добавление message_id"""
        with self.connection:
            return self.cursor.execute("INSERT INTO DataBase VALUES (?,?)", (username, message_id))

    def get_last_rowid(self):
        """Получение последнего ROWID"""
        with self.connection:
            return self.cursor.execute("SELECT ROWID, * FROM DataBase LIMIT 1 OFFSET (SELECT COUNT(*) FROM DataBase)-1")

    def get_data_in_table(self, message):
        
        """Получение записи о посте в таблице"""
        with self.connection:
        
            return self.cursor.execute(f"SELECT * FROM DataBase WHERE ROWID = {message.text}")

    def get_text(self, message):
        
        """Получение записи о посте в таблице"""
        with self.connection:
        
            return self.cursor.execute({message.text})

    def add_donor(self, name: str):
        """Добавление канала донора"""
        with self.connection:
            # Проверка на наличие записи такого канала
            result = self.cursor.execute("SELECT donor FROM config WHERE donor=?", (name,)).fetchall()
            if not bool(len(result)):
                self.cursor.execute("INSERT INTO config (donor) VALUES (?)", (name,))
                return f'Запись {name} добавлена.'
            return f'Запись {name} существует.'

    def delete_donor(self, name: str):
        """Удаление канала донора"""
        with self.connection:
            # Проверка на наличие записи такого канала
            result = self.cursor.execute("SELECT donor FROM config WHERE donor = ?", (name,)).fetchall()
            if not bool(len(result)):
                return f'Запись {name} не найдена.'
            else:
                self.cursor.execute("DELETE FROM config WHERE donor = ?", (name,))
                return f'Запись {name} удалена.'

    def add_moder(self, name: str):
        """Добавление канала модерации"""
        with self.connection:
            # Проверка на наличие записи такого канала
            result = self.cursor.execute("SELECT moder FROM config WHERE moder=?", (name,)).fetchall()
            if not bool(len(result)):
                self.cursor.execute("INSERT INTO config (moder) VALUES (?)", (name,))
                return f'Запись {name} добавлена.'
            return f'Запись {name} существует.'

    def delete_moder(self, name: str):
        """Удаление модера"""
        with self.connection:
            # Проверка на наличие записи такого канала
            result = self.cursor.execute("SELECT moder FROM config WHERE moder = ?", (name,)).fetchall()
            if not bool(len(result)):
                return f'Запись {name} не найдена.'
            else:
                self.cursor.execute("DELETE FROM config WHERE moder = ?", (name,))
                return f'Запись {name} удалена.'

    def add_channel(self, name: str):
        """Добавление основного канала"""
        with self.connection:
            # Проверка на наличие записи такого канала
            result = self.cursor.execute("SELECT channel FROM config WHERE channel=?", (name,)).fetchall()
            if not bool(len(result)):
                self.cursor.execute("INSERT INTO config (channel) VALUES (?)", (name,))
                return f'Запись {name} добавлена.'
            return f'Запись {name} существует.'

    def delete_channel(self, name: str):
        """Удаление основного канала"""
        with self.connection:
            # Проверка на наличие записи такого канала
            result = self.cursor.execute("SELECT channel FROM config WHERE channel = ?", (name,)).fetchall()
            if not bool(len(result)):
                return f'Запись {name} не найдена.'
            else:
                self.cursor.execute("DELETE FROM config WHERE channel = ?", (name,))
                return f'Запись {name} удалена.'

    def get_donor(self):
        """Возвращает список с каналами донорами"""
        with self.connection:
            donor_list = []
            result = self.cursor.execute("SELECT donor FROM config").fetchall()
            for donor in result:
                if donor[0] is None:
                    pass
                else:
                    donor_list.append(donor[0])
            return donor_list

    def get_moder(self):
        """Возвращает канал модерации"""
        with self.connection:
            moder = None
            result = self.cursor.execute("SELECT moder FROM config").fetchall()
            for i in result:
                if i[0] is None:
                    pass
                else:
                    moder = i[0]
            return moder

    def get_channel(self):
        """Возвращает основной канал"""
        with self.connection:
            result = self.cursor.execute("SELECT channel FROM config").fetchall()
            for i in result:
                if i[0] is None:
                    pass
                else:
                    channel = i[0]
            return channel

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
