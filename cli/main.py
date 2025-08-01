"""
Main CLI entry point for the Rain application - Beautiful system information tool.
"""

import sys
from typing import List, Optional

import click
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import DOUBLE
from rich import print as rprint

from core.robust_collector import RobustSystemCollector
from core.config import Config
from core.display import DisplayManager
from utils.exceptions import RainError
from utils.logger import setup_logging

# Import version from main package
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from __init__ import __version__

# Install rich traceback handler for better error display
install(show_locals=True)

console = Console()


def print_banner():
    """Print a beautiful banner for """
    banner_text = Text.assemble(
        ("🌧️ ", "bold blue"),
        ("RAIN", "bold cyan"),
        (" 🌧️", "bold blue")
    )
    
    subtitle = Text("Comprehensive System Information Tool", style="italic bright_white")
    version_text = Text(f"v{__version__}", style="dim")
    
    banner_panel = Panel(
        Align.center(Text.assemble(banner_text, "\n", subtitle, "\n", version_text)),
        box=DOUBLE,
        border_style="bright_blue",
        padding=(1, 2),
        title="[bold bright_cyan]Welcome[/bold bright_cyan]",
        title_align="center"
    )
    
    console.print()
    console.print(banner_panel)
    console.print()


def print_goodbye():
    """Print a beautiful goodbye message."""
    goodbye_panel = Panel(
        Align.center(Text("Thank you for using Rain! 🌧️✨", style="bold bright_green")),
        box=DOUBLE,
        border_style="bright_green",
        padding=(0, 2)
    )
    console.print(goodbye_panel)


@click.command()
@click.option(
    "-s",
    "--section",
    multiple=True,
    type=click.Choice([
        "system", "hardware", "network", "processes", 
        "security", "sensors", "python", "all"
    ]),
    help="🎯 Display specific section(s) only",
)
@click.option(
    "-l", "--live", is_flag=True, help="📊 Enable live monitoring mode"
)
@click.option(
    "-j", "--json", "output_json", is_flag=True, help="📄 Output in JSON format"
)
@click.option(
    "--save", type=click.Path(), help="💾 Save output to file"
)
@click.option(
    "-v", "--verbose", is_flag=True, help="🔍 Enable verbose logging"
)
@click.option(
    "--config", type=click.Path(exists=True), help="⚙️ Custom configuration file path"
)
@click.option(
    "--no-banner", is_flag=True, help="🚫 Skip the banner display"
)
@click.version_option(version=__version__, prog_name="rain")
def main(
    section: List[str],
    live: bool,
    output_json: bool,
    save: Optional[str],
    verbose: bool,
    config: Optional[str],
    no_banner: bool,
) -> None:
    """
    🌧️ Rain - Comprehensive System Information CLI Tool
    
    Display every piece of knowable information about your computer
    in a beautiful, interactive terminal interface.
    
    \b
    Examples:
      rain                    # Show all system information
      rain -s system          # Show only system information  
      rain -s hardware -s network  # Show hardware and network
      rain --live             # Live monitoring mode
      rain --json             # Output as JSON
      rain --save report.txt  # Save to file
    """
    try:
        # Setup logging - suppress for JSON output
        if output_json:
            setup_logging(verbose, suppress_output=True)
        else:
            setup_logging(verbose)
        
        # Show banner unless disabled or in JSON/save mode
        if not no_banner and not output_json and not save:
            print_banner()
        
        # Load configuration
        app_config = Config.create(config_path=config)
        
        # Determine sections to display
        sections_to_show = list(section) if section else app_config.default_sections
        if "all" in sections_to_show:
            sections_to_show = [
                "system", "hardware", "network", "processes", 
                "security", "sensors", "python"
            ]
        
        # Initialize components
        collector = RobustSystemCollector(config=app_config)
        display_manager = DisplayManager(config=app_config, console=console)
        
        if live:
            # Live monitoring mode
            if not no_banner:
                rprint("[dim]Starting live monitoring... Press Ctrl+C to exit[/dim]\n")
            display_manager.run_live_monitor(collector, sections_to_show)
        else:
            # Single run mode
            if not output_json and not save and not no_banner:
                with console.status("[bold blue]Collecting system information...", spinner="dots"):
                    data = collector.collect_all_data(sections_to_show)
            else:
                data = collector.collect_all_data(sections_to_show)
            
            if output_json:
                display_manager.output_json(data)
            elif save:
                display_manager.save_to_file(data, save, sections_to_show)
                if not no_banner:
                    console.print(f"[green]✅ Report saved to {save}[/green]")
            else:
                display_manager.display_all(data, sections_to_show)
        
        # Show goodbye message
        if not no_banner and not output_json and not save and not live:
            print_goodbye()
                
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Operation cancelled by user.[/yellow]")
        if not no_banner:
            print_goodbye()
        sys.exit(0)
    except RainError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]💥 Unexpected error: {e}[/red]")
        if verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
