
from collections import defaultdict
import subprocess

from rich.console import Console

from rcsm.ui.input import get_key
from rcsm.services.logger import LOG_DIR

console = Console()



import subprocess

from rcsm.services.logger import LOG_DIR


def open_logs_folder():
    """Open the existing project logs directory in Finder."""

    console.print(f"[cyan]Opening logs folder: {LOG_DIR}[/cyan]")

    if not LOG_DIR.is_dir():
        console.print("[red]Logs folder does not exist.[/red]")
        return

    try:
        subprocess.run(["open", str(LOG_DIR)], check=True)
    except (subprocess.CalledProcessError, OSError) as error:
        console.print(f"[red]Could not open logs folder: {error}[/red]")

def show_main_menu(jobs):
    """
    Display the main menu and return the user's choice.
    """

    groups = defaultdict(list)

    for job in jobs:
        groups[job.group].append(job)

    console.print()

    console.print("[bold cyan]Main Menu[/bold cyan]\n")

    menu = {}

    number = 1

    for group in sorted(groups.keys()):

        console.print(
            f"[bold yellow]{number}. {group}[/bold yellow]"
        )

        menu[str(number)] = group

        number += 1

    console.print()

    console.print("[green]A[/green]. Sync All")
    console.print("[blue]L[/blue]. Sync History")
    console.print("[magenta]O[/magenta]. Open Logs Folder")
    console.print("[red]Q[/red]. Quit\n")

    return get_key("Select: ").strip().upper(), groups, menu
