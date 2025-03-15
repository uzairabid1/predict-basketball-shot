# Basketball Shot Predictor

## Overview
This script tracks a moving ball in a video feed, estimates its trajectory using quadratic regression, and predicts whether it will land in a designated basket area. It utilizes OpenCV for image processing and contour detection.

## Features
- Captures frames from a video feed.
- Detects the ball using color filtering.
- Tracks the ball's position over multiple frames.
- Uses polynomial regression to estimate the trajectory.
- Predicts if the ball will land in the basket.
- Displays visual feedback with trajectory lines and predictions.

## Dependencies
Make sure you have the following Python libraries installed:
```bash
pip install opencv-python numpy math cvzone
```

## Code Breakdown

### 1. **Frame Capture and Processing**
- Captures a frame from the video feed.
- Crops the image to focus on the relevant region.
- Creates copies of the frame for different visualizations.

### 2. **Ball Detection**
- Uses color filtering (`myColorFinder.update()`) to extract the ball.
- Finds contours (`cvzone.findContours()`) to determine the ball’s position.
- Stores the detected positions in `posListX` and `posListY`.

### 3. **Trajectory Estimation**
- Fits a quadratic polynomial (`np.polyfit()`) to the tracked points.
- Draws circles at each detected position.
- Connects consecutive positions with lines to visualize the path.

### 4. **Prediction Mechanism**
- Evaluates the quadratic function at a future point.
- Checks if the predicted landing spot is within the basket area (`300 < x < 430`).
- Displays either **"Basket"** (Success) or **"No Basket"** (Failure).

### 5. **Displaying Results**
- A reference line is drawn at `(330, 593) to (430, 593)`.
- The final result image is resized and displayed using OpenCV.

### 6. **User Input Controls**
- Press **"s"** to start tracking.
- Press **"n"** (currently unused but assigned).

## Output
- Basket: ![basket1](https://github.com/user-attachments/assets/83069be2-07cf-4f83-b737-7a3f9a5ee8e2)
- No basket: ![nobasket1](https://github.com/user-attachments/assets/c2adf53b-4aa6-4db9-b5a4-76de6080d4e2)

## Usage
Run the script and ensure the camera captures the ball properly. The script will track the ball and provide a prediction.

## Future Improvements
- Implement real-time feedback with better smoothing for predictions.
- Allow dynamic adjustment of the basket position.
- Optimize contour detection for better accuracy in various lighting conditions.

