"""Drowsiness and Yawn Detection Engine using MediaPipe Face Mesh."""

import logging
from typing import Dict, List, Tuple

import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance

from src.config import (
    BOTTOM_LIP_INDEX,
    EAR_CONSEC_FRAMES,
    EAR_THRESH,
    LEFT_EYE_INDICES,
    LEFT_LIP_INDEX,
    MAR_THRESH,
    RIGHT_EYE_INDICES,
    RIGHT_LIP_INDEX,
    TOP_LIP_INDEX,
)
from src.utils import draw_landmarks, save_screenshot

logger = logging.getLogger(__name__)


def calculate_ear(eye_landmarks: List[Tuple[int, int]]) -> float:
    """Calculate the Eye Aspect Ratio (EAR) for a single eye.

    EAR formula:
        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

    Args:
        eye_landmarks: List of 6 landmark (x, y) coordinates for an eye.

    Returns:
        Eye Aspect Ratio scalar value.
    """
    a = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    b = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    c = distance.euclidean(eye_landmarks[0], eye_landmarks[3])

    if c == 0:
        return 0.0

    ear = (a + b) / (2.0 * c)
    return ear


def calculate_mar(
    top_lip: Tuple[int, int],
    bottom_lip: Tuple[int, int],
    left_lip: Tuple[int, int],
    right_lip: Tuple[int, int],
) -> float:
    """Calculate Mouth Aspect Ratio (MAR) for yawn detection.

    MAR formula:
        MAR = ||top - bottom|| / ||left - right||

    Args:
        top_lip: (x, y) coordinate of top inner lip center.
        bottom_lip: (x, y) coordinate of bottom inner lip center.
        left_lip: (x, y) coordinate of left mouth corner.
        right_lip: (x, y) coordinate of right mouth corner.

    Returns:
        Mouth Aspect Ratio scalar value.
    """
    vertical = distance.euclidean(top_lip, bottom_lip)
    horizontal = distance.euclidean(left_lip, right_lip)

    if horizontal == 0:
        return 0.0

    mar = vertical / horizontal
    return mar


class DrowsinessDetector:
    """Encapsulates MediaPipe Face Mesh processing, metric computation, and state tracking."""

    def __init__(
        self,
        ear_thresh: float = EAR_THRESH,
        ear_frames: int = EAR_CONSEC_FRAMES,
        mar_thresh: float = MAR_THRESH,
    ):
        """Initialize MediaPipe FaceMesh and state counters.

        Args:
            ear_thresh: Threshold for EAR below which eye is closed.
            ear_frames: Consecutive frame count threshold for drowsiness.
            mar_thresh: Threshold for MAR above which mouth is yawning.
        """
        self.ear_thresh = ear_thresh
        self.ear_frames = ear_frames
        self.mar_thresh = mar_thresh

        self.closed_frame_counter = 0
        self.drowsy_screenshot_taken = False
        self.yawn_screenshot_taken = False

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, bool]]:
        """Process a single camera BGR frame to detect facial landmarks and evaluate fatigue metrics.

        Args:
            frame: OpenCV image array (BGR format).

        Returns:
            Tuple containing:
                - Annotated image array (BGR format)
                - Dictionary with alert flags {'drowsy': bool, 'yawn': bool, 'ear': float, 'mar': float}
        """
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        alerts = {
            "drowsy": False,
            "yawn": False,
            "ear": 0.0,
            "mar": 0.0,
            "face_detected": False,
        }

        if results.multi_face_landmarks:
            alerts["face_detected"] = True
            mesh_points = results.multi_face_landmarks[0].landmark

            # Eye landmark extraction
            left_eye = [(int(mesh_points[i].x * w), int(mesh_points[i].y * h)) for i in LEFT_EYE_INDICES]
            right_eye = [(int(mesh_points[i].x * w), int(mesh_points[i].y * h)) for i in RIGHT_EYE_INDICES]

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            ear = (left_ear + right_ear) / 2.0
            alerts["ear"] = ear

            # Lip landmark extraction
            top_lip = (int(mesh_points[TOP_LIP_INDEX].x * w), int(mesh_points[TOP_LIP_INDEX].y * h))
            bottom_lip = (int(mesh_points[BOTTOM_LIP_INDEX].x * w), int(mesh_points[BOTTOM_LIP_INDEX].y * h))
            left_lip = (int(mesh_points[LEFT_LIP_INDEX].x * w), int(mesh_points[LEFT_LIP_INDEX].y * h))
            right_lip = (int(mesh_points[RIGHT_LIP_INDEX].x * w), int(mesh_points[RIGHT_LIP_INDEX].y * h))

            mar = calculate_mar(top_lip, bottom_lip, left_lip, right_lip)
            alerts["mar"] = mar

            # Draw visual landmarks on eyes & mouth
            draw_landmarks(frame, left_eye + right_eye, color=(0, 255, 0), radius=2)
            draw_landmarks(frame, [top_lip, bottom_lip, left_lip, right_lip], color=(255, 0, 255), radius=3)

            # Evaluate Drowsiness (EAR)
            if ear < self.ear_thresh:
                self.closed_frame_counter += 1
                if self.closed_frame_counter >= self.ear_frames:
                    alerts["drowsy"] = True
                    cv2.putText(
                        frame,
                        "DROWSINESS ALERT!",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2,
                    )
                    if not self.drowsy_screenshot_taken:
                        save_screenshot(frame, "drowsy")
                        self.drowsy_screenshot_taken = True
            else:
                self.closed_frame_counter = 0
                self.drowsy_screenshot_taken = False

            # Evaluate Yawning (MAR)
            if mar > self.mar_thresh:
                alerts["yawn"] = True
                cv2.putText(
                    frame,
                    "YAWNING ALERT!",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                )
                if not self.yawn_screenshot_taken:
                    save_screenshot(frame, "yawn")
                    self.yawn_screenshot_taken = True
            else:
                self.yawn_screenshot_taken = False

            # Display real-time HUD telemetry on frame
            cv2.putText(frame, f"EAR: {ear:.2f}", (w - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"MAR: {mar:.2f}", (w - 150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame, alerts

    def close(self) -> None:
        """Release MediaPipe resources."""
        self.face_mesh.close()
