"""
Jutsu Engine Module
Manages jutsu activation, visual effects, and sound feedback
"""

import cv2
import numpy as np
import pygame
import os
import time


class JutsuEngine:
    """Handles jutsu activation and effects"""

    def __init__(self, assets_path="assets"):
        """
        Initialize jutsu engine

        Args:
            assets_path: Path to assets folder
        """
        self.assets_path = assets_path

        # Initialize pygame mixer for sound
        pygame.mixer.init()

        # Jutsu mapping
        self.jutsu_map = {
            "Fist": "Fire Style: Fireball Jutsu",
            "Open Palm": "Shadow Clone Jutsu",
            "Peace Sign": "Lightning Style: Chidori",
            "Thumbs Up": "Water Style: Water Dragon",
            "Rock Sign": "Earth Style: Rock Barrier",
            "Gun Sign": "Wind Style: Air Bullet",
            "Three Fingers": "Ice Style: Crystal Mirror",
            "Point": "Gentle Fist: Chakra Strike"
        }

        # Active effects
        self.active_effects = []
        self.effect_duration = 1.5  # seconds

        # Load sounds (if available)
        self.sounds = self._load_sounds()

        # Effect colors
        self.effect_colors = {
            "Fire Style: Fireball Jutsu": (0, 69, 255),  # Orange
            "Shadow Clone Jutsu": (128, 128, 128),  # Gray
            "Lightning Style: Chidori": (255, 255, 0),  # Cyan
            "Water Style: Water Dragon": (255, 0, 0),  # Blue
            "Earth Style: Rock Barrier": (19, 69, 139),  # Brown
            "Wind Style: Air Bullet": (255, 255, 255),  # White
            "Ice Style: Crystal Mirror": (255, 200, 200),  # Light Blue
            "Gentle Fist: Chakra Strike": (255, 0, 255)  # Magenta
        }

        # Effect shapes
        self.effect_shapes = {
            "Fire Style: Fireball Jutsu": "circle",
            "Shadow Clone Jutsu": "clone",
            "Lightning Style: Chidori": "lightning",
            "Water Style: Water Dragon": "wave",
            "Earth Style: Rock Barrier": "rectangle",
            "Wind Style: Air Bullet": "spiral",
            "Ice Style: Crystal Mirror": "hexagon",
            "Gentle Fist: Chakra Strike": "burst"
        }

    def _load_sounds(self):
        """Load sound files if they exist"""
        sounds = {}
        sound_path = os.path.join(self.assets_path, "sounds")

        if not os.path.exists(sound_path):
            return sounds

        sound_files = {
            "Fire Style: Fireball Jutsu": "fire_jutsu.mp3",
            "Lightning Style: Chidori": "chidori.mp3",
            "Shadow Clone Jutsu": "shadow_clone_jutsu.mp3"
        }

        for jutsu, filename in sound_files.items():
            filepath = os.path.join(sound_path, filename)
            if os.path.exists(filepath):
                try:
                    sounds[jutsu] = pygame.mixer.Sound(filepath)
                except:
                    pass

        return sounds

    def activate_jutsu(self, gesture):
        """
        Activate jutsu based on gesture

        Args:
            gesture: Detected gesture name

        Returns:
            Jutsu name or None
        """
        if gesture in self.jutsu_map:
            jutsu_name = self.jutsu_map[gesture]

            # Add to active effects
            effect = {
                "name": jutsu_name,
                "start_time": time.time(),
                "progress": 0.0
            }
            self.active_effects.append(effect)

            # Play sound if available
            if jutsu_name in self.sounds:
                self.sounds[jutsu_name].play()

            return jutsu_name

        return None

    def update_effects(self, frame):
        """
        Update and render active effects

        Args:
            frame: Image frame to draw effects on
        """
        current_time = time.time()
        effects_to_remove = []

        for effect in self.active_effects:
            elapsed = current_time - effect["start_time"]

            if elapsed > self.effect_duration:
                effects_to_remove.append(effect)
                continue

            # Calculate progress (0.0 to 1.0)
            progress = elapsed / self.effect_duration
            effect["progress"] = progress

            # Render effect
            self._render_effect(frame, effect)

        # Remove completed effects
        for effect in effects_to_remove:
            self.active_effects.remove(effect)

    def _render_effect(self, frame, effect):
        """
        Render visual effect on frame

        Args:
            frame: Image frame
            effect: Effect dictionary
        """
        jutsu_name = effect["name"]
        progress = effect["progress"]

        h, w = frame.shape[:2]
        center = (w // 2, h // 2)

        color = self.effect_colors.get(jutsu_name, (255, 255, 255))
        shape = self.effect_shapes.get(jutsu_name, "circle")

        # Calculate effect size based on progress
        max_radius = min(w, h) // 3
        radius = int(max_radius * progress)

        # Alpha blending for transparency effect
        alpha = 1.0 - progress
        overlay = frame.copy()

        if shape == "circle":
            cv2.circle(overlay, center, radius, color, -1)

        elif shape == "lightning":
            # Lightning bolt effect
            for i in range(5):
                offset = int(50 * np.sin(progress * 10 + i))
                start = (center[0] + offset, center[1] - radius)
                end = (center[0] - offset, center[1] + radius)
                cv2.line(overlay, start, end, color, 3)

        elif shape == "clone":
            # Multiple circles (clone effect)
            for i in range(3):
                angle = (i * 120 + progress * 360) * np.pi / 180
                offset_x = int(100 * np.cos(angle))
                offset_y = int(100 * np.sin(angle))
                pos = (center[0] + offset_x, center[1] + offset_y)
                cv2.circle(overlay, pos, 30, color, -1)

        elif shape == "wave":
            # Water wave effect
            for i in range(0, w, 20):
                y_offset = int(30 * np.sin((i / 50) + progress * 10))
                cv2.line(overlay, (i, center[1] + y_offset),
                         (i + 10, center[1] + y_offset), color, 2)

        elif shape == "rectangle":
            # Rock barrier
            rect_size = int(100 + 50 * progress)
            top_left = (center[0] - rect_size, center[1] - rect_size)
            bottom_right = (center[0] + rect_size, center[1] + rect_size)
            cv2.rectangle(overlay, top_left, bottom_right, color, -1)

        elif shape == "spiral":
            # Wind spiral
            points = []
            for i in range(100):
                angle = (i / 100) * 4 * np.pi
                r = (i / 100) * radius
                x = int(center[0] + r * np.cos(angle))
                y = int(center[1] + r * np.sin(angle))
                points.append([x, y])

            if len(points) > 1:
                pts = np.array(points, np.int32)
                cv2.polylines(overlay, [pts], False, color, 2)

        elif shape == "hexagon":
            # Ice hexagon
            points = []
            for i in range(6):
                angle = i * 60 * np.pi / 180
                x = int(center[0] + radius * np.cos(angle))
                y = int(center[1] + radius * np.sin(angle))
                points.append([x, y])

            pts = np.array(points, np.int32)
            cv2.fillPoly(overlay, [pts], color)

        elif shape == "burst":
            # Chakra burst (star pattern)
            for i in range(8):
                angle = i * 45 * np.pi / 180
                end_x = int(center[0] + radius * np.cos(angle))
                end_y = int(center[1] + radius * np.sin(angle))
                cv2.line(overlay, center, (end_x, end_y), color, 3)

        # Blend overlay with original frame
        cv2.addWeighted(overlay, alpha * 0.5, frame, 1.0, 0, frame)

    def get_jutsu_name(self, gesture):
        """Get jutsu name from gesture"""
        return self.jutsu_map.get(gesture, None)

    def has_active_effects(self):
        """Check if there are active effects"""
        return len(self.active_effects) > 0