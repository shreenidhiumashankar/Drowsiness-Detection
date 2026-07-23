# Changelog

All notable changes to the **Drowsiness & Yawn Detection System** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-23

### Added
- Complete refactoring into modular Python package (`src/config.py`, `src/detector.py`, `src/sound_alert.py`, `src/gui.py`, `src/utils.py`).
- Integrated **MediaPipe Face Mesh** for 468 3D facial landmark detection replacing legacy dlib 68-point model.
- Vectorized calculation of Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR).
- Asynchronous multithreaded Tkinter real-time graphical user interface.
- Automatic timestamped screenshot logger for event tracking.
- Audio alert system powered by Pygame mixer.
- Automated unit test suite under `tests/` covering configuration, EAR/MAR formulas, and sound alert safety.
- High-resolution architecture, workflow, flowchart, use case, and vision pipeline diagrams in `assets/`.
- 15-slide PowerPoint presentation deck (`presentation/Drowsiness_Detection_Presentation.pptx`).

### Removed
- Legacy unused dlib weight files (`shape_predictor_68_face_landmarks.dat` and `.bz2`).
- Hardcoded system paths.
