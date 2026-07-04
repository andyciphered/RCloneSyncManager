from rich.console import Console
from rich.table import Table

from rcsm.services.command_builder import build_command
from rcsm.services.config import load_jobs
from rcsm.services.health import check_rclone
from rcsm.ui.banner import show_banner
from rcsm.ui.menu import show_main_menu

console = Console()


def run():

    show_banner()

    jobs = load_jobs()

    table = Table(title="System Status")

    table.add_column("Component")
    table.add_column("Status")

    table.add_row("Python", "✅")
    table.add_row(
        "RClone",
        "✅ Installed" if check_rclone() else "❌ Missing",
    )
    table.add_row("Jobs", f"✅ {len(jobs)} Loaded")

    console.print(table)

    choice, groups, menu = show_main_menu(jobs)

    if choice == "Q":
        console.print("\nGoodbye!")
        return

    if choice == "A":
        console.print("\n[green]Sync All will be implemented in the next milestone.[/green]")
        return

    if choice in menu:

        group = menu[choice]

        console.print()

        console.print(f"[bold cyan]{group}[/bold cyan]\n")

        for index, job in enumerate(groups[group], start=1):
            console.print(f"{index}. {job.name}")

        print()

        selection = input("Select a job: ")

        try:
            selected = groups[group][int(selection) - 1]

        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")
            return

        command = build_command(selected)

        console.print()
        console.print("[bold green]Generated Command[/bold green]\n")
        console.print(" ".join(command))

        input("\nPress Enter to exit...")