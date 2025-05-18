#!/usr/bin/env python3
"""
GitHub Explorer CLI - A shell-integrated tool for exploring GitHub
"""

import sys
import os
import click
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

from gh_explorer.api.client import GitHubClient
from gh_explorer.utils.formatting import format_repo_list, format_repo_details
from gh_explorer.ui.screens.main_menu import display_main_menu
from gh_explorer.ui.screens.repo_search import search_repos_interactive

# Set up Rich console
console = Console(theme=Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "green",
    "repo": "bold blue",
    "stars": "yellow",
    "forks": "cyan",
    "language": "green",
    "date": "dim white",
}))

@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False, help='Enable debug mode')
@click.pass_context
def cli(ctx, debug):
    """GitHub Explorer (ghx) - Shell-integrated GitHub exploration tool"""
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['CLIENT'] = GitHubClient()
    ctx.obj['CONSOLE'] = console
    
    if ctx.invoked_subcommand is None:
        # No subcommand was specified, run interactive mode
        display_main_menu(ctx.obj)

@cli.command()
@click.argument('query', required=False, nargs=-1)
@click.option('--limit', '-l', default=20, help='Maximum number of results')
@click.option('--language', help='Filter by programming language')
@click.option('--topic', help='Filter by topic')
@click.option('--sort', type=click.Choice(['stars', 'forks', 'updated']), 
              default='stars', help='Sort results by')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
@click.pass_context
def search_repos(ctx, query, limit, language, topic, sort, json_output):
    """Search for GitHub repositories"""
    # Convert tuple of arguments to a space-separated string if provided
    query_str = ' '.join(query) if query else ''
    
    if not query_str:
        # If no query provided, go to interactive mode
        search_repos_interactive(ctx.obj)
        return
    
    client = ctx.obj['CLIENT']
    console = ctx.obj['CONSOLE']
    
    console.print(f"[info]Searching for repositories: [/info][repo]{query_str}[/repo]")
    
    repos = client.search_repositories(
        query=query_str, 
        limit=limit,
        language=language,
        topic=topic,
        sort=sort
    )
    
    if json_output:
        import json
        console.print(json.dumps(repos))
    else:
        # Always use the simple output mode for now
        # Until we can properly debug the terminal capabilities
        from gh_explorer.utils.formatting import format_repo_list
        formatted = format_repo_list(repos)
        console.print(formatted)
        
        # Only prompt in interactive mode
        if sys.stdin.isatty():
            console.print()
            try:
                choice = console.input("Enter number to view or press Enter to exit: ")
                if choice and choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(repos):
                        repo_name = repos[idx]["fullName"]
                        client = ctx.obj['CLIENT']
                        repo_details = client.get_repository(repo_name)
                        from gh_explorer.utils.formatting import format_repo_details
                        formatted = format_repo_details(repo_details)
                        console.print(formatted)
            except (EOFError, KeyboardInterrupt):
                # Handle terminal input errors gracefully
                pass

@cli.command()
@click.argument('repo', required=True)
@click.option('--web', is_flag=True, help='Open in web browser')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
@click.pass_context
def view_repo(ctx, repo, web, json_output):
    """View details of a GitHub repository"""
    client = ctx.obj['CLIENT']
    console = ctx.obj['CONSOLE']
    
    if web:
        # Open in web browser
        client.open_in_browser(repo)
        return
    
    console.print(f"[info]Fetching repository details for: [/info][repo]{repo}[/repo]")
    
    repo_details = client.get_repository(repo)
    
    if json_output:
        import json
        console.print(json.dumps(repo_details))
    else:
        formatted = format_repo_details(repo_details)
        console.print(formatted)

@cli.command()
@click.argument('query', required=True, nargs=-1)
@click.option('--limit', '-l', default=20, help='Maximum number of results')
@click.option('--language', help='Filter by programming language')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
@click.pass_context
def search_code(ctx, query, limit, language, json_output):
    """Search for code in GitHub repositories"""
    # Convert tuple of arguments to a space-separated string
    query_str = ' '.join(query)
    
    client = ctx.obj['CLIENT']
    console = ctx.obj['CONSOLE']
    
    console.print(f"[info]Searching for code: [/info]{query_str}")
    
    results = client.search_code(
        query=query_str,
        limit=limit,
        language=language
    )
    
    if json_output:
        import json
        console.print(json.dumps(results))
    else:
        from gh_explorer.utils.formatting import format_code_results
        formatted = format_code_results(results)
        console.print(formatted)

def main():
    """Main entry point for the CLI"""
    import signal
    
    # Handle keyboard interrupts (Ctrl+C) gracefully
    def signal_handler(sig, frame):
        console.print("\n[info]Exiting GitHub Explorer. Goodbye![/info]")
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Set environment variable for proper Escape key handling in terminal
        os.environ["ESCDELAY"] = "25"  # 25ms delay for escape key (faster response)
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[info]Exiting GitHub Explorer. Goodbye![/info]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        if os.environ.get("GHX_DEBUG"):
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()