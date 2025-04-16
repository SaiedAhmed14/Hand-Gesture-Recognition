# Hand Gesture Recognition

A Python application that uses computer vision to detect and count fingers in real-time using your webcam.

## Features

- Real-time hand detection and tracking
- Finger counting for both left and right hands simultaneously
- Visual feedback with colored landmarks (green for right hand, blue for left hand)
- Display of finger count for each detected hand

## Requirements

- Python 3.6+
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/hand-gesture-recognition.git
cd hand-gesture-recognition
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Run the application:
```
python vision.py
```

2. Position your hand(s) in front of the webcam
3. The application will detect your hands and count the number of raised fingers
4. Press 'q' to quit the application

## How It Works

The application uses MediaPipe's hand tracking solution to detect hand landmarks in real-time. It then analyzes the positions of these landmarks to determine which fingers are raised. The finger counting logic takes into account whether the hand is left or right to correctly interpret the thumb position.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for the hand tracking solution
- [OpenCV](https://opencv.org/) for computer vision capabilities 