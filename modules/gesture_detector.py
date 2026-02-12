"""
Gesture Detector Module
Handles hand tracking and gesture recognition using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np


class GestureDetector:
    """Detects hand gestures using MediaPipe hand tracking"""

    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Initialize the gesture detector

        Args:
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Finger tip and pip (proximal interphalangeal) landmark IDs
        self.finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.finger_pips = [2, 6, 10, 14, 18]

    def detect_hands(self, frame):
        """
        Detect hands in the frame

        Args:
            frame: BGR image frame from camera

        Returns:
            results: MediaPipe hand detection results
            frame_rgb: RGB converted frame
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        return results, frame_rgb

    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on the frame

        Args:
            frame: BGR image frame
            hand_landmarks: Detected hand landmarks
        """
        self.mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

    def count_fingers(self, landmarks, hand_label):
        """
        Count extended fingers

        Args:
            landmarks: Hand landmark list
            hand_label: 'Left' or 'Right' hand

        Returns:
            List of finger states [thumb, index, middle, ring, pinky]
        """
        fingers = []

        # Thumb (different logic based on hand)
        if hand_label == "Right":
            if landmarks[self.finger_tips[0]].x < landmarks[self.finger_pips[0]].x:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if landmarks[self.finger_tips[0]].x > landmarks[self.finger_pips[0]].x:
                fingers.append(1)
            else:
                fingers.append(0)

        # Other four fingers
        for i in range(1, 5):
            if landmarks[self.finger_tips[i]].y < landmarks[self.finger_pips[i]].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def recognize_gesture(self, fingers):
        """
        Recognize gesture based on finger states

        Args:
            fingers: List of finger states [thumb, index, middle, ring, pinky]

        Returns:
            Gesture name as string
        """
        # Count total fingers up
        total = sum(fingers)

        # Gesture patterns
        if total == 0:
            return "Fist"
        elif total == 5:
            return "Open Palm"
        elif fingers == [0, 1, 1, 0, 0]:
            return "Peace Sign"
        elif fingers == [1, 0, 0, 0, 0]:
            return "Thumbs Up"
        elif fingers == [0, 1, 0, 0, 1]:
            return "Rock Sign"
        elif fingers == [1, 1, 0, 0, 0]:
            return "Gun Sign"
        elif fingers == [1, 1, 1, 0, 0]:
            return "Three Fingers"
        elif fingers == [0, 1, 0, 0, 0]:
            return "Point"
        else:
            return "Unknown"

    def get_gesture(self, frame):
        """
        Main method to get gesture from frame

        Args:
            frame: BGR image frame

        Returns:
            gesture: Detected gesture name
            frame: Processed frame with landmarks
            landmarks: Hand landmarks (or None)
        """
        results, frame_rgb = self.detect_hands(frame)
        gesture = None
        landmarks = None

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw landmarks
                self.draw_landmarks(frame, hand_landmarks)

                # Get hand label (Left/Right)
                hand_label = results.multi_handedness[idx].classification[0].label

                # Get landmark list
                lm_list = hand_landmarks.landmark

                # Count fingers
                fingers = self.count_fingers(lm_list, hand_label)

                # Recognize gesture
                gesture = self.recognize_gesture(fingers)
                landmarks = lm_list

                # Display finger count
                cv2.putText(frame, f"Fingers: {sum(fingers)}", (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                break  # Process only first hand for simplicity

        return gesture, frame, landmarks

    def release(self):
        """Release resources"""
        self.hands.close()