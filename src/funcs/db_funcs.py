import hashlib
import sqlite3

from funcs.command_funcs import parse_key_sequence


def hash_password(password):
    """Хеширует пароль с использованием SHA256."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def get_user(db_path, login, password):
    """Получает ID пользователя по логину и паролю (хешированному)."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        hashed_password = hash_password(password)  # Хешируем введенный пароль
        print(f"get_user вызван с login: {login}, hashed_password: {hashed_password}")  # Добавляем отладочный вывод
        cursor.execute("SELECT id FROM Users WHERE login = ? AND password = ?", (login, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            print(f"Пользователь найден с ID: {user[0]}")  # Добавляем отладочный вывод
            return user[0]
        else:
            print("Пользователь не найден.")  # Добавляем отладочный вывод
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса get_user: {e}")
        return None


def create_user(db_path, login, password):
    """Создает нового пользователя."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE login = ?", (login,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return False  # Пользователь существует
        hashed_password = hash_password(password)  # Хешируем пароль перед сохранением
        cursor.execute("INSERT INTO Users (login, password) VALUES (?, ?)", (login, hashed_password))
        conn.commit()
        conn.close()
        return True  # Пользователь успешно создан
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса create_user: {e}")
        return False


def save_user_gesture_binding(db_path, user_id, gesture_name, key_sequence):
    """
    Сохраняет связывание жеста для пользователя в базе данных.
    Args:
        db_path: Путь к базе данных.
        user_id: ID пользователя.
        gesture_name: Имя жеста (например, "ID: Pointer, Name: Pointer").
        key_sequence: Строка, представляющая клавишу или кнопку мыши (например, "Левая кнопка мыши", "1", "Ctrl+C").
    """
    print(
        f"Сохранение: user_id={user_id}, gesture_name={gesture_name}, key_sequence={key_sequence}")  # Отладочный вывод
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Определяем input_type, key_code и key_modifier на основе key_sequence
        input_type, key_code, key_modifier = parse_key_sequence(key_sequence)
        # Сначала удаляем существующую запись (чтобы избежать дубликатов)
        cursor.execute("""
            DELETE FROM UserGestureBindings
            WHERE user_id = ? AND gesture_id = ?
        """, (user_id, gesture_name))  # Используем gesture_name вместо gesture_id
        print(f"Удалено записей: {cursor.rowcount}")  # Проверяем сколько записей было удалено

        # Затем вставляем новую запись
        cursor.execute("""
            INSERT INTO UserGestureBindings (user_id, gesture_id, input_type, key_code, key_modifier)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, gesture_name, input_type, key_code, key_modifier))  # Используем gesture_name вместо gesture_id
        print(f"Вставлено записей: {cursor.rowcount}")  # Проверяем сколько записей было вставлено

        conn.commit()
        conn.close()
        print("Сохранение успешно!")  # Сообщение об успехе
    except sqlite3.Error as e:
        print(f"Ошибка при сохранении привязки жеста: {e}")


def get_user_gesture_bindings(db_path, user_id):
    """Loads gesture bindings for a user from the database."""
    gesture_key_map = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT gesture_id, input_type, key_code, key_modifier FROM UserGestureBindings WHERE user_id = ?",
            (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            gesture_id, input_type, key_code, key_modifier = row
            # Удаляем BOM из gesture_id
            gesture_id = gesture_id.lstrip('\ufeff')  # Удаляем BOM слева
            gesture_key_map[gesture_id] = {
                "input_type": input_type,
                "key_code": key_code,
                "key_modifier": key_modifier
            }
        conn.close()
        print(f"Связывания жестов загружены из базы данных для user_id={user_id}")
    except sqlite3.Error as e:
        print(f"Ошибка при загрузке связываний жестов: {e}")
    return gesture_key_map


def create_user_gesture_bindings_table(db_path):
    """Создает таблицу UserGestureBindings, если ее не существует."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserGestureBindings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                gesture_id TEXT NOT NULL,
                input_type TEXT NOT NULL,
                key_code INTEGER,
                key_modifier INTEGER
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы UserGestureBindings: {e}")


if __name__ == '__main__':
    db_path = "handsight.db"
    user_id = get_user(db_path, "test_user", "test_password")
    print(f"User ID: {user_id}")
