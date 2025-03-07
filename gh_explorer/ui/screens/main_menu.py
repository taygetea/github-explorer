#!/usr/bin/env python3
"""
Main menu screen for GitHub Explorer
"""

from typing import Dict, Any
from rich.panel import Panel
from rich.text import Text

from gh_explorer.ui.screens.repo_search import search_repos_interactive
from gh_explorer.ui.screens.code_search import search_code_interactive

def display_main_menu(ctx: Dict[str, Any]) -> None:
    """Display the main menu and handle user selection."""
    console = ctx.get('CONSOLE')
    
    while True:
        # Display menu
        console.print()
        console.print(Panel(
            Text("📚 GitHub Explorer", style="bold"),
            subtitle="Shell-integrated GitHub tool"
        ))
        console.print()
        
        options = [
            ("1", "Search Repositories"),
            ("2", "Search Code"),
            ("3", "View Recent Repositories"),
            ("4", "Create a Gist"),
            ("5", "Search by Topic"),
            ("6", "Search by Language"),
            ("0", "Exit")
        ]
        
        for key, desc in options:
            console.print(f"  [bold]{key}[/bold]. {desc}")
        
        console.print()
        choice = console.input("Enter your choice (0-6): ")
        
        if choice == "0":
            console.print("[info]Exiting GitHub Explorer. Goodbye![/info]")
            break
        elif choice == "1":
            search_repos_interactive(ctx)
        elif choice == "2":
            search_code_interactive(ctx)
        elif choice == "3":
            console.print("[info]Feature not implemented yet[/info]")
        elif choice == "4":
            console.print("[info]Feature not implemented yet[/info]")
        elif choice == "5":
            console.print("[info]Feature not implemented yet[/info]")
        elif choice == "6":
            console.print("[info]Feature not implemented yet[/info]")
        else:
            console.print("[warning]Invalid choice. Please try again.[/warning]")
        
        # Wait for user acknowledgment after completing action
        if choice in ["3", "4", "5", "6"] or choice not in ["0", "1", "2"]:
            console.input("\nPress Enter to continue...")