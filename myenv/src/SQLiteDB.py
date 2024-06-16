import sqlite3
from typing import List, Tuple, Any, Optional


class SQLiteDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            emale TEXT,
            gender BOOL,
            age TEXT,
            company TEXT
        );
        """

        image_table = """
        CREATE TABLE IF NOT EXISTS image (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            imageCount INTEGER,
            imageSize INTEGER,
            request TEXT,
            answer TEXT,
            rate INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """

        self.execute_query(users_table)
        self.execute_query(image_table)

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = ()) -> None:
        """Выполняет запрос без возвращения результата (например, INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")

    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = ()) -> Optional[Tuple[Any, ...]]:
        """Выполняет запрос и возвращает одну запись."""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = ()) -> List[Tuple[Any, ...]]:
        """Выполняет запрос и возвращает все записи."""
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    def add_user(self, name: str, emale: str, gender: bool, age: str, company: str) -> None:
        query = """
        INSERT INTO users (name, emale, gender, age, company)
        VALUES (?, ?, ?, ?, ?)
        """
        self.execute_query(query, (name, emale, gender, age, company))

    def add_image(self, user_id: int, imageCount: int, imageSize: int, request: str, answer: str, rate: int) -> None:
        query = """
        INSERT INTO image (user_id, imageCount, imageSize, request, answer, rate)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (user_id, imageCount, imageSize, request, answer, rate))

    def find_images_by_user_id(self, user_id: int) -> List[Tuple[Any, ...]]:
        query = """
        SELECT users.id, users.name, users.emale, users.gender, users.age, users.company,
               image.id, image.imageCount, image.imageSize, image.request, image.answer, image.rate
        FROM users
        LEFT JOIN image ON users.id = image.user_id
        WHERE users.id = ?
        """
        return self.fetch_all(query, (user_id,))

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Ошибка закрытия соединения: {e}")

'''
# Пример использования класса
if __name__ == "__main__":
    db = SQLiteDB("example.db")

    # Добавление пользователей
    db.add_user("Alice", "emale1", True, "02/03/2005", "company1")
    db.add_user("Bob", "emale22", False, "17/10/1999", "company2")
    #print(db.fetch_all("SELECT * from users"))

    # Добавление изображений
    db.add_image(1, 10, 2048, "request1", "answer1", 5)
    db.add_image(1, 5, 1024, "request2", "answer2", 4)
    db.add_image(2, 7, 512, "request3", "answer3", 3)

    # Поиск изображений по user_id
    user_images = db.find_images_by_user_id(1)
    for user_image in user_images:
        print(user_image)

    db.close()
'''