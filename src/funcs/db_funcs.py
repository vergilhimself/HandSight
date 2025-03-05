import sqlite3
import hashlib
import json
import os


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def get_user(db_path, login, password):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Users WHERE login = ? AND password = ?", (login, password))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None  # Возвращаем id пользователя, если найден, иначе None
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса get_user: {e}")
        return None


def create_user(db_path, login, password):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE login = ?", (login,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return False  # Пользователь существует
        cursor.execute("INSERT INTO Users (login, password) VALUES (?, ?)", (login, password))
        conn.commit()
        conn.close()
        return True  # Пользователь успешно создан
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса create_user: {e}")
        return False


def add_new_custom_gesture(db_path, user_id, name, data, keyboard_shortcut):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Добавляем новый жест в таблицу Gestures
        cursor.execute(
            "INSERT INTO Gestures (user_id, name, data, keyboard_shortcut) VALUES (?, ?, ?, ?)",
            (user_id, name, data, keyboard_shortcut)
        )

        conn.commit()
        conn.close()
        return True  # Жест успешно добавлен
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса add_new_custom_gesture: {e}")
        return False


def get_user_gestures(db_path, user_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
            SELECT id, name, data, keyboard_shortcut
            FROM Gestures
            WHERE user_id = ?
        """

        cursor.execute(query, (user_id,))
        gestures = []
        for row in cursor.fetchall():
            gesture = {
                "id": row[0],
                "name": row[1],
                "data": row[2],
                "keyboard_shortcut": row[3]
            }
            gestures.append(gesture)
        conn.close()
        return gestures
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса get_user_gestures: {e}")
        return []


def remove_user_gesture(db_path, user_id, gesture_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Gestures WHERE id = ? AND user_id = ?",
            (gesture_id, user_id)
        )

        conn.commit()
        conn.close()
        return True  # Жест успешно удален
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса remove_user_gesture: {e}")
        return False


def update_keyboard_shortcut(db_path, gesture_id, user_id, keyboard_shortcut):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Gestures SET keyboard_shortcut = ? WHERE id = ? AND user_id = ?",
            (keyboard_shortcut, gesture_id, user_id)
        )

        conn.commit()
        conn.close()
        return True  # Клавиша успешно обновлена
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса update_keyboard_shortcut: {e}")
        return False
