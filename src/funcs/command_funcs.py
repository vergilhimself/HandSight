import os
import csv
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QPoint

def load_standard_gestures():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "..", "model", "keypoint_classifier", "keypoint_classifier_label.csv")
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            gestures = [{"name": row[0]} for row in reader]  # id и name одинаковы
        return gestures
    except FileNotFoundError:
        QMessageBox.critical(None, "Ошибка", "Файл keypoint_classifier_label.csv не найден!")
        return []
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при чтении keypoint_classifier_label.csv: {e}!")
        return []

def parse_key_sequence(key_sequence):
    """
    Разбирает строку key_sequence и возвращает input_type, key_code и key_modifier.
    """
    if key_sequence == "Левая кнопка мыши":
        return "mouse", Qt.LeftButton, 0
    elif key_sequence == "Правая кнопка мыши":
        return "mouse", Qt.RightButton, 0
    elif key_sequence == "Средняя кнопка мыши":
        return "mouse", Qt.MiddleButton, 0
    else:  # Предполагаем, что это клавиша или комбинация клавиш
        input_type = "keyboard"
        key_code = 0  # Значение по умолчанию, будет переопределено
        key_modifier = 0

        keys = key_sequence.split('+')
        if len(keys) > 1:  # Есть модификаторы
            for key in keys[:-1]:  # Исключаем последнюю клавишу (она будет key_code)
                if key.lower() == "ctrl":
                    key_modifier |= Qt.ControlModifier
                elif key.lower() == "shift":
                    key_modifier |= Qt.ShiftModifier
                elif key.lower() == "alt":
                    key_modifier |= Qt.AltModifier

            # Получаем key_code для последней клавиши
            key_code = getattr(Qt, f"Key_{keys[-1]}", 0) # Получаем код клавиши из Qt.Key_*
            if key_code == 0:
                # Если не найдено соответствие Qt.Key, пробуем просто взять первый символ
                key_code = ord(keys[-1][0]) if keys[-1] else 0  # Получаем код первого символа
        else:
            # Просто клавиша без модификаторов
             key_code = getattr(Qt, f"Key_{key_sequence}", 0) # Получаем код клавиши из Qt.Key_*
             if key_code == 0:
                # Если не найдено соответствие Qt.Key, пробуем просто взять первый символ
                key_code = ord(key_sequence[0]) if key_sequence else 0  # Получаем код первого символа


        return input_type, key_code, key_modifier

