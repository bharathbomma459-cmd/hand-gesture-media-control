# Hand Gesture Media Control 

## Description

Hand Gesture Media Control is a real-time computer vision application that enables users to control media playback using hand gestures captured via a webcam. The system detects hand landmarks and translates specific gestures into media control actions such as play/pause, volume adjustment, navigation, and more.


## Features

* Real-time hand tracking using MediaPipe
* Gesture-based media control
* Volume control using hand gestures
* Playback control (Play/Pause, Next, Previous)
* Advanced controls (Fullscreen, Theater Mode, Speed control)
* Smooth and stable gesture detection


## Gesture Controls

| Gesture                | Action                  |
| ---------------------- | ----------------------- |
| Fist                 | Play / Pause            |
| Open Palm            | Increase Playback Speed |
| Index + Middle      | Volume Up               |
| Ring + Pinky           | Volume Down             |
| Pinky Only          | Next Video              |
| Index + Middle + Ring  | Previous Video          |
| Middle + Ring          | Theater Mode            |
| Index Only          | Decrease Playback Speed |
| Index + Ring + Pinky   | Forward                 |
| Index + Middle + Pinky | Rewind                  |
| Middle + Ring + Pinky  | Fullscreen              |
| Index + Pinky       | Mute / Unmute           |


## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

## How to Run

1. Clone the repository:

```
git clone https://github.com/bharathbomma459-cmd/hand-gesture-media-control.git
```

2. Navigate to the project folder:

```
cd hand-gesture-media-control
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the project:

```
hand gesture.py
```

## How It Works

* The webcam captures real-time video
* MediaPipe detects 21 hand landmarks
* Finger positions are analyzed to determine gestures
* Each gesture is mapped to keyboard shortcuts using PyAutoGUI
* Actions are triggered only when gestures are stable

## Requirements

* Webcam-enabled device
* Python 3.x
* Opencv
* mediapipe
* pyautogui

## Future Improvements

* Add GUI interface
* Support for multiple hands
* Custom gesture configuration
* Mobile integration

## 👨‍💻 Author
Developed by Bharath M
