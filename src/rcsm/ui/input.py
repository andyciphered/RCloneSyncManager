import sys
import termios
import tty

from rich.console import Console

console = Console()


def get_key(prompt=""):
    """Read one key immediately without requiring Enter."""
    console.print(prompt, end="")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    console.print(key)

    return key