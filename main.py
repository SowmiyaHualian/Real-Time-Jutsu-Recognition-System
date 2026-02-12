"""
Real-Time Jutsu Recognition System
Main application entry point
"""

import cv2
import sys
import os
import time

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.gesture_detector import GestureDetector
from modules.jutsu_engine import JutsuEngine
from modules.chakra_system import ChakraSystem


class JutsuRecognitionApp:
    """Main application class"""

    def __init__(self):
        """Initialize the application"""
        print("Initializing Real-Time Jutsu Recognition System...")

        # Initialize components
        self.gesture_detector = GestureDetector()
        self.jutsu_engine = JutsuEngine(assets_path="assets")
        self.chakra_system = ChakraSystem(max_chakra=100, regen_rate=0.5)

        # Video capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # FPS calculation
        self.prev_time = time.time()
        self.fps = 0

        # State variables
        self.last_gesture = None
        self.last_jutsu = None
        self.gesture_start_time = None
        self.gesture_hold_duration = 0.5  # seconds to hold gesture before activation

        # UI settings
        self.paused = False

        print("✓ Initialization complete!")
        print("\nControls:")
        print("  Q or ESC - Quit")
        print("  R - Reset Chakra")
        print("  P - Pause/Resume")
        print("\nGestures:")
        print("  ✊ Fist - Fire Style: Fireball Jutsu")
        print("  ✌️ Peace Sign - Lightning Style: Chidori")
        print("  🖐️ Open Palm - Shadow Clone Jutsu")
        print("  👍 Thumbs Up - Water Style: Water Dragon")
        print("  🤘 Rock Sign - Earth Style: Rock Barrier")
        print("\n" + "=" * 50 + "\n")

    def draw_ui(self, frame):
        """
        Draw UI elements on frame

        Args:
            frame: Image frame
        """
        h, w = frame.shape[:2]

        # Create semi-transparent overlay for UI background
        overlay = frame.copy()

        # Top panel background
        cv2.rectangle(overlay, (0, 0), (w, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

        # Title
        title = "REAL-TIME JUTSU RECOGNITION SYSTEM"
        cv2.putText(frame, title, (w // 2 - 400, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

        # FPS Counter
        fps_text = f"FPS: {self.fps}"
        cv2.putText(frame, fps_text, (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Chakra bar
        chakra_percentage = self.chakra_system.get_chakra_percentage()
        chakra_color = self.chakra_system.get_chakra_color()

        # Chakra label
        cv2.putText(frame, "CHAKRA:", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Chakra bar background
        bar_x, bar_y, bar_w, bar_h = 120, 95, 300, 20
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h),
                      (50, 50, 50), -1)

        # Chakra bar fill
        fill_w = int(bar_w * (chakra_percentage / 100))
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h),
                      chakra_color, -1)

        # Chakra percentage text
        chakra_text = f"{int(chakra_percentage)}%"
        cv2.putText(frame, chakra_text, (bar_x + bar_w + 10, bar_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Current gesture
        if self.last_gesture and self.last_gesture != "Unknown":
            gesture_text = f"Gesture: {self.last_gesture}"
            cv2.putText(frame, gesture_text, (w - 400, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Active jutsu
        if self.last_jutsu:
            jutsu_text = f"Active: {self.last_jutsu}"
            cv2.putText(frame, jutsu_text, (w - 550, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Cooldown indicator
            cooldown = self.chakra_system.get_cooldown_remaining(self.last_gesture)
            if cooldown > 0:
                cooldown_text = f"Cooldown: {cooldown:.1f}s"
                cv2.putText(frame, cooldown_text, (w - 550, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 150, 255), 2)

        # Paused indicator
        if self.paused:
            pause_text = "PAUSED"
            text_size = cv2.getTextSize(pause_text, cv2.FONT_HERSHEY_SIMPLEX, 2.0, 3)[0]
            text_x = (w - text_size[0]) // 2
            text_y = h // 2
            cv2.putText(frame, pause_text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 5)

        # Instructions (bottom)
        instructions = "Q:Quit | R:Reset Chakra | P:Pause"
        cv2.putText(frame, instructions, (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    def calculate_fps(self):
        """Calculate and update FPS"""
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.fps = int(fps)
        self.prev_time = current_time

    def process_gesture(self, gesture):
        """
        Process detected gesture and activate jutsu if conditions met

        Args:
            gesture: Detected gesture name
        """
        if gesture == "Unknown" or gesture is None:
            self.last_gesture = None
            self.gesture_start_time = None
            return

        # Check if it's a new gesture
        if gesture != self.last_gesture:
            self.last_gesture = gesture
            self.gesture_start_time = time.time()
            return

        # Check if gesture held long enough
        if self.gesture_start_time:
            hold_time = time.time() - self.gesture_start_time

            if hold_time >= self.gesture_hold_duration:
                # Try to activate jutsu
                if self.chakra_system.can_use_jutsu(gesture):
                    # Use chakra
                    if self.chakra_system.use_jutsu(gesture):
                        # Activate jutsu
                        jutsu_name = self.jutsu_engine.activate_jutsu(gesture)
                        if jutsu_name:
                            self.last_jutsu = jutsu_name
                            print(f"✓ Activated: {jutsu_name}")

                # Reset gesture timer to prevent immediate re-activation
                self.gesture_start_time = None

    def run(self):
        """Main application loop"""
        print("Starting camera feed...")
        print("Show hand gestures to activate jutsus!\n")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)

            # Calculate FPS
            self.calculate_fps()

            if not self.paused:
                # Detect gesture
                gesture, frame, landmarks = self.gesture_detector.get_gesture(frame)

                # Process gesture for jutsu activation
                if gesture:
                    self.process_gesture(gesture)

                # Regenerate chakra
                self.chakra_system.regenerate()

                # Update and render effects
                self.jutsu_engine.update_effects(frame)

            # Draw UI
            self.draw_ui(frame)

            # Display frame
            cv2.imshow("Jutsu Recognition System", frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == 27:  # Q or ESC
                print("\nShutting down...")
                break
            elif key == ord('r'):  # Reset chakra
                self.chakra_system.reset()
                print("Chakra reset to maximum!")
            elif key == ord('p'):  # Pause
                self.paused = not self.paused
                print("Paused" if self.paused else "Resumed")

        # Cleanup
        self.cleanup()

    def cleanup(self):
        """Release resources"""
        print("Releasing resources...")
        self.cap.release()
        self.gesture_detector.release()
        cv2.destroyAllWindows()
        print("✓ Cleanup complete!")


def main():
    """Application entry point"""
    try:
        app = JutsuRecognitionApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()