"""Unit tests for audio alert manager."""

import unittest
from pathlib import Path
from src.sound_alert import AlertManager


class TestSoundAlert(unittest.TestCase):
    """Test AlertManager class initialization and safe execution."""

    def test_alert_manager_init(self):
        """Ensure AlertManager initializes gracefully even if audio device or file is missing."""
        dummy_path = Path("non_existent_audio_file.mp3")
        manager = AlertManager(sound_path=dummy_path)
        self.assertFalse(manager.initialized)
        # Calling play_alert on uninitialized manager should not raise exceptions
        manager.play_alert()
        manager.stop_alert()


if __name__ == "__main__":
    unittest.main()
