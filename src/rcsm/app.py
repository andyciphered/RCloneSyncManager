import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

from rcsm.services.command_builder import build_command
from rcsm.services.config import load_jobs
from rcsm.services.health import (
    check_rclone,
    check_remotes,
    check_local_paths,
    validate_job,
)
from rcsm.services.rclone import execute
from rcsm.services.logger import log_sync, get_sync_history
from rcsm.ui.banner import show_banner
from rcsm.ui.menu import show_main_menu
from rcsm.ui.input import get_key

console = Console()

def show_status(jobs):

    table = Table(title="System Status")
    table.add_column("Component")
    table.add_column("Status")

    table.add_row("Python", "✅")

    rclone_available = check_rclone()

    table.add_row(
        "RClone",
        "✅ Installed" if rclone_available else "❌ Missing",
    )

    table.add_row(
        "Jobs",
        f"✅ {len(jobs)} Loaded",
    )

    missing_remotes = None

    missing_paths, invalid_paths = check_local_paths(jobs)

    if invalid_paths:
        table.add_row(
            "Paths",
            f"❌ {len(invalid_paths)} Invalid",
        )

    elif missing_paths:
        table.add_row(
            "Paths",
            f"⚠️ {len(missing_paths)} Not Created",
        )

    else:
        table.add_row(
            "Paths",
            "✅ All Ready",
        )

    if rclone_available:
        missing_remotes = check_remotes(jobs)

        if missing_remotes is None:
            table.add_row(
                "Remotes",
                "⚠️ Check Failed",
            )

        elif missing_remotes:
            table.add_row(
                "Remotes",
                f"⚠️ {len(missing_remotes)} Missing",
            )

        else:
            table.add_row(
                "Remotes",
                "✅ All Ready",
            )

    console.print(table)

    if rclone_available and missing_remotes:
        console.print()
        console.print("[yellow]Missing remotes:[/yellow]")

        for job_name, remote_name in missing_remotes:
            console.print(
                f"  • {job_name}: {remote_name}"
            )

def show_sync_history():

    history = get_sync_history()

    console.print()
    console.print("[bold cyan]Sync History[/bold cyan]\n")

    if not history:
        console.print("[yellow]No sync history found.[/yellow]")
        return

    table = Table()
    table.add_column("Date/Time")
    table.add_column("Job")
    table.add_column("Status")
    table.add_column("Duration")

    for entry in reversed(history[-20:]):

        status = entry["status"]

        if status == "SUCCESS":
            status_display = "[green]SUCCESS[/green]"
        else:
            status_display = f"[red]{status}[/red]"

        table.add_row(
            entry["timestamp"],
            entry["job_name"],
            status_display,
            entry["duration"],
        )

    console.print(table)

def select_job(group, jobs):

    console.print()
    console.print(f"[bold cyan]{group}[/bold cyan]\n")

    for index, job in enumerate(jobs, start=1):
        console.print(f"{index}. {job.name}")

    console.print()

    selection = get_key("Select a job: ")

    try:
        return jobs[int(selection) - 1]
    except (ValueError, IndexError):
        console.print("[red]Invalid selection[/red]")
        return None


def select_execution_mode(job):

    console.print()
    console.print("[bold cyan]Execution Mode[/bold cyan]\n")

    console.print("1. Normal")

    choices = {
        "1": "normal",
    }

    if job.mode == "bisync":
        console.print("2. Resync")
        console.print("3. Force")
        console.print("4. Cancel\n")

        choices.update(
            {
                "2": "resync",
                "3": "force",
                "4": "cancel",
            }
        )

    else:
        console.print("2. Cancel\n")

        choices["2"] = "cancel"

    return choices.get(
        get_key("Select mode: ").strip()
    )

def select_force_conflict():

    console.print()
    console.print("[bold cyan]Force Direction[/bold cyan]\n")
    console.print("1. Push (local wins)")
    console.print("2. Pull (cloud wins)\n")

    choices = {
        "1": "push",
        "2": "pull",
    }

    return choices.get(get_key("Select force direction: ").strip())


def preview_command(command):

    console.print()
    console.print("[bold green]Generated Command[/bold green]\n")
    console.print(" ".join(command))
    console.print()


def confirm(prompt):

    return get_key(prompt).strip().upper() == "Y"


def report_result(result, output=""):

    if result == 0:
        console.print(
            "\n[green]Sync completed successfully.[/green]"
        )
        return

    console.print(
        f"\n[red]Sync failed (Exit Code {result}).[/red]"
    )

    error_lines = [
        line
        for line in output.splitlines()
        if (
            "ERROR" in line
            or "Failed" in line
            or "error" in line.lower()
        )
    ]

    if error_lines:
        console.print("\n[red]Error details:[/red]")

        for line in error_lines[-5:]:
            console.print(f"  {line}")

def execute_command(
    command,
    require_confirm=True,
    show_preview=True,
    report=True,
    job_name=None,
):

    if show_preview:
        preview_command(command)

    if require_confirm and not confirm("Run this command? (Y/N): "):
        return None, ""

    start_time = time.time()

    result, output = execute(command)

    duration = time.time() - start_time

    if job_name:
        log_sync(
            job_name,
            result,
            duration,
        )

    if report:
        report_result(result, output)

    return result, output

def ensure_local_folder(job):

    local = Path(job.local).expanduser()

    if local.exists():
        return

    console.print()
    console.print(f"[yellow]Creating local folder:[/yellow] {local}")

    local.mkdir(parents=True, exist_ok=True)

    console.print("[green]✓ Folder created.[/green]\n")

def handle_resync_recovery(job, command, result, output):

    if result != 7 and "Must run --resync" not in output:
        return False

    console.print()
    console.print("[yellow]Bisync requires a Resync.[/yellow]")

    if not confirm("Run Resync now? (Y/N): "):
        return False

    resync_command = build_command(
        job,
        execution_mode="resync",
    )

    resync_result, _ = execute_command(
        resync_command,
        require_confirm=False,
        show_preview=False,
        report=False,
    )

    if resync_result != 0:
        console.print(
            f"\n[red]Resync failed "
            f"(Exit Code {resync_result}).[/red]"
        )
        return False

    console.print("\n[green]Resync completed.[/green]")

    if not confirm("Run normal sync now? (Y/N): "):
        return False

    retry_result, _ = execute_command(
        command,
        require_confirm=False,
        show_preview=False,
        job_name=job.name,
    )

    return retry_result == 0

def execute_normal(job, confirm_before_run=True):

    ensure_local_folder(job)

    command = build_command(job)

    result, output = execute_command(
        command,
        require_confirm=confirm_before_run,
        job_name=job.name,
    )

    if result is None:
        return False

    if result == 0:
        return True

    return handle_resync_recovery(
        job,
        command,
        result,
        output,
    )

def execute_resync(job, confirm_before_run=True):

    ensure_local_folder(job)

    command = build_command(
        job,
        execution_mode="resync",
    )

    result, _ = execute_command(
        command,
        require_confirm=confirm_before_run,
        job_name=job.name,
    )

    return result == 0


def execute_force(job, confirm_before_run=True):

    ensure_local_folder(job)

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

    console.print()
    console.print("[bold yellow]Running Dry Run...[/bold yellow]\n")

    result, _ = execute_command(
        dry_run_command,
        require_confirm=False,
        report=False,
    )

    if result != 0:
        console.print(
            f"\n[red]Dry run failed (Exit Code {result}).[/red]"
        )
        return False

    console.print("\n[green]Dry Run completed.[/green]")

    command = build_command(
        job,
        execution_mode="force",
        conflict=conflict,
    )

    if confirm_before_run:

        console.print()
        console.print("[bold yellow]⚠ Force Sync[/bold yellow]")

        if conflict == "push":
            console.print(
                "[yellow]Direction: PUSH (local wins)[/yellow]"
            )
        else:
            console.print(
                "[yellow]Direction: PULL (cloud wins)[/yellow]"
            )

        if not confirm("Proceed with FORCE sync? (Y/N): "):
            return False

    result, _ = execute_command(
        command,
        require_confirm=False,
        job_name=job.name,
    )

    if result is None:
        return False

    return result == 0


def execute_selected_mode(
    job,
    execution_mode,
    confirm_before_run=True,
):

    if execution_mode == "cancel":
        console.print("\nCancelled.")
        return False

    if execution_mode not in {"normal", "resync", "force"}:
        console.print("[red]Invalid execution mode[/red]")
        return False

    valid, message = validate_job(job)

    if not valid:
        console.print(
            f"\n[red]Pre-flight check failed:[/red] {message}"
        )
        return False

    if execution_mode == "normal":
        return execute_normal(
            job,
            confirm_before_run=confirm_before_run,
        )

    if execution_mode == "resync":
        return execute_resync(
            job,
            confirm_before_run=confirm_before_run,
        )

    if execution_mode == "force":
        return execute_force(
            job,
            confirm_before_run=confirm_before_run,
        )

def execute_all(jobs):
    """
    Execute all applicable sync jobs using one selected execution mode.
    """

    start_time = time.time()

    console.print()
    console.print("[bold cyan]Sync All[/bold cyan]\n")

    execution_mode = select_execution_mode(
        next(
            job for job in jobs
            if job.mode == "bisync"
        )
    )

    if execution_mode == "cancel":
        console.print("\nCancelled.")
        return

    if execution_mode is None:
        console.print("\n[red]Invalid execution mode[/red]")
        return

    if execution_mode in {"resync", "force"}:
        jobs_to_run = [
            job for job in jobs
            if job.mode == "bisync"
        ]

        skipped_jobs = [
            job for job in jobs
            if job.mode != "bisync"
        ]

    else:
        jobs_to_run = jobs
        skipped_jobs = []

    console.print()

    if skipped_jobs:
        console.print(
            f"[yellow]{len(jobs_to_run)} bisync jobs will be processed.[/yellow]"
        )
        console.print(
            f"[yellow]{len(skipped_jobs)} non-bisync jobs will be skipped.[/yellow]"
        )

    else:
        console.print(
            f"[yellow]{len(jobs_to_run)} jobs will be processed.[/yellow]"
        )

    if not confirm("Run selected jobs? (Y/N): "):
        console.print("\nCancelled.")
        return

    successful = 0
    failed = 0
    results = []

    console.print()

    for index, job in enumerate(jobs_to_run, start=1):

        console.print(
            f"\n[bold cyan]"
            f"[{index}/{len(jobs_to_run)}] {job.name}"
            f"[/bold cyan]"
        )

        job_start_time = time.time()

        try:
            result = execute_selected_mode(
                job,
                execution_mode,
                confirm_before_run=False,
            )

            job_duration = time.time() - job_start_time

            if result:
                successful += 1
                results.append(
                    (job.name, "SUCCESS", job_duration)
                )
            else:
                failed += 1
                results.append(
                    (job.name, "FAILED", job_duration)
                )

        except Exception as error:
            job_duration = time.time() - job_start_time

            failed += 1
            results.append(
                (job.name, "FAILED", job_duration)
            )

            console.print(
                f"\n[red]Job failed:[/red] {error}"
            )

            console.print(
                "[yellow]Continuing to next job...[/yellow]"
            )

    total_seconds = int(time.time() - start_time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    console.print()
    console.print("[bold cyan]Sync All Complete[/bold cyan]\n")

    console.print(
        f"[green]✓ Successful: {successful}[/green]"
    )

    console.print(
        f"[red]✗ Failed: {failed}[/red]"
    )

    console.print(
        f"[cyan]⏱ Total time: "
        f"{minutes:02d}:{seconds:02d}[/cyan]"
    )

    if skipped_jobs:
        console.print(
            f"[yellow]⚠ Skipped: {len(skipped_jobs)}[/yellow]"
        )

    console.print()
    console.print("[bold cyan]Job Summary[/bold cyan]\n")

    for job_name, status, duration in results:

        if status == "SUCCESS":
            symbol = "✓"
            style = "green"
        else:
            symbol = "✗"
            style = "red"

        console.print(
            f"[{style}]{symbol} {job_name:<25} "
            f"{duration:>6.1f}s[/{style}]"
        )

def run():

    show_banner()

    jobs = load_jobs()
    show_status(jobs)

    while True:

        choice, groups, menu = show_main_menu(jobs)

        if choice == "Q":
            console.print("\nGoodbye!")
            return

        if choice == "A":
            execute_all(jobs)
            continue

        if choice == "L":
            show_sync_history()
            input("\nPress Enter to continue...")
            continue

        if choice not in menu:
            console.print("[red]Invalid selection[/red]")
            input("\nPress Enter to continue...")
            continue

        group = menu[choice]

        selected = select_job(group, groups[group])

        if selected is None:
            input("\nPress Enter to continue...")
            continue

        execution_mode = select_execution_mode(selected)

        execute_selected_mode(selected, execution_mode)

        input("\nPress Enter to continue...")
