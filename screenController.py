import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import pyautogui as pg
import virtual_keyboard
import tkinter as tk
import threading
import queue

# Screen size and PyAutoGUI setup
screen_width, screen_height = pg.size()
pg.FAILSAFE = False
window_position = [0, 0]

# Queue for click events from video thread to main thread
click_queue = queue.Queue()

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Drawing specifications
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
RIGHT_IRIS = [474, 475, 476, 477]

def distance(landmark1, landmark2):
    return np.sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)

#counting the fingers that are up
def count_fingers(hand_landmarks):
    tip_ids = [4,8,12,16,20]
    fingers = []
    fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    for ids in range(1,5):
        if hand_landmarks.landmark[tip_ids[ids]].y < hand_landmarks.landmark[tip_ids[ids]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers.count(1)

# Initialize variables
def video_capture():
    global running
    cap = cv.VideoCapture(0)
    delay = 0.5
    last_action_time = 0
    last_blink_time = 0
    pinch_drag_threshold = 0.5
    double_click_threshold = 0.3
    last_click_time = 0
    is_dragging = False
    neutral_x, neutral_y = None, None
    gain = 1.75
    smooth = 0.3
    prev_x, prev_y = screen_width // 2, screen_height // 2
    calibration_frames = 30
    calibration_count = 0
    neutral_samples = []
    cursor_enabled = True
    pinch_start_time = None

    while running:
        success, image = cap.read()
        if not success:
            print("Failed to read from camera.")
            break
        image = cv.flip(image, 1)
        image = cv.resize(image, (screen_width, screen_height))
        img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        hand_result = hands.process(img_rgb)
        face_result = face_mesh.process(img_rgb)
        current_time = time.time()

        # Calibrate neutral position
        if face_result.multi_face_landmarks and calibration_count < calibration_frames:
            for face_landmarks in face_result.multi_face_landmarks:
                iris = face_landmarks.landmark[RIGHT_IRIS[0]]
                neutral_samples.append((iris.x, iris.y))
                calibration_count += 1
                if calibration_count == calibration_frames:
                    neutral_x = sum(x for x, _ in neutral_samples) / calibration_frames
                    neutral_y = sum(y for _, y in neutral_samples) / calibration_frames

        # Face-based cursor control
        if face_result.multi_face_landmarks and neutral_x is not None:
            for face_landmarks in face_result.multi_face_landmarks:
                eye_distance = distance(face_landmarks.landmark[159], face_landmarks.landmark[145])  # Distance between eyes
                if eye_distance < 0.01 and current_time - last_blink_time > 0.3:
                    cursor_enabled = not cursor_enabled  # Toggle cursor state
                    last_blink_time = current_time
                    
                if cursor_enabled:
                    iris = face_landmarks.landmark[RIGHT_IRIS[0]]
                    # Draw iris for debugging
                    iris_x, iris_y = int(iris.x * screen_width), int(iris.y * screen_height)
                    cv.circle(image, (iris_x, iris_y), 5, (0, 255, 0), -1)

                    delta_x = (iris.x - neutral_x) * gain
                    delta_y = (iris.y - neutral_y) * gain

                    # Calculate target cursor position
                    target_x = int(prev_x + delta_x * screen_width)
                    target_y = int(prev_y + delta_y * screen_height)

                    # Bound to screen edges
                    target_x = np.clip(target_x, 0, screen_width - 2)
                    target_y = np.clip(target_y, 0, screen_height - 1)

                    # Smooth movement
                    curr_x = prev_x + (target_x - prev_x) * smooth
                    curr_y = prev_y + (target_y - prev_y) * smooth

                    # Move cursor
                    pg.moveTo(curr_x, curr_y, duration=0)
                    prev_x, prev_y = curr_x, curr_y

        # Hand-based click detection
        if hand_result.multi_hand_landmarks:
            for hand_landmarks in hand_result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                pinch_dist = distance(thumb_tip, index_tip)
                count = count_fingers(hand_landmarks)
                
                if count == 2 and pinch_dist > 0.17 and current_time - last_action_time > delay:
                    pg.keyDown('ctrl')
                    pg.press('-')
                    pg.keyUp('ctrl')
                    
                if count == 4 and pinch_dist > 0.17 and current_time - last_action_time > delay:
                    pg.keyDown('ctrl')
                    pg.press('+')
                    pg.keyUp('ctrl')

                if pinch_dist < 0.05 and current_time - last_action_time > delay:
                    if pinch_start_time is None:
                        pinch_start_time = current_time
                        drag_start_x, drag_start_y = curr_x, curr_y
                        drag_prev_x, drag_prev_y = curr_x, curr_y
                elif pinch_dist >= 0.07 and pinch_start_time is not None:
                    pinch_duration = current_time - pinch_start_time
                    if is_dragging:
                        pg.mouseUp()  # End drag
                        is_dragging = False
                    elif pinch_duration <= pinch_drag_threshold:
                        # Double click logic
                        if current_time - last_click_time < double_click_threshold:
                            pg.doubleClick()
                            last_click_time = 0  # Reset to avoid triple click
                        else:
                            click_queue.put((curr_x, curr_y))
                            last_click_time = current_time
                    pinch_start_time = None
                    last_action_time = current_time
                    
                # Drag logic
                if pinch_start_time is not None:
                    pinch_duration = current_time - pinch_start_time
                    if pinch_duration > pinch_drag_threshold and not is_dragging:
                        pg.mouseDown()  # Start drag
                        is_dragging = True
                    if is_dragging:
                        # Move mouse while dragging
                        pg.moveTo(curr_x, curr_y, duration=0)
                        drag_prev_x, drag_prev_y = curr_x, curr_y
                        
                #Right Click Logic
                if distance(thumb_tip, middle_tip) < 0.08 and current_time - last_action_time > delay and pinch_dist >= 0.1:
                    pg.rightClick()
                    last_action_time = current_time

        # Display the image
        cv.imshow("Gesture Based Controller", image)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            running = False
            break

    cap.release()
    cv.destroyAllWindows()

# Global flag to control both loops
running = True

# Start video loop in a separate thread
video_thread = threading.Thread(target=video_capture)
video_thread.daemon = True
video_thread.start()

# Tkinter update loop
while running:
    try:
        virtual_keyboard.root.update()  # Process Tkinter events
        window_position[0], window_position[1] = virtual_keyboard.root.winfo_x(), virtual_keyboard.root.winfo_y()
        # Process click events from the queue
        while not click_queue.empty():
            x, y = click_queue.get()
            widget = virtual_keyboard.root.winfo_containing(x, y)
            if widget and isinstance(widget, tk.Button) and widget.winfo_toplevel() == virtual_keyboard.root:
                widget.invoke()
            else:
                pg.click()
        time.sleep(0.01)  # Prevent high CPU usage
    except:
        running = False  # Exit on Tkinter window close
        break

virtual_keyboard.root.quit()
virtual_keyboard.root.destroy()