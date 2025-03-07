#!/usr/bin/env python3
"""
Formatting utilities for GitHub Explorer
"""

import re
from typing import Dict, List, Any
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

def format_date(date_str: str) -> str:
    """Format a GitHub date string to a human-readable format."""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        now = datetime.now()
        delta = now - date
        
        if delta.days > 365:
            years = delta.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif delta.days > 30:
            months = delta.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
    except Exception:
        return date_str

def format_repo_list(repos: List[Dict[str, Any]]) -> Table:
    """Format a list of repositories as a Rich Table with a compact single-row format."""
    import shutil
    from rich.text import Text
    
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns
    
    # Adjust column widths based on terminal width - more conservative values
    # Use percentages of screen width for better adaptability
    repo_width = min(40, max(20, int(terminal_width * 0.3)))
    stars_width = 8  # Compact star count
    forks_width = 8  # Compact fork count
    
    # Calculate description width from remaining space
    desc_width = max(20, terminal_width - repo_width - stars_width - forks_width - 15)  # 15 for padding and spacing
    
    table = Table(
        show_header=True, 
        header_style="bold", 
        box=None, 
        width=terminal_width, 
        padding=(0, 1, 0, 0),  # Minimal padding
        collapse_padding=True,
        show_edge=False,
        expand=False  # Prevent automatic expansion
    )
    
    table.add_column("Repository", style="repo", width=repo_width, no_wrap=True)
    table.add_column("Stars", style="stars", justify="right", width=stars_width, no_wrap=True)
    table.add_column("Forks", style="forks", justify="right", width=forks_width, no_wrap=True)
    table.add_column("Description", width=desc_width, no_wrap=True)
    
    # Process each repository
    for repo in repos:
        name = repo.get("fullName", "Unknown")
        stars = str(repo.get("stargazersCount", 0))
        forks = str(repo.get("forksCount", 0))
        description = repo.get("description", "") or ""
        
        # Truncate repo name if needed
        if len(name) > repo_width:
            name = name[:repo_width-3] + "..."
            
        # Truncate description if too long
        if len(description) > desc_width:
            description = description[:desc_width-3] + "..."
        
        # Add a single row with all information
        table.add_row(name, stars, forks, description)
    
    return table

def format_repo_details(repo: Dict[str, Any]) -> Panel:
    """Format repository details as a Rich Panel with markdown content."""
    import shutil
    
    # Get terminal width for formatting
    terminal_width = shutil.get_terminal_size().columns
    
    name = repo.get("nameWithOwner", "Unknown")
    stars = repo.get("stargazerCount", 0)
    forks = repo.get("forkCount", 0)
    updated = format_date(repo.get("updatedAt", ""))
    description = repo.get("description", "") or "No description"
    url = repo.get("url", "")
    
    # Format language information
    primary_language = repo.get("primaryLanguage", {})
    lang_text = primary_language.get("name", "Not specified") if primary_language else "Not specified"
    
    # Build header text
    header_text = f"Repository: [repo]{name}[/repo]\n\n"
    header_text += f"[stars]★ {stars}[/stars]  [forks]⑂ {forks}[/forks]  Updated: [date]{updated}[/date]\n\n"
    header_text += f"URL: {url}\n\n"
    header_text += f"Languages: [language]{lang_text}[/language]\n\n"
    header_text += f"Description: {description}\n\n"
    
    # Process README if available to improve formatting
    readme = repo.get("readme", {}).get("text", "")
    if readme:
        # Format README for better terminal display
        from rich.markdown import Markdown
        
        # Truncate extremely long README files
        if len(readme) > 5000:
            readme = readme[:5000] + "\n\n... [README truncated for better display] ..."
        
        # Try to add some width constraints to tables and code blocks
        lines = readme.split("\n")
        formatted_lines = []
        in_code_block = False
        in_table = False
        
        for line in lines:
            # Handle code blocks
            if line.startswith("```"):
                in_code_block = not in_code_block
            
            # Handle tables
            if line.startswith("|") and not in_code_block:
                in_table = True
            elif in_table and not line.startswith("|"):
                in_table = False
            
            # Add the line with potential modifications
            if in_table and terminal_width < 100:
                # Simplify wide tables for narrow terminals
                if "|" in line:
                    cols = line.split("|")
                    if len(cols) > 4:  # If table has many columns
                        # Keep first few columns only
                        simplified = "|".join(cols[:3]) + "|...|"
                        formatted_lines.append(simplified)
                    else:
                        formatted_lines.append(line)
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        readme = "\n".join(formatted_lines)
        content = header_text + "## README\n\n" + readme
    else:
        content = header_text + "No README available."
    
    return Markdown(content)

def format_code_results(results: List[Dict[str, Any]]) -> Table:
    """Format code search results as a Rich Table with compact single-row format."""
    import shutil
    from rich.text import Text
    from rich.highlighter import RegexHighlighter
    
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns
    
    # Create a simple code highlighter
    class SimpleCodeHighlighter(RegexHighlighter):
        highlights = [r"(def|class|function|import|from|const|let|var)\b"]
    
    highlighter = SimpleCodeHighlighter()
    
    # Calculate column widths - more conservative for terminal constraints
    repo_width = min(30, max(15, int(terminal_width * 0.25)))
    path_width = min(25, max(10, int(terminal_width * 0.25)))
    match_width = max(20, terminal_width - repo_width - path_width - 10)  # 10 for padding
    
    table = Table(
        show_header=True, 
        header_style="bold", 
        box=None, 
        width=terminal_width, 
        padding=(0, 1, 0, 0),  # Minimal padding
        collapse_padding=True,
        show_edge=False,
        expand=False  # Prevent automatic expansion
    )
    
    table.add_column("Repository", style="repo", width=repo_width, no_wrap=True)
    table.add_column("File", style="bold", width=path_width, no_wrap=True)
    table.add_column("Match", style="cyan", width=match_width, no_wrap=True)
    
    for result in results:
        repo = result.get("repository", {}).get("nameWithOwner", "Unknown")
        path = result.get("path", "Unknown")
        
        # Truncate repo name if needed
        if len(repo) > repo_width:
            repo = repo[:repo_width-3] + "..."
            
        # Truncate path if needed
        if len(path) > path_width:
            # Try to keep the filename part
            if "/" in path:
                parts = path.split("/")
                filename = parts[-1]
                if len(filename) > path_width - 3:
                    # If filename itself is too long
                    path = "..." + filename[-(path_width-3):]
                else:
                    # Try to keep part of the path before the filename
                    remaining = path_width - len(filename) - 3
                    if remaining > 0:
                        path_prefix = "/".join(parts[:-1])
                        if len(path_prefix) > remaining:
                            path_prefix = "..." + path_prefix[-remaining:]
                        path = f"{path_prefix}/{filename}"
                    else:
                        path = "..." + filename
            else:
                path = path[:path_width-3] + "..."
        
        # Extract and clean up the text match
        matches = result.get("textMatches", [])
        match_text = ""
        if matches:
            match_text = matches[0].get("fragment", "")
            # Clean up - remove newlines and extra spaces
            match_text = re.sub(r'\s+', ' ', match_text).strip()
            # Truncate if needed
            if len(match_text) > match_width:
                match_text = match_text[:match_width-3] + "..."
        
        # Add a row with all the information
        table.add_row(repo, path, match_text)
    
    return table