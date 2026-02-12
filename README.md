# 🎥 Real-Time Jutsu Recognition System

An interactive computer vision application that detects hand gestures through live webcam feed and triggers corresponding virtual "jutsu" effects in real time.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)

## 📌 Overview

The **Real-Time Jutsu Recognition System** uses computer vision to detect hand gestures and activate ninja-themed visual effects. Simply show your hand to the camera, make a gesture, and watch the corresponding jutsu activate with visual effects and a chakra energy system!

### Core Technologies

- **OpenCV** - Real-time video capture and rendering
- **MediaPipe** - Hand landmark detection and tracking (21-point model)
- **Pygame** - Audio feedback system
- **NumPy** - Numerical computations

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Supported Gestures

| Gesture | Jutsu | Chakra Cost | Cooldown |
|---------|-------|-------------|----------|
| ✊ **Fist** | Fire Style: Fireball Jutsu | 30 | 2.0s |
| ✌️ **Peace Sign** | Lightning Style: Chidori | 40 | 4.0s |
| 🖐️ **Open Palm** | Shadow Clone Jutsu | 25 | 3.0s |
| 👍 **Thumbs Up** | Water Style: Water Dragon | 20 | 2.0s |
| 🤘 **Rock Sign** | Earth Style: Rock Barrier | 35 | 3.5s |
| 🔫 **Gun Sign** | Wind Style: Air Bullet | 30 | 2.5s |
| 👌 **Three Fingers** | Ice Style: Crystal Mirror | 25 | 2.0s |
| ☝️ **Point** | Gentle Fist: Chakra Strike | 15 | 1.5s |

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Q** or **ESC** | Quit application |
| **R** | Reset chakra to maximum |
| **P** | Pause/Resume detection |

## 📁 Project Structure

```
Real-Time-Jutsu-Recognition-System/
│
├── main.py                          # Application entry point
│
├── modules/
│   ├── gesture_detector.py          # Hand tracking & gesture recognition
│   ├── jutsu_engine.py              # Jutsu logic & visual effects
│   └── chakra_system.py             # Energy management system
│
├── assets/
│   ├── images/                      # Visual effect assets (optional)
│   └── sounds/                      # Audio files (optional)
│
└── requirements.txt                 # Python dependencies
```

## 🎯 Features

### ✋ Hand Tracking & Gesture Detection
- Real-time hand tracking using MediaPipe's 21 landmark points
- Intelligent finger state detection (up/down logic)
- Multi-gesture recognition capability
- No training dataset required (rule-based approach)

### ⚡ Jutsu System
- **Gesture → Jutsu Mapping** - Each hand gesture triggers a specific jutsu
- **Energy Management** - Chakra consumption and regeneration system
- **Cooldown Mechanism** - Prevents jutsu spam with timed restrictions
- **Visual Effects** - Dynamic procedurally-generated effects for each jutsu
- **Audio Feedback** - Sound effects for technique activation (optional)

### 🏗️ System Architecture
- **Modular Design** - Separated concerns for maintainability
- **Stateful Processing** - Frame-by-frame effect handling
- **Scalable Structure** - Easy to add new jutsus and gestures
- **Event-driven Logic** - Responsive gesture-to-action pipeline

## 🧠 How It Works

### Hand Landmark Detection

MediaPipe tracks 21 key points on your hand:

```
        8   12  16  20
        |   |   |   |
    4   |   |   |   |
    |   7   11  15  19
    |   |   |   |   |
    3   6   10  14  18
    |   |   |   |   |
    2   5   9   13  17
    |   |   |   |   |
    1   |   |   |   |
    |   |   |   |   |
    0 (wrist)
```

### Gesture Recognition

The system analyzes finger positions to determine which are extended:
- **Fist**: All fingers down
- **Open Palm**: All fingers up
- **Peace Sign**: Index and middle fingers up
- **Thumbs Up**: Only thumb up
- **Rock Sign**: Index and pinky up

### Chakra System

- **Starting Chakra**: 100 points
- **Regeneration**: +0.5 points per frame
- **Consumption**: Varies by jutsu (15-40 points)
- **Cooldown**: 1.5-4 seconds per jutsu

### Visual Effects

Each jutsu has a unique procedurally-generated visual effect:
- **Fire**: Expanding orange circle
- **Lightning**: Animated lightning bolts
- **Shadow Clone**: Multiple orbiting circles
- **Water**: Sine wave animation
- **Earth**: Rectangular barrier
- **Wind**: Spiral pattern
- **Ice**: Hexagonal crystal
- **Chakra Strike**: Star burst

## 🔧 Customization

### Adjust Detection Sensitivity

Edit `modules/gesture_detector.py`:

```python
min_detection_confidence=0.7  # Lower = more sensitive
min_tracking_confidence=0.5   # Tracking threshold
```

### Modify Chakra Values

Edit `modules/chakra_system.py`:

```python
MAX_CHAKRA = 100
REGEN_RATE = 0.5
```

### Add Custom Jutsus

1. Define gesture pattern in `gesture_detector.py`
2. Create jutsu definition in `jutsu_engine.py`
3. Add visual effect rendering
4. Set chakra cost in `chakra_system.py`

## 📊 System Requirements

### Minimum
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 4 GB
- **Webcam**: 720p @ 30fps
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Python**: 3.8+

### Recommended
- **CPU**: Quad-core 2.5 GHz+
- **RAM**: 8 GB+
- **Webcam**: 1080p @ 60fps
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04
- **Python**: 3.10+

## 🐛 Troubleshooting

### Camera Not Detected

Try changing the camera index in `main.py`:

```python
self.cap = cv2.VideoCapture(0)  # Try 1, 2, etc.
```

### Low FPS / Performance Issues

- Ensure good lighting conditions
- Close background applications
- Reduce camera resolution
- Update graphics drivers

### Gesture Not Recognized

- Keep hand clearly visible in frame
- Ensure proper lighting
- Hold gesture for 0.5 seconds
- Adjust detection confidence threshold

### Import Errors

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 🎨 Adding Assets (Optional)

The system works perfectly without assets using procedural effects!

### Sound Effects (assets/sounds/)
- `fire_jutsu.mp3`
- `chidori.mp3`
- `shadow_clone_jutsu.mp3`

Format: MP3, under 5 seconds

### Images (assets/images/)
- `fire.png`
- `lightning.png`

Format: PNG with transparency, 512x512 recommended

## 🛠 Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **OpenCV** | 4.8.0+ | Video capture and frame processing |
| **MediaPipe** | 0.10.0+ | Hand landmark detection |
| **NumPy** | 1.24.0+ | Mathematical operations |
| **Pygame** | 2.5.0+ | Sound system |

## 🚦 Future Enhancements

- [ ] Machine learning-based gesture classification
- [ ] Multi-hand tracking support
- [ ] 3D visual effects using OpenGL
- [ ] Gesture recording and playback
- [ ] Multiplayer jutsu battles
- [ ] Custom jutsu creator interface
- [ ] Mobile app version
- [ ] VR integration



## 👏 Acknowledgments

- **MediaPipe Team** - Excellent hand tracking solution
- **OpenCV Community** - Comprehensive computer vision library
- **Naruto Series** - Inspiration for jutsu concepts

---

**Made with ❤️ and 🐍 Python | Powered by Computer Vision**

**Happy Jutsu Training! 🥷**
