"""Graphical User Interface (Tkinter) for real-time driver fatigue monitoring."""

import logging
import threading
import tkinter as tk
from tkinter import ttk
from typing import Optional

import cv2
from PIL import Image, ImageTk

from src.config import FRAME_HEIGHT, FRAME_WIDTH, GUI_WINDOW_SIZE
from src.detector import DrowsinessDetector
from src.sound_alert import AlertManager

logger = logging.getLogger(__name__)


class DrowsinessGUI:
    """Tkinter Application window for Drowsiness & Yawn Detection."""

    def __init__(self, root: tk.Tk):
        """Initialize GUI layout, video feed components, and detector systems.

        Args:
            root: Root Tkinter window instance.
        """
        self.root = root
        self.root.title("Drowsiness & Yawn Detection System")
        self.root.geometry(GUI_WINDOW_SIZE)
        self.root.resizable(False, False)

        # Apply dark theme styling
        self.root.configure(bg="#1e1e2e")

        self.detector = DrowsinessDetector()
        self.alert_manager = AlertManager()

        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.video_thread: Optional[threading.Thread] = None

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self) -> None:
        """Construct Tkinter layout components."""
        # Header Title
        title_frame = tk.Frame(self.root, bg="#1e1e2e")
        title_frame.pack(fill="x", pady=10)

        title_label = tk.Label(
            title_frame,
            text="Driver Fatigue & Drowsiness Monitoring System",
            font=("Helvetica", 16, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e",
        )
        title_label.pack()

        # Video Panel Container
        self.video_panel = tk.Label(self.root, bg="#11111b", width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.video_panel.pack(pady=10)

        # Status & Metric Telemetry Bar
        telemetry_frame = tk.Frame(self.root, bg="#1e1e2e")
        telemetry_frame.pack(fill="x", px=20, pady=5)

        self.status_label = tk.Label(
            telemetry_frame,
            text="System Status: IDLE",
            font=("Helvetica", 11, "bold"),
            fg="#a6adc8",
            bg="#1e1e2e",
        )
        self.status_label.pack(side="left", px=20)

        self.metrics_label = tk.Label(
            telemetry_frame,
            text="EAR: -- | MAR: --",
            font=("Helvetica", 11),
            fg="#a6adc8",
            bg="#1e1e2e",
        )
        self.metrics_label.pack(side="right", px=20)

        # Control Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start Detection",
            font=("Helvetica", 11, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            px=20,
            py=8,
            relief="flat",
            command=self.start_detection,
        )
        self.start_btn.pack(side="left", padx=15)

        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ Stop Detection",
            font=("Helvetica", 11, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            activebackground="#eba0ac",
            px=20,
            py=8,
            relief="flat",
            state="disabled",
            command=self.stop_detection,
        )
        self.stop_btn.pack(side="right", padx=15)

    def start_detection(self) -> None:
        """Start camera video stream and detection thread."""
        if self.is_running:
            return

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.config(text="Status: Error - Camera Not Found", fg="#f38ba8")
            return

        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="Status: MONITORING ACTIVE", fg="#a6e3a1")

        self.video_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.video_thread.start()

    def _detection_loop(self) -> None:
        """Background thread loop capturing frames and evaluating fatigue."""
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to capture webcam frame.")
                break

            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            annotated_frame, alerts = self.detector.process_frame(frame)

            # Trigger sound alerts
            if alerts["drowsy"] or alerts["yawn"]:
                self.alert_manager.play_alert()

            # Format status text updates
            ear_val = alerts.get("ear", 0.0)
            mar_val = alerts.get("mar", 0.0)
            status_text = f"EAR: {ear_val:.2f} | MAR: {mar_val:.2f}"

            # Convert frame for Tkinter rendering
            rgb_img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(rgb_img)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            # Schedule UI update on main thread
            self.root.after(0, self._update_ui_frame, img_tk, status_text, alerts)

        self._cleanup_camera()

    def _update_ui_frame(self, img_tk: ImageTk.PhotoImage, telemetry_text: str, alerts: dict) -> None:
        """Update video panel image and telemetry labels safely on main thread."""
        if not self.is_running:
            return

        self.video_panel.configure(image=img_tk)
        self.video_panel.image = img_tk
        self.metrics_label.config(text=telemetry_text)

        if alerts.get("drowsy"):
            self.status_label.config(text="ALERT: DROWSINESS DETECTED!", fg="#f38ba8")
        elif alerts.get("yawn"):
            self.status_label.config(text="ALERT: YAWNING DETECTED!", fg="#fab387")
        elif alerts.get("face_detected"):
            self.status_label.config(text="Status: MONITORING (NORMAL)", fg="#a6e3a1")
        else:
            self.status_label.config(text="Status: NO FACE DETECTED", fg="#f9e2af")

    def stop_detection(self) -> None:
        """Stop video stream and reset controls."""
        self.is_running = False
        self.alert_manager.stop_alert()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Status: STOPPED", fg="#a6adc8")
        self.metrics_label.config(text="EAR: -- | MAR: --")

    def _cleanup_camera(self) -> None:
        """Release camera resources."""
        if self.cap:
            self.cap.release()
            self.cap = None

    def on_close(self) -> None:
        """Handle application close event."""
        self.stop_detection()
        self.detector.close()
        self.root.destroy()
