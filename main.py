"""Main entry point for the Drowsiness & Yawn Detection application.

Run this module to launch the graphical user interface.
"""

import logging
import sys
import tkinter as tk

from src.gui import DrowsinessGUI

# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    """Initialize root Tkinter app and start main loop."""
    root = tk.Tk()
    app = DrowsinessGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
