"""Audio alert module for triggering drowsiness and yawning alarms."""

import logging
from pathlib import Path
import pygame

from src.config import SOUND_FILE_PATH

logger = logging.getLogger(__name__)


class AlertManager:
    """Manages sound initialization and playback for alerts."""

    def __init__(self, sound_path: Path = SOUND_FILE_PATH, volume: float = 1.0):
        """Initialize the Pygame mixer and load the alarm sound file.

        Args:
            sound_path: Path object pointing to the audio file.
            volume: Volume level between 0.0 and 1.0.
        """
        self.sound_path = sound_path
        self.volume = volume
        self.initialized = False
        self._init_audio()

    def _init_audio(self) -> None:
        """Initialize Pygame mixer safely."""
        try:
            pygame.mixer.init()
            if self.sound_path.exists():
                pygame.mixer.music.load(str(self.sound_path))
                pygame.mixer.music.set_volume(self.volume)
                self.initialized = True
                logger.info(f"Audio alert initialized with sound file: {self.sound_path}")
            else:
                logger.warning(f"Audio file not found at {self.sound_path}. Sound alerts disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize audio mixer: {e}")
            self.initialized = False

    def play_alert(self) -> None:
        """Play alarm audio if mixer is not already busy."""
        if not self.initialized:
            return
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
        except Exception as e:
            logger.error(f"Error playing alarm sound: {e}")

    def stop_alert(self) -> None:
        """Stop alarm audio playback."""
        if self.initialized:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                logger.error(f"Error stopping sound: {e}")
