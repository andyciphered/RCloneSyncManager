from rich.console import Console
from rich.panel import Panel

console = Console()


def show_banner():

    panel = Panel.fit(
        "[bold cyan]RClone Sync Manager[/bold cyan]\n"
        "[green]v0.2.0[/green]",
        border_style="cyan",
    )

    console.print(panel)