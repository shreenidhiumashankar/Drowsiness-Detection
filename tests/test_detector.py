"""Unit tests for Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR) metrics."""

import unittest
from src.detector import calculate_ear, calculate_mar


class TestDetectorMetrics(unittest.TestCase):
    """Verify accuracy of EAR and MAR formulas with mock coordinates."""

    def test_calculate_ear_open_eye(self):
        """Test EAR calculation for simulated open eye."""
        # Simulated eye landmarks: [p1, p2, p3, p4, p5, p6]
        eye = [
            (0, 10),   # p1 (left corner)
            (3, 16),   # p2 (top left)
            (7, 16),   # p3 (top right)
            (10, 10),  # p4 (right corner)
            (7, 4),    # p5 (bottom right)
            (3, 4),    # p6 (bottom left)
        ]
        # Vertical dist 1: ||(3,16) - (3,4)|| = 12
        # Vertical dist 2: ||(7,16) - (7,4)|| = 12
        # Horizontal dist: ||(0,10) - (10,10)|| = 10
        # EAR = (12 + 12) / (2 * 10) = 24 / 20 = 1.2
        ear = calculate_ear(eye)
        self.assertAlmostEqual(ear, 1.2, places=2)

    def test_calculate_ear_closed_eye(self):
        """Test EAR calculation for simulated closed eye (vertical distance near 0)."""
        eye = [
            (0, 10),
            (3, 10),
            (7, 10),
            (10, 10),
            (7, 10),
            (3, 10),
        ]
        ear = calculate_ear(eye)
        self.assertAlmostEqual(ear, 0.0, places=2)

    def test_calculate_mar_yawning(self):
        """Test MAR calculation for wide open mouth (yawn)."""
        top_lip = (5, 25)
        bottom_lip = (5, 5)
        left_lip = (0, 15)
        right_lip = (10, 15)

        # Vertical: ||(5,25) - (5,5)|| = 20
        # Horizontal: ||(0,15) - (10,15)|| = 10
        # MAR = 20 / 10 = 2.0
        mar = calculate_mar(top_lip, bottom_lip, left_lip, right_lip)
        self.assertAlmostEqual(mar, 2.0, places=2)

    def test_calculate_mar_closed_mouth(self):
        """Test MAR calculation for closed mouth."""
        top_lip = (5, 16)
        bottom_lip = (5, 14)
        left_lip = (0, 15)
        right_lip = (10, 15)

        # Vertical: 2
        # Horizontal: 10
        # MAR = 2 / 10 = 0.2
        mar = calculate_mar(top_lip, bottom_lip, left_lip, right_lip)
        self.assertAlmostEqual(mar, 0.2, places=2)


if __name__ == "__main__":
    unittest.main()
