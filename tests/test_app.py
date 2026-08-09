import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import greet


def test_greet_default():
    assert greet() == "Hello, world!"


def test_greet_name():
    assert greet("Claude") == "Hello, Claude!"
