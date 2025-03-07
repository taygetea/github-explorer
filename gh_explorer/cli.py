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
@click.argument('query', required=False)
@click.option('--limit', '-l', default=20, help='Maximum number of results')
@click.option('--language', help='Filter by programming language')
@click.option('--topic', help='Filter by topic')
@click.option('--sort', type=click.Choice(['stars', 'forks', 'updated']), 
              default='stars', help='Sort results by')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
@click.pass_context
def search_repos(ctx, query, limit, language, topic, sort, json_output):
    """Search for GitHub repositories"""
    if not query:
        # If no query provided, go to interactive mode
        search_repos_interactive(ctx.obj)
        return
    
    client = ctx.obj['CLIENT']
    console = ctx.obj['CONSOLE']
    
    console.print(f"[info]Searching for repositories: [/info][repo]{query}[/repo]")
    
    repos = client.search_repositories(
        query=query, 
        limit=limit,
        language=language,
        topic=topic,
        sort=sort
    )
    
    if json_output:
        import json
        console.print(json.dumps(repos))
    else:
        formatted = format_repo_list(repos)
        console.print(formatted)

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
@click.argument('query', required=True)
@click.option('--limit', '-l', default=20, help='Maximum number of results')
@click.option('--language', help='Filter by programming language')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
@click.pass_context
def search_code(ctx, query, limit, language, json_output):
    """Search for code in GitHub repositories"""
    client = ctx.obj['CLIENT']
    console = ctx.obj['CONSOLE']
    
    console.print(f"[info]Searching for code: [/info]{query}")
    
    results = client.search_code(
        query=query,
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
    try:
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