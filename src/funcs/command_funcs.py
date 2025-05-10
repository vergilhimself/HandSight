import os
import csv
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import  QKeySequence
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

def parse_key_sequence(sequence_str):
    # ... (начало функции без изменений) ...
    # print(f"--- parse_key_sequence CALLED with: '{sequence_str}' ---")

    if not sequence_str:
        # print("parse_key_sequence: sequence_str is empty")
        return 'keyboard', None, int(Qt.NoModifier)  # Явно приводим к int

    if sequence_str == "Левая кнопка мыши":
        # print("parse_key_sequence: Matched 'Левая кнопка мыши'")
        return 'mouse', int(Qt.LeftButton), int(Qt.NoModifier)  # Явно приводим к int
    # ... (остальные кнопки мыши так же) ...
    if sequence_str == "Правая кнопка мыши":
        return 'mouse', int(Qt.RightButton), int(Qt.NoModifier)
    if sequence_str == "Средняя кнопка мыши":
        return 'mouse', int(Qt.MiddleButton), int(Qt.NoModifier)

    input_type = "keyboard"
    qt_key_code = None
    qt_modifiers_val = Qt.NoModifier  # Инициализируем как int

    parts = sequence_str.split('+')
    cleaned_parts = [part.strip() for part in parts]
    main_key_str = cleaned_parts[-1]

    for mod_str in cleaned_parts[:-1]:
        if mod_str.lower() == "ctrl":
            qt_modifiers_val |= Qt.ControlModifier
        elif mod_str.lower() == "shift":
            qt_modifiers_val |= Qt.ShiftModifier
        elif mod_str.lower() == "alt":
            qt_modifiers_val |= Qt.AltModifier

    qks_single_key = QKeySequence.fromString(main_key_str, QKeySequence.PortableText)
    if not qks_single_key.isEmpty() and qks_single_key.count() > 0:
        key_int_from_qks = qks_single_key[0]
        potential_key = key_int_from_qks & ~Qt.KeyboardModifierMask
        if potential_key != Qt.Key_unknown and potential_key != 0:
            qt_key_code = potential_key
    elif len(main_key_str) == 1 and main_key_str.isalnum():
        qt_key_code = Qt.Key(ord(main_key_str.upper()))
    else:
        qt_key_code_attr = getattr(Qt, f"Key_{main_key_str.replace(' ', '')}", None)
        if qt_key_code_attr is not None:
            qt_key_code = qt_key_code_attr
    # ... (конец определения qt_key_code)

    if qt_key_code is None or qt_key_code == 0 or qt_key_code == Qt.Key_unknown:
        print(
            f"parse_key_sequence: FAILED to determine main key_code for '{main_key_str}' from sequence '{sequence_str}'")
        return input_type, None, int(qt_modifiers_val)  # Возвращаем int

    # Убедимся, что qt_key_code тоже int
    final_key_code = int(qt_key_code)
    final_modifiers = int(qt_modifiers_val)

    print(
        f"parse_key_sequence: Parsed SUCCESS: '{sequence_str}' -> key={final_key_code} (Qt.Key_0x{final_key_code:X}), modifiers={final_modifiers} (Qt.KeyboardModifier_0x{final_modifiers:X})")
    return input_type, final_key_code, final_modifiers

