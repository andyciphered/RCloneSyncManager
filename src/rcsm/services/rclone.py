import subprocess
import sys

from rich.console import Console

console = Console()


def execute(command: list[str]) -> tuple[int, str]:
    """
    Execute an rclone command.

    Returns:
        (exit_code, output)
    """

    console.print("\n[bold green]Executing...[/bold green]\n")
    console.print(" ".join(command))
    console.print()

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

    except FileNotFoundError:
        console.print(
            "\n[red]Error:[/red] rclone executable not found."
        )
        console.print(
            "Please install rclone or ensure it is available in your PATH."
        )
        return 127, ""

    output_lines = []

    assert process.stdout is not None

    for line in process.stdout:
        sys.stdout.write(line)
        output_lines.append(line)

    process.wait()

    return process.returncode, "".join(output_lines)