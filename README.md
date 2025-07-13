# Hands-free Smart Screen Controller
This project enables **hands-free control** of your Windows PC using **eye gaze** (for cursor movement) and **hand gestures** (for mouse clicks, drag, double-click, right-click, and virtual keyboard input) via your webcam. It combines [MediaPipe](https://google.github.io/mediapipe/) for face and hand tracking, [PyAutoGUI](https://pyautogui.readthedocs.io/) for system control, and a custom Tkinter-based virtual keyboard.

---

## Features

- **Gaze Tracking:** Move the mouse cursor using your eye gaze.
- **Blink to Toggle:** Enable/disable gaze cursor with a blink.
- **Pinch Gesture:** 
  - Single pinch for left click.
  - Quick double pinch for double-click.
  - Long pinch for drag (hold and move).
- **Right Click:** Pinch thumb and middle finger together while index is away.
- **Zoom In/Out:** Four fingers up for zoom in, two for zoom out (Ctrl + '+'/'-').
- **Virtual Keyboard:** On-screen keyboard with support for Shift, Ctrl, Alt, and other keys.
- **Modifier Keys:** Hold Shift/Ctrl/Alt, then press another key for combinations (e.g., Ctrl+C).

---

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- MediaPipe
- PyAutoGUI
- Tkinter (usually included with Python)
- Numpy

Install dependencies:
```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

## Usage

- **Move Cursor:** Look at the screen; your gaze moves the cursor.
- **Enable/Disable Cursor:** Blink to toggle.
- **Left Click:** Pinch thumb and index finger quickly.
- **Double Click:** Two quick pinches.
- **Drag:** Pinch and hold, then move your hand.
- **Right Click:** Pinch thumb and middle finger together, index finger away.
- **Zoom:** Show 2 or 4 fingers and pinch out.
- **Virtual Keyboard:** Use mouse or pinch to click keys. Hold Shift/Ctrl/Alt, then press another key for combos.

---

## Notes

- **Accuracy:** Good lighting and a clear webcam view improve performance.
- **Focus:** The virtual keyboard window is always on top and semi-transparent.
- **No window borders:** The keyboard window is borderless for accessibility.
- **Platform:** Designed for Windows, but may work on other OSes with minor tweaks.

---

## 📦 Installation

```bash
git clone https://github.com/sam-1409/Screen_controller.git
cd screenController
pip install -r requirements.txt
---
