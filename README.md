# Hand Controller

## Preview
<img src="https://raw.githubusercontent.com/BenjaminBurnell/Hand-Controller/refs/heads/main/assets/ezgif-4fd1b8759ca1fc.gif"></img>

## Overview

**Hand Controller** is a computer vision project that allows you to **control your mouse cursor using your hand and fingers** through your webcam. It uses **MediaPipe Hands** for real-time hand and finger landmark detection, combined with **OpenCV** for video capture and **PyAutoGUI** for precise cursor and click control.

This project demonstrates how computer vision can bridge human movement and computer interaction—effectively turning your camera into a virtual touchpad.

---

## Features

- **Real-Time Hand Tracking** — Uses **MediaPipe Hands** to detect 21 key landmarks on your hand.
- **Cursor Control** — Moves your mouse cursor based on the position of your **index finger** or **thumb**.
- **Click Detection** — Detects a click when the **thumb and index finger touch**, and holds/release dynamically.
- **Camera Border Scaling** — Allows for movement to the edges of the monitor without leaving the camera frame.
- **Smooth Cursor Mapping** — Maps camera coordinates to screen space for accurate and responsive control.
- **Multi-Monitor Support** — Automatically reads connected monitor dimensions.
- **Adjustable FPS & Borders** — Optimized for better frame rates and flexible tracking zones.

---

## How It Works

1. **Camera Feed (OpenCV)**  
   Captures live video frames and flips them horizontally for a natural mirrored view.

2. **Hand Landmark Detection (MediaPipe)**  
   Detects 21 landmarks per hand, including fingertips, joints, and wrist coordinates.

3. **Cursor Mapping**  
   Translates the detected finger coordinates from the camera frame to monitor resolution, adjusting for borders.

4. **Click Logic**  
   When the thumb and index fingertip come close together, a **mouseDown()** event is triggered; separating them releases the click.

5. **Real-Time Updates**  
   Runs continuously, giving instant feedback as you move or click.

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/BenjaminBurnell/Hand-Controller
cd Hand-Controller
```

### 2. Create a virtual environment
```bash
python -m venv hand-controller-environment
source hand-controller-environment/bin/activate   # Windows: hand-controller-environment\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the program
```bash
python main.py
```

Your webcam will open, and your hand should control the cursor movement.

> **Tip:** Ensure your environment has good lighting for best hand-tracking accuracy.

---

## Built With

- **Python 3.x** — Core programming language.
- **OpenCV (`cv2`)** — For webcam access and frame processing.
- **MediaPipe** — For high-precision real-time hand and finger tracking.
- **PyAutoGUI** — For mouse cursor and click simulation.
- **ScreenInfo** — For detecting monitor dimensions and multi-display setups.

---

## Future Enhancements

- Implement **gesture-based commands** (scroll, drag, right-click).
- Add **on-screen UI feedback** (cursor trail, click visualizations).
- Introduce **configurable sensitivity** for smoother cursor motion.
- Add **multi-hand support** (one for cursor, one for gestures).
- Optimize for **higher FPS** and **GPU acceleration**.

---

## License

MIT License © 2025 **Benjamin Burnell**

You are free to use, modify, and distribute this project under the terms of the MIT License.

---

## Credits

Developed by **Benjamin Burnell**  
Powered by **MediaPipe**, **OpenCV**, and **PyAutoGUI**.

