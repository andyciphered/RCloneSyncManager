from collections import defaultdict

from rich.console import Console

from rcsm.ui.input import get_key

console = Console()


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

        console.print(f"[bold yellow]{number}. {group}[/bold yellow]")

        menu[str(number)] = group

        number += 1

    console.print()

    console.print("[green]A[/green]. Sync All")

    console.print("[blue]L[/blue]. Sync History")

    console.print("[red]Q[/red]. Quit\n")

    return get_key("Select: ").strip().upper(), groups, menu