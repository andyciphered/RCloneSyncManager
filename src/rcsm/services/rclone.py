import subprocess

from rich.console import Console

from rcsm.models.job import SyncJob
from rcsm.services.command_builder import build_command

console = Console()


def execute(job: SyncJob):

    command = build_command(job)

    console.print("\n[bold green]Executing...[/bold green]\n")

    console.print(" ".join(command))
    console.print()

    process = subprocess.Popen(command)

    process.wait()

    return process.returncode