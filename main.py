from screeninfo import get_monitors
import pyautogui

import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,      # For video input
    max_num_hands=2,              # Track up to two hands
    min_detection_confidence=0.5, # Detection threshold
    min_tracking_confidence=0.5
)

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally (like a mirror)
    frame = cv2.flip(frame, 1)

    # Convert to RGB (MediaPipe requires RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    result = hands.process(rgb_frame)

    # Draw landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
            )

            # Get coordinates of the index fingertip (landmark 8)
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
            cv2.putText(frame, f"Index Tip: ({x}, {y})", (x+10, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Hand Tracker", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()


def get_camera():
    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame (so movement feels natural)
        frame = cv2.flip(frame, 1)

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define skin color range (adjust for your lighting/skin tone)
        lower_skin = np.array([0, 30, 60], dtype=np.uint8)
        upper_skin = np.array([20, 150, 255], dtype=np.uint8)

        # Create a mask for skin color
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Optional: clean up the mask
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour (most likely your hand)
            largest_contour = max(contours, key=cv2.contourArea)

            # Get bounding box and center
            x, y, w, h = cv2.boundingRect(largest_contour)
            cx = x + w // 2
            cy = y + h // 2

            # Draw rectangle and center point
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)

            # Display coordinates
            cv2.putText(frame, f"Hand Position: ({cx}, {cy})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Hand Tracker", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    # Check for the primary monitor size
    for monitor in get_monitors():
        print(f"Monitor: {monitor.name}")
        print(f" Width: {monitor.width}")
        print(f" Height: {monitor.height}")
        print(f" X: {monitor.x}")  # X position relative to primary monitor
        print(f" Y: {monitor.y}")  # Y position relative to primary monitor
        print("------")
        
    x, y = pyautogui.position()
    print(f"Mouse position: ({x}, {y})")
    
    get_camera()
    
    