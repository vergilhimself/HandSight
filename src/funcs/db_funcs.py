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
        cursor.execute("SELECT * FROM MainTable WHERE login = ? AND password = ?", (login, password))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
         print(f"Ошибка при выполнении запроса get_user: {e}")
         return None


def create_user(db_path, login, password):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MainTable WHERE login = ?", (login,))
        existing_user = cursor.fetchone()
        if existing_user:
             conn.close()
             return False # Пользователь существует
        cursor.execute("INSERT INTO MainTable (login, password, gestures) VALUES (?, ?, ?)", (login, password, "[]"))
        conn.commit()
        conn.close()
        return True # Пользователь успешно создан
    except sqlite3.Error as e:
       print(f"Ошибка при выполнении запроса create_user: {e}")
       return False


def get_user_gestures(db_path, login):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT gestures FROM MainTable WHERE login = ?", (login,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
           return json.loads(result[0])
        else:
           return []
    except sqlite3.Error as e:
       print(f"Ошибка при выполнении запроса get_user_gestures: {e}")
       return []


def save_user_gestures(db_path, login, gestures):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        gestures_json = json.dumps(gestures)
        cursor.execute("UPDATE MainTable SET gestures = ? WHERE login = ?", (gestures_json, login))
        conn.commit()
        conn.close()
        return True # жесты успешно сохранены
    except sqlite3.Error as e:
      print(f"Ошибка при выполнении запроса save_user_gestures: {e}")
      return False