import subprocess

from rich.console import Console

console = Console()


def execute(command: list[str]) -> int:
    """
    Execute a previously generated rclone command.
    """

    console.print("\n[bold green]Executing...[/bold green]\n")
    console.print(" ".join(command))
    console.print()

    process = subprocess.Popen(command)

    process.wait()

    return process.returncode