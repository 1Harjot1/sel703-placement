"""
demo.py
=======
One-command launch for the Cognitive-Access Live Demo (Web Inspector).
Simply run:
    python demo.py
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tool.web.server import run_server

if __name__ == "__main__":
    run_server()
