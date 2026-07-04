from rich.console import Console
from rich.table import Table

from rcsm.services.command_builder import build_command
from rcsm.services.config import load_jobs
from rcsm.services.health import check_rclone
from rcsm.services.rclone import execute
from rcsm.ui.banner import show_banner
from rcsm.ui.menu import show_main_menu

console = Console()


def show_status(jobs):

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


def select_job(group, jobs):

    console.print()
    console.print(f"[bold cyan]{group}[/bold cyan]\n")

    for index, job in enumerate(jobs, start=1):
        console.print(f"{index}. {job.name}")

    console.print()

    selection = input("Select a job: ")

    try:
        return jobs[int(selection) - 1]
    except (ValueError, IndexError):
        console.print("[red]Invalid selection[/red]")
        return None


def select_execution_mode():

    console.print()
    console.print("[bold cyan]Execution Mode[/bold cyan]\n")
    console.print("1. Normal")
    console.print("2. Resync")
    console.print("3. Force")
    console.print("4. Cancel\n")

    choices = {
        "1": "normal",
        "2": "resync",
        "3": "force",
        "4": "cancel",
    }

    return choices.get(input("Select mode: ").strip())


def select_force_conflict():

    console.print()
    console.print("[bold cyan]Force Direction[/bold cyan]\n")
    console.print("1. Push (local wins)")
    console.print("2. Pull (cloud wins)\n")

    choices = {
        "1": "push",
        "2": "pull",
    }

    return choices.get(input("Select force direction: ").strip())


def preview_command(command):

    console.print()
    console.print("[bold green]Generated Command[/bold green]\n")
    console.print(" ".join(command))
    console.print()


def confirm(prompt):

    return input(prompt).strip().upper() == "Y"


def report_result(result):

    if result == 0:
        console.print("\n[green]Sync completed successfully.[/green]")
    else:
        console.print(f"\n[red]Sync failed (Exit Code {result}).[/red]")


def execute_command(
    command,
    require_confirm=True,
    show_preview=True,
    report=True,
):

    if show_preview:
        preview_command(command)

    if require_confirm and not confirm("Run this command? (Y/N): "):
        return None, ""

    result, output = execute(command)

    if report:
        report_result(result)

    return result, output


def handle_resync_recovery(job, command, result, output):

    if result != 7 and "Must run --resync" not in output:
        return

    console.print()
    console.print("[yellow]Bisync requires a Resync.[/yellow]")

    if not confirm("Run Resync now? (Y/N): "):
        return

    resync_command = build_command(job, execution_mode="resync")
    resync_result, _ = execute_command(
        resync_command,
        require_confirm=False,
        show_preview=False,
        report=False,
    )

    if resync_result != 0:
        console.print(f"\n[red]Resync failed (Exit Code {resync_result}).[/red]")
        return

    console.print("\n[green]Resync completed.[/green]")

    if confirm("Run normal sync now? (Y/N): "):
        execute_command(
            command,
            require_confirm=False,
            show_preview=False,
        )


def execute_normal(job):

    command = build_command(job)
    result, output = execute_command(command)

    if result is not None:
        handle_resync_recovery(job, command, result, output)

    return True


def execute_resync(job):

    command = build_command(job, execution_mode="resync")
    execute_command(command)

    return True


def execute_force(job):

    conflict = select_force_conflict()

    if conflict is None:
        console.print("[red]Invalid force direction[/red]")
        return False

    dry_run_command = build_command(
        job,
        execution_mode="force",
        conflict=conflict,
        dry_run=True,
    )

    result, _ = execute_command(
        dry_run_command,
        require_confirm=False,
        report=False,
    )

    if result != 0:
        console.print(f"\n[red]Dry run failed (Exit Code {result}).[/red]")
        return False

    command = build_command(
        job,
        execution_mode="force",
        conflict=conflict,
    )

    execute_command(command)

    return True


def execute_selected_mode(job, execution_mode):

    if execution_mode == "normal":
        return execute_normal(job)

    if execution_mode == "resync":
        return execute_resync(job)

    if execution_mode == "force":
        return execute_force(job)

    if execution_mode == "cancel":
        console.print("\nCancelled.")
        return False

    console.print("[red]Invalid execution mode[/red]")
    return False


def run():

    show_banner()

    jobs = load_jobs()
    show_status(jobs)

    choice, groups, menu = show_main_menu(jobs)

    if choice == "Q":
        console.print("\nGoodbye!")
        return

    if choice == "A":
        console.print("\n[green]Sync All will be implemented later.[/green]")
        return

    if choice not in menu:
        console.print("[red]Invalid selection[/red]")
        return

    group = menu[choice]
    selected = select_job(group, groups[group])

    if selected is None:
        return

    execution_mode = select_execution_mode()

    if execute_selected_mode(selected, execution_mode):
        input("\nPress Enter to continue...")
