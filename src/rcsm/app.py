from rich.console import Console
from rich.table import Table

from rcsm.services.command_builder import build_command
from rcsm.services.config import load_jobs
from rcsm.services.health import check_rclone
from rcsm.services.rclone import execute
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
        console.print("\n[green]Sync All will be implemented later.[/green]")
        return

    if choice in menu:

        group = menu[choice]

        console.print()
        console.print(f"[bold cyan]{group}[/bold cyan]\n")

        for index, job in enumerate(groups[group], start=1):
            console.print(f"{index}. {job.name}")

        console.print()

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
        console.print()

        answer = input("Run this command? (Y/N): ").strip().upper()

        if answer == "Y":

            result, output = execute(command)

            if result == 0:
                console.print("\n[green]Sync completed successfully.[/green]")
            else:
                console.print(f"\n[red]Sync failed (Exit Code {result}).[/red]")

            if (
                result == 7
                or "Must run --resync" in output
            ):
                console.print()
                console.print("[yellow]Bisync requires a Resync.[/yellow]")

                answer = input("Run Resync now? (Y/N): ").strip().upper()

                if answer == "Y":

                    resync_command = build_command(
                        selected,
                        execution_mode="resync",
                    )

                    result, _ = execute(resync_command)

                    if result == 0:

                        console.print("\n[green]Resync completed.[/green]")

                        answer = input(
                            "Run normal sync now? (Y/N): "
                        ).strip().upper()

                        if answer == "Y":

                            result, _ = execute(command)

                            if result == 0:
                                console.print(
                                    "\n[green]Sync completed successfully.[/green]"
                                )
                            else:
                                console.print(
                                    f"\n[red]Sync failed (Exit Code {result}).[/red]"
                                )
        input("\nPress Enter to continue...")