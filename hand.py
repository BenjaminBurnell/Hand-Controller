import cv2
import mediapipe as mp
import pyautogui

class HandTracker():
    def __init__(self, monitor_w, monitor_h):
        # --- Initialize MediaPipe Hands ---
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.current_clicking = False
        
        self.monitor_w = monitor_w
        self.monitor_h = monitor_h

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,      # Use for live video
            max_num_hands=1,              # Detect up to 2 hands
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def move_cursor_with_border(self, finger_x, finger_y, border_ratio=0.1):
        # Calculate inner camera area
        border_x = self.camera_w * border_ratio
        border_y = self.camera_h * border_ratio

        # Clamp finger coordinates within the inner area
        finger_x = min(max(finger_x, border_x), self.camera_w - border_x)
        finger_y = min(max(finger_y, border_y), self.camera_h - border_y)

        # Map inner camera area to full screen
        self.screen_x = int((finger_x - border_x) * self.monitor_w / (self.camera_w - 2 * border_x))
        self.screen_y = int((finger_y - border_y) * self.monitor_h / (self.camera_h - 2 * border_y))

        # Move the mouse
        pyautogui.moveTo(self.screen_x, self.screen_y)

        # print(f"Finger pos (camera, clamped): ({finger_x}, {finger_y})")
        # print(f"Mouse pos (screen): ({screen_x}, {screen_y})")
        
    def add_difference_to_smaller(self, a, b):
        difference = abs(a - b)
        smaller = min(a, b)
        return smaller + difference

    
    def get_hand_and_finger_positions(self):
        cap = cv2.VideoCapture(0)
        
        self.camera_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.camera_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Request a higher FPS
        cap.set(cv2.CAP_PROP_FPS, 60)  # try 60 FPS if your camera supports it

        # Check what FPS the camera actually uses
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Camera FPS: {fps}")

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Flip horizontally (mirror view)
            frame = cv2.flip(frame, 1)

            # Convert to RGB (MediaPipe requires RGB input)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb_frame)
            

            h, w, _ = frame.shape

            # Draw detected landmarks and connections
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                        self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )

                    # Collect positions of all 21 landmarks
                    landmarks = []
                    for i, lm in enumerate(hand_landmarks.landmark):
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        landmarks.append((i, cx, cy))

                    # Example: get specific finger landmarks
                    wrist = landmarks[0]
                    thumb_tip = landmarks[4]
                    index_tip = landmarks[8]
                    middle_tip = landmarks[12]
                    ring_tip = landmarks[16]
                    pinky_tip = landmarks[20]
                    
                    # Current Click X/Y
                    current_click_x = 0
                    current_click_y = 0

                    # Draw fingertip points
                    for fid, fx, fy in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]:
                        cv2.circle(frame, (fx, fy), 8, (255, 0, 0), -1)

                    # Display coordinates of index fingertip
                    ix, iy = index_tip[1], index_tip[2]
                    cv2.putText(frame, f"Index Tip: ({ix}, {iy})", (ix + 10, iy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    tx, ty = thumb_tip[1], thumb_tip[2]
                    cv2.putText(frame, f"Thumb Tip: ({tx}, {ty})", (tx + 10, ty - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    if(ix, iy, tx, ty):
                        self.move_cursor_with_border(tx, ty)
                    
                    current_click_x = self.add_difference_to_smaller(ix, tx)
                    current_click_y = self.add_difference_to_smaller(iy, ty)
                    
                    if (iy + 20) >= ty and iy <= ty and (ty - 20) <= iy and ty >= iy:
                        if (ix + 20) >= tx and ix <= tx and (tx - 20) <= ix and tx >= ix:
                            if(not self.current_clicking):
                                pyautogui.mouseDown(self.screen_x, self.screen_y)
                                print("Started clicking at:", current_click_x, current_click_y)
                                self.current_clicking = True
                                
                        elif(self.current_clicking):
                            pyautogui.mouseUp(self.screen_x, self.screen_y)
                            print("Stopped clicking at:", current_click_x, current_click_y)
                            self.current_clicking = False
                            
                    elif(self.current_clicking):
                        pyautogui.mouseUp(self.screen_x, self.screen_y)
                        print("Stopped clicking at:", current_click_x, current_click_y)
                        self.current_clicking = False

            # Show the video
            cv2.imshow("Hand & Finger Tracker", frame)

            # Press ESC to quit
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()