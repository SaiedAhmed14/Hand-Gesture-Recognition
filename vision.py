import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands with multi-hand support
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Changed to detect up to 2 hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks, handedness):
    # Define finger tip IDs and pip IDs (first joint)
    tip_ids = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
    pip_ids = [2, 6, 10, 14, 18]  # First joints for each finger
    
    fingers = []
    
    # Handle thumb separately based on hand orientation
    if handedness.classification[0].label == "Right":
        # For right hand
        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[pip_ids[0]].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        # For left hand
        if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[pip_ids[0]].x:
            fingers.append(1)
        else:
            fingers.append(0)
    
    # For other fingers, check if the tip is above the pip joint
    for id in range(1, 5):
        # Get the y coordinates of the tip and pip
        tip_y = hand_landmarks.landmark[tip_ids[id]].y
        pip_y = hand_landmarks.landmark[pip_ids[id]].y
        
        # If tip is above pip (lower y value), finger is up
        if tip_y < pip_y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers.count(1)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video")
        break
    
    # Flip the image horizontally
    img = cv2.flip(img, 1)
    
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process hands
    results = hands.process(img_rgb)
    
    # Draw hand landmarks and count fingers
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get handedness (left or right hand)
            handedness = results.multi_handedness[idx]
            
            # Draw landmarks with different colors for each hand
            color = (0, 255, 0) if handedness.classification[0].label == "Right" else (255, 0, 0)
            mp_draw.draw_landmarks(
                img, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=color, thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=color, thickness=2)
            )
            
            # Count fingers
            finger_count = count_fingers(hand_landmarks, handedness)
            
            # Calculate position for text based on hand position
            h, w, c = img.shape
            x = int(min([landmark.x for landmark in hand_landmarks.landmark]) * w)
            y = int(min([landmark.y for landmark in hand_landmarks.landmark]) * h) - 20
            
            # Display the count with hand label
            hand_label = "R" if handedness.classification[0].label == "Right" else "L"
            cv2.putText(img, f"{hand_label}: {finger_count}", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # Display FPS and instructions
    cv2.putText(img, "Press 'q' to quit", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Display the image
    cv2.imshow("Hand Gesture Recognition", img)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()