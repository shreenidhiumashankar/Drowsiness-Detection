# Facial Landmark Detection Model

This repository utilizes **Google MediaPipe Face Mesh** for real-time 3D facial landmark estimation.

## Model Specifications
- **Landmarks Count**: 468 3D facial coordinates.
- **Inference Speed**: ~30-60 FPS on standard desktop CPU without requiring a GPU.
- **Model Loading**: Dynamically fetched and initialized via `mediapipe.solutions.face_mesh` at runtime.
- **Eye Landmarks**: 6 points per eye for Eye Aspect Ratio (EAR) computation.
- **Lip Landmarks**: Top, bottom, left, and right lip centers for Mouth Aspect Ratio (MAR) computation.
