# Rock Paper Scissors - Computer Vision Game

This is a fun interactive Rock-Paper-Scissors game that uses your webcam and computer vision to recognize hand gestures and play against the system.

## 🔧 Features

- Real-time hand gesture detection using OpenCV.
- Countdown with visual feedback.
- AI opponent that randomly selects a move.
- Score tracking for user and AI.
- Image processing pipeline display: ROI, grayscale, background subtraction, thresholding, and finger detection.
- Overlayed GUI on a custom background (`BG.png`).

## 🧠 Gesture Recognition

- ✊ **Rock** 
- ✌️ **Scissors** 
- 🖐 **Paper** 

## 🛠 Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
````

## 📁 Folder Structure

```
Resources/
├── BG.png          # Main background image for the UI
├── 1.png           # Rock image (AI hand)
├── 2.png           # Paper image (AI hand)
└── 3.png           # Scissors image (AI hand)
```

## 🚀 How to Run

1. Clone or download this repository.
2. Place the required images inside the `Resources/` folder.
3. Run the main Python file:

```bash
python rps.py
```

4. When the live preview starts:

   * Press `S` to start the game
   * Press `Q` to quit

5. Show your gesture inside the green rectangle to play.

## ♻️ Controls

* `S` → Start the game
* `R` → Recalibrate the background
* `Q` → Quit the game

## 📸 Image Processing Stages

The following image processing stages are displayed in a side panel:

* ROI (original hand image)
* Grayscale & blur
* Background subtraction
* Thresholded binary image
* Finger detection (circular mask)

## 🤠 Credits

Developed using OpenCV and NumPy.

---

Have fun playing!