import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

def db_connect():
    # SQLite подключение
    dir_path = Path(__file__).parent
    db_path = dir_path / "database.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def init_db():
    """Инициализация базы данных с тестовыми данными"""
    conn, cur = db_connect()
    
    # Создание таблицы пользователей
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Создание таблицы книг
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            publisher TEXT NOT NULL,
            cover_image TEXT DEFAULT 'default_cover.jpg'
        )
    ''')
    
    # Создание администратора
    admin_password = generate_password_hash('admin123')
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ('admin', admin_password, True)
        )
    except sqlite3.IntegrityError:
        pass  # Админ уже существует
    
    # Добавление тестовых книг (минимум 100)
    books_count = cur.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if books_count == 0:
        sample_books = [
            ('Война и мир', 'Лев Толстой', 1225, 'АСТ', 'War_and_peace.jpg'),
            ('Преступление и наказание', 'Федор Достоевский', 671, 'Эксмо', 'Crime_and_punishment.jpg'),
            ('Мастер и Маргарита', 'Михаил Булгаков', 480, 'Азбука', 'Master_and_margaret.jpg'),
            ('Анна Каренина', 'Лев Толстой', 864, 'Фолио', 'Ann_Karenina.jpg'),
            ('Братья Карамазовы', 'Федор Достоевский', 824, 'Эксмо', 'Karamazov_brothers.jpg'),
            ('Отцы и дети', 'Иван Тургенев', 288, 'АСТ', 'Dads_and_sons.jpg'),
            ('Евгений Онегин', 'Александр Пушкин', 320, 'Фолио', 'Crime_and_punishment.jpg'),
            ('Герой нашего времени', 'Михаил Лермонтов', 224, 'Азбука', 'Evgeny_Onegin.jpg'),
            ('Мертвые души', 'Николай Гоголь', 352, 'Эксмо', 'Dead_souls.jpg'),
            ('Идиот', 'Федор Достоевский', 640, 'АСТ', 'Idiot.jpg'),
            ('Ревизор', 'Николай Гоголь', 160, 'АСТ', 'revizor.jpg'),
            ('Накануне', 'Иван Тургенев', 240, 'Азбука', 'eve.jpg'),
            ('Что делать?', 'Николай Чернышевский', 528, 'АСТ', 'what_to_do.jpg'),
            ('Обломов', 'Иван Гончаров', 480, 'Фолио', 'oblomov.jpg'),
            ('Собачье сердце', 'Михаил Булгаков', 192, 'Фолио', 'dog_heart.jpg'),
            ('Бесы', 'Федор Достоевский', 768, 'Эксмо', 'demons.jpg'),
            ('Гроза', 'Александр Островский', 128, 'Эксмо', 'thunderstorm.jpg'),
            ('Тихий Дон', 'Михаил Шолохов', 1504, 'Эксмо', 'quiet_don.jpg'),
            ('Поднятая целина', 'Михаил Шолохов', 672, 'Азбука', 'virgin_soil.jpg'),
            ('Доктор Живаго', 'Борис Пастернак', 592, 'Фолио', 'doctor_zhivago.jpg'),
            ('Белая гвардия', 'Михаил Булгаков', 352, 'АСТ', 'white_guard.jpg'),
            ('Двенадцать стульев', 'Ильф и Петров', 416, 'Эксмо', 'twelve_chairs.jpg'),
            ('Золотой теленок', 'Ильф и Петров', 384, 'Азбука', 'golden_calf.jpg'),
            ('Как закалялась сталь', 'Николай Островский', 416, 'Фолио', 'how_steel_tempered.jpg'),
        ]
        # Добавим еще книг чтобы было больше 100
        label = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(1, 101):
            sample_books.append(
                (f'Книга пример {i}', f'Автор {label[i%5]}', 200 + i * 10, f'Издательство {label[i%5]}', 'default_cover.jpg')
            )
        
        cur.executemany(
            "INSERT INTO books (title, author, pages, publisher, cover_image) VALUES (?, ?, ?, ?, ?)",
            sample_books
        )
    
    db_close(conn, cur)