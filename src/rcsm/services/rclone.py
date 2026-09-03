import subprocess
import time

from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table

console = Console()


def execute(command: list[str]) -> tuple[int, str]:
    """
    Execute an rclone command with a live progress display.

    Returns:
        (exit_code, output)
    """

    if "--progress" not in command:
        command = command + ["--progress"]

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

    start_time = time.time()

    checks = ""
    transferred = ""
    speed = ""
    eta = ""
    listed = ""

    status = "Starting..."
    transfer_started = False

    assert process.stdout is not None

    with Live(console=console, refresh_per_second=10) as live:

        for line in process.stdout:

            clean = line.rstrip("\r\n")

            if not clean:
                continue

            output_lines.append(clean)

            # ---------------------------------
            # RCLONE PROGRESS
            # ---------------------------------

            if clean.startswith("Checks:"):
                checks = clean.replace("Checks:", "").strip()

                if not transfer_started:
                    status = "Checking files..."

            elif clean.startswith("Transferred:"):

                transferred = clean.replace(
                    "Transferred:", ""
                ).strip()

                # Detect whether actual data is being transferred
                if not transferred.startswith("0 B / 0 B"):
                    transfer_started = True
                    status = "Transferring..."
                else:
                    if not transfer_started:
                        status = "Checking files..."

                # Extract speed and ETA
                parts = clean.split(",")

                for part in parts:

                    part = part.strip()

                    if "B/s" in part:
                        speed = part

                    if "ETA" in part:
                        eta = part.replace(
                            "ETA", ""
                        ).strip()

            elif "Listed" in clean:

                listed = clean

            # ---------------------------------
            # IMPORTANT RCLONE MESSAGES
            # ---------------------------------

            elif (
                "NOTICE:" in clean
                or "ERROR" in clean
                or "Failed" in clean
            ):

                console.print(clean)

            # ---------------------------------
            # BUILD STATUS DISPLAY
            # ---------------------------------

            elapsed_seconds = int(
                time.time() - start_time
            )

            minutes = elapsed_seconds // 60
            seconds = elapsed_seconds % 60

            elapsed_display = (
                f"{minutes:02d}:{seconds:02d}"
            )

            table = Table(
                title="RClone Sync Manager",
                show_header=False,
                box=None,
            )

            table.add_row(
                Spinner(
                    "dots",
                    text=status,
                )
            )

            if checks:
                table.add_row(
                    f"[cyan]Checks:[/cyan] {checks}"
                )

            if listed:
                table.add_row(
                    f"[cyan]Files:[/cyan] {listed}"
                )

            # Only show transfer information
            # when an actual transfer is happening.
            if transfer_started:

                if transferred:
                    table.add_row(
                        f"[cyan]Transferred:[/cyan] "
                        f"{transferred}"
                    )

                if speed:
                    table.add_row(
                        f"[cyan]Speed:[/cyan] {speed}"
                    )

                if eta:
                    table.add_row(
                        f"[cyan]ETA:[/cyan] {eta}"
                    )

            table.add_row(
                f"[cyan]Elapsed:[/cyan] "
                f"{elapsed_display}"
            )

            live.update(table)

    process.wait()

    console.print()

    return (
        process.returncode,
        "\n".join(output_lines),
    )
