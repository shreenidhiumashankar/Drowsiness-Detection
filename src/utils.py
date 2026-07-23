"""Utility functions for screenshot management and landmark rendering."""

from datetime import datetime
import logging
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np

from src.config import DROWSY_SCREENSHOTS_DIR, YAWN_SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


def save_screenshot(frame: np.ndarray, alert_type: str) -> str:
    """Save an annotated camera frame as a timestamped JPEG image.

    Args:
        frame: OpenCV image matrix (BGR).
        alert_type: Type of alert ('drowsy' or 'yawn').

    Returns:
        String path to the saved screenshot file.
    """
    target_dir = DROWSY_SCREENSHOTS_DIR if alert_type == "drowsy" else YAWN_SCREENSHOTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = target_dir / f"{alert_type}_{timestamp}.jpg"

    cv2.imwrite(str(filename), frame)
    logger.info(f"[{alert_type.upper()}] Screenshot saved: {filename}")
    return str(filename)


def draw_landmarks(
    frame: np.ndarray,
    landmarks: List[Tuple[int, int]],
    color: Tuple[int, int, int] = (0, 255, 0),
    radius: int = 2,
) -> None:
    """Draw dots on specified facial landmark coordinates.

    Args:
        frame: OpenCV image matrix in-place.
        landmarks: List of (x, y) coordinate tuples.
        color: BGR color tuple.
        radius: Circle radius in pixels.
    """
    for point in landmarks:
        cv2.circle(frame, point, radius, color, -1)
