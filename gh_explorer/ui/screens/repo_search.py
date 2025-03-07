#!/usr/bin/env python3
"""
Repository search screen for GitHub Explorer
"""

from typing import Dict, Any, List
from rich.panel import Panel
from rich.text import Text

from gh_explorer.utils.formatting import format_repo_list

def search_repos_interactive(ctx: Dict[str, Any]) -> None:
    """Interactive repository search."""
    console = ctx.get('CONSOLE')
    client = ctx.get('CLIENT')
    
    # Get search terms
    console.print()
    query = console.input("Enter search terms: ")
    
    if not query:
        console.print("[warning]Search cancelled.[/warning]")
        return
    
    # Allow filtering options
    console.print()
    console.print("[bold]Filter options (press Enter to skip):[/bold]")
    language = console.input("Language: ")
    topic = console.input("Topic: ")
    sort_options = {
        "1": "stars",
        "2": "forks",
        "3": "updated",
        "": "stars"  # Default
    }
    sort_choice = console.input("Sort by ([1] Stars, [2] Forks, [3] Recently updated): ")
    sort = sort_options.get(sort_choice, "stars")
    
    limit = 20
    try:
        limit_input = console.input(f"Number of results (default {limit}): ")
        if limit_input:
            limit = int(limit_input)
    except ValueError:
        console.print(f"[warning]Invalid number, using default ({limit}).[/warning]")
    
    # Perform search
    console.print()
    console.print(f"[info]Searching for repositories: [/info][repo]{query}[/repo]")
    if language:
        console.print(f"[info]Language: [/info][language]{language}[/language]")
    if topic:
        console.print(f"[info]Topic: [/info]{topic}")
    console.print(f"[info]Sorting by: [/info]{sort}")
    console.print()
    
    try:
        repos = client.search_repositories(
            query=query, 
            limit=limit,
            language=language if language else None,
            topic=topic if topic else None,
            sort=sort
        )
        
        if not repos:
            console.print("[warning]No repositories found matching your criteria.[/warning]")
            return
        
        # Display results
        table = format_repo_list(repos)
        console.print(table)
        console.print()
        
        # Let user select a repo to view
        view_repo_details(ctx, repos)
        
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")

def view_repo_details(ctx: Dict[str, Any], repos: List[Dict[str, Any]]) -> None:
    """Allow user to select and view repository details."""
    console = ctx.get('CONSOLE')
    client = ctx.get('CLIENT')
    
    while True:
        choice = console.input(
            "Enter number to view, 'f' for filters, 's' for sort, or 'q' to return: "
        )
        
        if choice.lower() == 'q':
            return
        elif choice.lower() == 'f':
            console.print("[info]Filter option not implemented yet[/info]")
            continue
        elif choice.lower() == 's':
            console.print("[info]Sort option not implemented yet[/info]")
            continue
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(repos):
                selected_repo = repos[idx]["fullName"]
                
                # Get detailed repo information
                console.print()
                console.print(f"[info]Fetching details for: [/info][repo]{selected_repo}[/repo]")
                repo_details = client.get_repository(selected_repo)
                
                # Show repo info
                from gh_explorer.utils.formatting import format_repo_details
                formatted = format_repo_details(repo_details)
                console.print(formatted)
                
                # Show options
                console.print()
                console.print("[bold]Options:[/bold]")
                console.print("  [bold]1[/bold]. Open in browser")
                console.print("  [bold]2[/bold]. Clone repository")
                console.print("  [bold]3[/bold]. Back to search results")
                
                action = console.input("\nEnter choice (1-3): ")
                
                if action == '1':
                    client.open_in_browser(selected_repo)
                    console.print("[success]Opened in browser.[/success]")
                elif action == '2':
                    console.print(f"[info]Cloning {selected_repo}...[/info]")
                    result = client.clone_repository(selected_repo)
                    console.print(f"[success]{result}[/success]")
                    return  # Return to main menu after cloning
                else:
                    # Back to search results
                    continue
            else:
                console.print("[warning]Invalid selection. Please try again.[/warning]")
        except ValueError:
            console.print("[warning]Please enter a number, 'f', 's', or 'q'.[/warning]")