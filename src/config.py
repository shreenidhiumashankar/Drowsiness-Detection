"""Configuration settings for the Drowsiness and Yawn Detection system.

This module centralizes threshold parameters, facial landmark indices for MediaPipe,
audio alert settings, and directory paths for dynamic asset loading.
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
SCREENSHOTS_DIR = ASSETS_DIR / "screenshots"
DROWSY_SCREENSHOTS_DIR = SCREENSHOTS_DIR / "drowsy"
YAWN_SCREENSHOTS_DIR = SCREENSHOTS_DIR / "yawning"
SOUND_FILE_PATH = BASE_DIR / "music.mp3"

# Ensure directories exist
DROWSY_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
YAWN_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Detection Thresholds
EAR_THRESH: float = 0.25
"""Eye Aspect Ratio (EAR) threshold below which an eye is considered closed."""

EAR_CONSEC_FRAMES: int = 20
"""Number of consecutive frames closed before triggering a drowsiness alert."""

MAR_THRESH: float = 0.60
"""Mouth Aspect Ratio (MAR) threshold above which a mouth is considered yawning."""

# MediaPipe Face Mesh Landmark Indices
# Eye Landmark Indices (3D Mesh)
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

# Lip Landmark Indices
TOP_LIP_INDEX = 13
BOTTOM_LIP_INDEX = 14
LEFT_LIP_INDEX = 78
RIGHT_LIP_INDEX = 308

# Video Display Settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
GUI_WINDOW_SIZE = "720x640"
