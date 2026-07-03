from rich.console import Console
from rich.table import Table

from rcsm.services.health import check_rclone
from rcsm.services.config import load_jobs
from rcsm.ui.banner import show_banner

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
        "✅ Installed" if check_rclone() else "❌ Missing"
    )

    table.add_row(
        "Jobs",
        f"✅ {len(jobs)} Loaded"
    )

    console.print(table)

    console.print()

    console.print("[bold cyan]Available Jobs[/bold cyan]\n")

    for job in jobs:
        console.print(f"• {job['name']}")