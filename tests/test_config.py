"""Unit tests for configuration parameters."""

import unittest
from pathlib import Path

from src import config


class TestConfig(unittest.TestCase):
    """Test configuration threshold constraints and path definitions."""

    def test_threshold_ranges(self):
        """Ensure threshold constants are within expected mathematical ranges."""
        self.assertGreater(config.EAR_THRESH, 0.1)
        self.assertLess(config.EAR_THRESH, 0.5)
        self.assertGreater(config.MAR_THRESH, 0.3)
        self.assertLess(config.MAR_THRESH, 1.0)
        self.assertGreater(config.EAR_CONSEC_FRAMES, 5)

    def test_landmark_indices(self):
        """Ensure facial landmark index lists have expected count."""
        self.assertEqual(len(config.LEFT_EYE_INDICES), 6)
        self.assertEqual(len(config.RIGHT_EYE_INDICES), 6)

    def test_directories_creation(self):
        """Check directory paths."""
        self.assertIsInstance(config.BASE_DIR, Path)
        self.assertTrue(config.DROWSY_SCREENSHOTS_DIR.exists())
        self.assertTrue(config.YAWN_SCREENSHOTS_DIR.exists())


if __name__ == "__main__":
    unittest.main()
