import copy
import csv
import itertools
import threading
import mediapipe as mp
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import pyautogui
from PyQt5.QtCore import pyqtSignal, QObject, Qt

from model import KeyPointClassifier
from model import PointHistoryClassifier
from utils import CvFpsCalc

class VideoProcessor(QObject):
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, device=0, width=960, height=540, use_static_image_mode=False, min_detection_confidence=0.7,
                 min_tracking_confidence=0.5, gesture_key_map=None):
        super().__init__()
        self.cap_device = device
        self.cap_width = width
        self.cap_height = height
        self.use_static_image_mode = use_static_image_mode
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.use_brect = True
        self.running = False
        self.mode = 0
        self.number = -1
        self.fps = 0
        self.previous_gesture = None
        # Model and Label loading
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.use_static_image_mode,
            max_num_hands=1,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        self.keypoint_classifier = KeyPointClassifier()
        self.point_history_classifier = PointHistoryClassifier()

        # Read labels
        try:
            with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                      encoding='utf-8-sig') as f:  # Используем utf-8-sig
                reader = csv.reader(f)
                self.keypoint_classifier_labels = [row[0].strip() for row in reader]  # Удаляем BOM и пробелы
        except FileNotFoundError:
            print("Error: keypoint_classifier_label.csv not found.")
            self.keypoint_classifier_labels = []

        print(f"self.keypoint_classifier_labels: {self.keypoint_classifier_labels}")  # Отладочный вывод

        try:
            with open(
                    'model/point_history_classifier/point_history_classifier_label.csv',
                    encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                self.point_history_classifier_labels = [row[0] for row in
                                                        reader]
        except FileNotFoundError:
            print("Error: point_history_classifier_label.csv not found.")
            self.point_history_classifier_labels = []

        self.cvFpsCalc = CvFpsCalc(buffer_len=10)

        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)

        self.finger_gesture_history = deque(maxlen=self.history_length)

        self.gesture_key_map = gesture_key_map if gesture_key_map else {}

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False

    def _run(self):
        cap = cv.VideoCapture(self.cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        mode = 0
        number = -1

        while self.running:
            self.fps = self.cvFpsCalc.get()

            # Camera capture
            ret, image = cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if results.multi_hand_landmarks is not None:

                for hand_landmarks, handedness in zip(
                        results.multi_hand_landmarks, results.multi_handedness):
                    # Bounding box calculation
                    brect = self.calc_bounding_rect(debug_image,
                                                    hand_landmarks)
                    # Landmark calculation
                    landmark_list = self.calc_landmark_list(debug_image,
                                                            hand_landmarks)

                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = self.pre_process_landmark(
                        landmark_list)
                    pre_processed_point_history_list = self.pre_process_point_history(
                        debug_image, self.point_history)  # Use self.point_history
                    # Write to the dataset file
                    self.logging_csv(number, mode, pre_processed_landmark_list, pre_processed_point_history_list)

                    # Hand sign classification
                    hand_sign_id = self.keypoint_classifier(
                        pre_processed_landmark_list)
                    if hand_sign_id == "point_history_class":  # Point gesture
                        self.point_history.append(landmark_list[8])  # Append to self.point_history
                    else:
                        self.point_history.append([0, 0])  # Append to self.point_history

                    # Finger gesture classification
                    finger_gesture_id = 0
                    point_history_len = len(
                        pre_processed_point_history_list)
                    if point_history_len == (self.history_length * 2):
                        finger_gesture_id = self.point_history_classifier(
                            pre_processed_point_history_list)

                    # Calculates the gesture IDs in the latest detection
                    self.finger_gesture_history.append(finger_gesture_id)
                    most_common_fg_id = Counter(
                        self.finger_gesture_history).most_common()

                    # Get gesture names
                    try:
                        hand_sign_text = self.keypoint_classifier_labels[
                            hand_sign_id].strip()
                        finger_gesture_text = self.point_history_classifier_labels[
                            most_common_fg_id[0][
                                0]] if self.point_history_classifier_labels and most_common_fg_id and 0 <= \
                                       most_common_fg_id[0][
                                           0] < len(self.point_history_classifier_labels) else "Unknown"
                    except IndexError as e:
                        print(
                            f"IndexError: {e}. Check classifier outputs and label files.")
                        hand_sign_text = "Error"
                        finger_gesture_text = "Error"

                    # Drawing part
                    debug_image = self.draw_bounding_rect(self.use_brect,
                                                          debug_image, brect)
                    debug_image = self.draw_landmarks(debug_image,
                                                      landmark_list)
                    debug_image = self.draw_info_text(
                        debug_image,
                        brect,
                        handedness,
                        hand_sign_text,
                        finger_gesture_text,

                    )

                    # Emulate keypress                   
                    if hand_sign_text != self.previous_gesture:
                        self.emulate_keypress(hand_sign_text)
                        self.previous_gesture = hand_sign_text

            else:
                self.point_history.append([0, 0])
                self.previous_gesture = None
            debug_image = self.draw_point_history(debug_image, self.point_history)
            debug_image = self.draw_info(debug_image, self.fps)

            # Screen reflection
            self.frame_ready.emit(debug_image)

    def emulate_keypress(self, hand_sign_text):
        clean_hand_sign_text = hand_sign_text.lstrip('\ufeff')

        print(f"\n--- Попытка эмуляции для жеста: '{clean_hand_sign_text}' ---")

        # self.gesture_key_map теперь содержит данные в новом формате
        if clean_hand_sign_text in self.gesture_key_map:
            binding_info = self.gesture_key_map[clean_hand_sign_text]
            input_type = binding_info.get("input_type")
            binding_str = binding_info.get("binding_str")

            if not input_type or not binding_str:
                print(f"Ошибка: Неполная информация о привязке для жеста '{clean_hand_sign_text}': {binding_info}")
                return

            print(f"Найдено действие: Тип='{input_type}', Привязка='{binding_str}'")

            try:
                if input_type == 'keyboard':
                    # 1. Разбираем строку и приводим к нижнему регистру
                    keys_to_press = [key.strip().lower() for key in binding_str.split('+')]
                    print(f"Клавиши для pyautogui: {keys_to_press}")

                    # 2. Проверяем, что список не пуст
                    if not keys_to_press:
                        print("Ошибка: после разбора строки не осталось клавиш для нажатия.")
                        return

                    # --- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ ---
                    # 3. Разделяем логику в зависимости от количества клавиш
                    if len(keys_to_press) == 1:
                        # Если клавиша одна (например, 'a', 'enter', 'f5')
                        key_to_press = keys_to_press[0]
                        print(f"Эмуляция одиночного нажатия: pyautogui.press('{key_to_press}')")
                        pyautogui.press(key_to_press)
                    else:
                        # Если клавиш несколько (комбинация, например, ['ctrl', 'a'])
                        print(
                            f"Эмуляция комбинации клавиш: pyautogui.hotkey({', '.join(repr(k) for k in keys_to_press)})")
                        pyautogui.hotkey(*keys_to_press)


                    print("Эмуляция клавиатуры выполнена успешно.")

                elif input_type == 'mouse':
                    action = binding_str.lower()
                    print(f"Эмуляция действия мыши: '{action}'")

                    if 'левая кнопка' in action:
                        pyautogui.click(button='left')
                    elif 'правая кнопка' in action:
                        pyautogui.click(button='right')
                    elif 'средняя кнопка' in action:
                        pyautogui.click(button='middle')
                    else:
                        print(f"Неизвестное действие мыши: '{binding_str}'")

                else:
                    print(f"Неизвестный тип ввода: '{input_type}'")

            except Exception as e:
                print(f"КРИТИЧЕСКАЯ ОШИБКА во время эмуляции: {e}")
        else:
            print(f"Для жеста '{clean_hand_sign_text}' действие не назначено.")

    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point,
                                       axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def pre_process_point_history(self, image, point_history):
        image_width, image_height = image.shape[1], image.shape[0]

        temp_point_history = copy.deepcopy(point_history)

        base_x, base_y = 0, 0
        for index, point in enumerate(temp_point_history):
            if index == 0:
                base_x, base_y = point[0], point[1]

            temp_point_history[index][0] = (temp_point_history[index][0] -
                                            base_x) / image_width
            temp_point_history[index][1] = (temp_point_history[index][1] -
                                            base_y) / image_height

        temp_point_history = list(
            itertools.chain.from_iterable(temp_point_history))

        return temp_point_history

    def logging_csv(self, number, mode, landmark_list, point_history_list):
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 9):
            csv_path = 'model/keypoint_classifier/keypoint.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        if mode == 2 and (0 <= number <= 9):
            csv_path = 'model/point_history_classifier/point_history.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *point_history_list])
        return

    def draw_landmarks(self, image, landmark_point):
        if len(landmark_point) > 0:
            # Thumb
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (255, 255, 255), 2)

            # Index finger
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (255, 255, 255), 2)

            # Middle finger
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (255, 255, 255), 2)

            # Ring finger
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (255, 255, 255), 2)

            # Little finger
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (255, 255, 255), 2)

            # Palm
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (255, 255, 255), 2)

        # Key Points
        for index, landmark in enumerate(landmark_point):
            if index == 0:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 1:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 2:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 3:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 4:
                cv.circle(image, (landmark[0], landmark[1]), 8,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 5:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 6:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 7:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 8:
                cv.circle(image, (landmark[0], landmark[1]), 8,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 9:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 10:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 11:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 12:
                cv.circle(image, (landmark[0], landmark[1]), 8,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 13:  # 薬指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 14:  # 薬指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 15:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 16:
                cv.circle(image, (landmark[0], landmark[1]), 8,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 17:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 18:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 19:
                cv.circle(image, (landmark[0], landmark[1]), 5,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 20:
                cv.circle(image, (landmark[0], landmark[1]), 8,
                          (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        return image

    def draw_bounding_rect(self, use_brect, image, brect):
        if use_brect:
            # Outer rectangle
            cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                         (0, 0, 0), 1)

        return image

    def draw_info_text(self, image, brect, handedness, hand_sign_text,
                       finger_gesture_text, key_to_press=""):
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                     (0, 0, 0), -1)

        info_text = handedness.classification[0].label[0:]
        if hand_sign_text != "":
            info_text = info_text + ':' + hand_sign_text
        if key_to_press:
            info_text = info_text + f" (Клавиша: {key_to_press})"

        cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                   cv.LINE_AA)

        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                   cv.LINE_AA)

        return image

    def draw_point_history(self, image, point_history):
        for index, point in enumerate(point_history):
            if point[0] != 0 and point[1] != 0:
                cv.circle(image, (point[0], point[1]), 1 + int(index / 2),
                          (152, 251, 152), 2)
        return image

    def draw_info(self, image, fps):
        cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                   1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                   1.0, (255, 255, 255), 2, cv.LINE_AA)
        return image


if __name__ == '__main__':
    processor = VideoProcessor()
    processor.start()
