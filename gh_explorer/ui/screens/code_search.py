#!/usr/bin/env python3
"""
Code search screen for GitHub Explorer
"""

from typing import Dict, Any, List
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from gh_explorer.utils.formatting import format_code_results

def search_code_interactive(ctx: Dict[str, Any]) -> None:
    """Interactive code search."""
    console = ctx.get('CONSOLE')
    client = ctx.get('CLIENT')
    
    # Get search terms
    console.print()
    query = console.input("Enter code search terms: ")
    
    if not query:
        console.print("[warning]Search cancelled.[/warning]")
        return
    
    # Allow filtering options
    console.print()
    console.print("[bold]Filter options (press Enter to skip):[/bold]")
    language = console.input("Language: ")
    
    limit = 15
    try:
        limit_input = console.input(f"Number of results (default {limit}): ")
        if limit_input:
            limit = int(limit_input)
    except ValueError:
        console.print(f"[warning]Invalid number, using default ({limit}).[/warning]")
    
    # Perform search
    console.print()
    console.print(f"[info]Searching for code: [/info]{query}")
    if language:
        console.print(f"[info]Language: [/info][language]{language}[/language]")
    console.print()
    
    try:
        results = client.search_code(
            query=query, 
            limit=limit,
            language=language if language else None
        )
        
        if not results:
            console.print("[warning]No code found matching your criteria.[/warning]")
            return
        
        # Display results
        table = format_code_results(results)
        console.print(table)
        console.print()
        
        # Let user select code to view
        view_code_details(ctx, results)
        
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")

def view_code_details(ctx: Dict[str, Any], results: List[Dict[str, Any]]) -> None:
    """Allow user to select and view code details."""
    console = ctx.get('CONSOLE')
    client = ctx.get('CLIENT')
    
    while True:
        choice = console.input(
            "Enter number to view or 'q' to return: "
        )
        
        if choice.lower() == 'q':
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                result = results[idx]
                repo = result.get("repository", {}).get("nameWithOwner", "Unknown")
                path = result.get("path", "Unknown")
                
                # Show code info
                console.print()
                console.print(f"[repo]{repo}[/repo]: [bold]{path}[/bold]")
                
                # Show match
                matches = result.get("textMatches", [])
                if matches:
                    fragment = matches[0].get("fragment", "")
                    
                    # Try to determine language from file extension
                    lang = "text"
                    if "." in path:
                        ext = path.split(".")[-1].lower()
                        if ext in ["py", "js", "ts", "go", "java", "rb", "c", "cpp", "cs", "php", "html", "css"]:
                            lang = ext
                    
                    # Syntax highlight the fragment
                    syntax = Syntax(fragment, lang, theme="monokai", line_numbers=True)
                    console.print(syntax)
                
                # Show options
                console.print()
                console.print("[bold]Options:[/bold]")
                console.print("  [bold]1[/bold]. Open repository in browser")
                console.print("  [bold]2[/bold]. Search in this repository")
                console.print("  [bold]3[/bold]. Back to search results")
                
                action = console.input("\nEnter choice (1-3): ")
                
                if action == '1':
                    client.open_in_browser(repo)
                    console.print("[success]Opened in browser.[/success]")
                elif action == '2':
                    console.print("[info]Feature not implemented yet[/info]")
                else:
                    # Back to search results
                    continue
            else:
                console.print("[warning]Invalid selection. Please try again.[/warning]")
        except ValueError:
            console.print("[warning]Please enter a number or 'q'.[/warning]")