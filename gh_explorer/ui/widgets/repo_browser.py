#!/usr/bin/env python3
"""
Interactive repository browser widget
Written by Claude, I didnt even realize it was here.
"""
#TODO figure out whether it should be here
import time
from typing import Dict, Any, List, Optional
from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.live import Live
from rich.tree import Tree

class RepoBrowser:
    """Interactive browser for repository results with keyboard navigation."""
    
    def __init__(self, 
                 ctx: Dict[str, Any], 
                 repos: List[Dict[str, Any]]):
        """Initialize the repository browser."""
        self.ctx = ctx
        self.repos = repos
        self.console = ctx.get('CONSOLE')
        self.client = ctx.get('CLIENT')
        self.selected_index = 0
        self.repo_details: Optional[Dict[str, Any]] = None
        self.layout = self._create_layout()
        self.tree = None
        
    def _create_layout(self) -> Layout:
        """Create the layout for the browser."""
        layout = Layout()
        
        # Create a horizontal split
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main")
        )
        
        # Split the main area horizontally
        layout["main"].split_row(
            Layout(name="repos", minimum_size=30, ratio=1),
            Layout(name="content", ratio=2)
        )
        
        # Split the content area vertically
        layout["content"].split_column(
            Layout(name="details", size=8),
            Layout(name="readme")
        )
        
        return layout
    
    def _render_header(self) -> Panel:
        """Render the header section."""
        text = Text("GitHub Repository Browser", style="bold")
        text.append("\n")
        text.append("j/k or ↑/↓: Navigate  Enter/Space: Load details  q: Exit  o: Open in browser  c: Clone repo", style="dim")
        return Panel(text)
    
    def _render_repo_list(self) -> Panel:
        """Render the repository list section."""
        table = Table(show_header=False, expand=True, box=None)
        table.add_column("Repositories")
        
        for idx, repo in enumerate(self.repos):
            name = repo.get("fullName", "Unknown")
            stars = repo.get("stargazersCount", 0)
            stars_text = f"★ {stars}" if stars else ""
            
            if idx == self.selected_index:
                name_style = "bold reverse"
                star_style = "yellow reverse"
            else:
                name_style = "bold"
                star_style = "yellow"
            
            row = Text(f"{name}", style=name_style)
            if stars_text:
                row.append(" ")
                row.append(stars_text, style=star_style)
            
            table.add_row(row)
            
        return Panel(table, title="Repositories")
    
    def _render_repo_details(self) -> Panel:
        """Render the repository details section."""
        if not self.repo_details:
            selected_repo = self.repos[self.selected_index]
            details = Text(f"{selected_repo.get('fullName', 'Unknown')}")
            if selected_repo.get("description"):
                details.append(f"\n{selected_repo.get('description')}")
            if "language" in selected_repo and selected_repo["language"]:
                details.append(f"\nLanguage: ", style="dim")
                details.append(f"{selected_repo['language']}", style="green")
            stars = selected_repo.get("stargazersCount", 0)
            forks = selected_repo.get("forksCount", 0)
            details.append(f"\nStars: ", style="dim")
            details.append(f"{stars}", style="yellow")
            details.append(f"  Forks: ", style="dim")
            details.append(f"{forks}", style="cyan")
        else:
            # Full details view
            details = Text(f"{self.repo_details.get('nameWithOwner', 'Unknown')}", style="bold")
            if self.repo_details.get("description"):
                details.append(f"\n{self.repo_details.get('description')}")
            if "primaryLanguage" in self.repo_details and self.repo_details["primaryLanguage"]:
                details.append(f"\nLanguage: ", style="dim")
                details.append(f"{self.repo_details['primaryLanguage']}", style="green")
            stars = self.repo_details.get("stargazerCount", 0)
            forks = self.repo_details.get("forkCount", 0)
            details.append(f"\nStars: ", style="dim")
            details.append(f"{stars}", style="yellow")
            details.append(f"  Forks: ", style="dim")
            details.append(f"{forks}", style="cyan")
            if "url" in self.repo_details:
                details.append(f"\nURL: ", style="dim")
                details.append(f"{self.repo_details['url']}")
                
        return Panel(details, title="Details")
    
    def _render_readme(self) -> RenderableType:
        """Render the README section."""
        if not self.repo_details:
            return Panel(
                Text("Press Enter to load repository details and README"),
                title="README"
            )
        
        readme = self.repo_details.get("readme", {}).get("text", "No README available.")
        
        # Create the directory tree
        self.tree = Tree(f"📁 {self.repo_details.get('nameWithOwner', 'Unknown')}")
        try:
            self._populate_tree_with_files()
        except Exception:
            pass  # Silently fail on tree population errors
        
        # Split into horizontal layout - directory tree on left, readme on right
        content_layout = Layout()
        content_layout.split_row(
            Layout(Panel(self.tree, title="Files"), ratio=1),
            Layout(Panel(Markdown(readme), title="README"), ratio=2)
        )
        
        return content_layout
    
    def _populate_tree_with_files(self) -> None:
        """Populate the tree with repository files and directories."""
        if not self.tree:
            return
            
        try:
            repo_name = self.repo_details.get("nameWithOwner", "")
            if repo_name:
                # Get repository files using our client method
                files = self.client.get_repository_files(repo_name)
                
                # Add files to tree
                for file_info in files:
                    name = file_info.get("name", "")
                    file_type = file_info.get("type", "")
                    
                    if not name:
                        continue
                        
                    if file_type == "dir":
                        self.tree.add(f"📁 {name}")
                    else:
                        self.tree.add(f"📄 {name}")
                        
                # If no files were found or error occurred, add placeholder
                if not files:
                    raise Exception("No files found")
        except Exception:
            # Add some placeholder structure if we can't get the real one
            self.tree.add("📁 src")
            self.tree.add("📄 README.md")
            self.tree.add("📄 LICENSE")
            self.tree.add("[dim]Error loading repository structure[/dim]")
    
    def _fetch_repo_details(self) -> None:
        """Fetch detailed information for the selected repository."""
        selected_repo = self.repos[self.selected_index]
        repo_name = selected_repo.get("fullName", "")
        
        try:
            self.repo_details = self.client.get_repository(repo_name)
        except Exception as e:
            self.console.print(f"[danger]Error fetching repository details: {str(e)}[/danger]")
            self.repo_details = None
    
    def _compose_layout(self) -> Layout:
        """Compose the full layout with all components."""
        self.layout["header"].update(self._render_header())
        self.layout["repos"].update(self._render_repo_list())
        self.layout["details"].update(self._render_repo_details())
        self.layout["readme"].update(self._render_readme())
        
        return self.layout
    
    def run(self) -> None:
        """Run the interactive browser."""
        try:
            # Try to use better key handling with external library if available
            has_readchar = False
            try:
                import readchar
                has_readchar = True
            except ImportError:
                pass
                
            with Live(self._compose_layout(), console=self.console, screen=True, refresh_per_second=4) as live:
                running = True
                
                while running:
                    # Handle keys differently based on available libraries
                    if has_readchar:
                        # readchar provides better cross-platform key handling
                        key = readchar.readkey()
                        
                        # Map keys to actions
                        if key in ('q', '\x1b', readchar.key.ESC):  # q or ESC
                            running = False
                        elif key in (readchar.key.UP, 'k'):  # Up arrow or k
                            self.selected_index = max(0, self.selected_index - 1)
                            self.repo_details = None  # Reset details when changing selection
                        elif key in (readchar.key.DOWN, 'j'):  # Down arrow or j
                            self.selected_index = min(len(self.repos) - 1, self.selected_index + 1)
                            self.repo_details = None  # Reset details when changing selection
                        elif key == readchar.key.ENTER:  # Enter
                            if not self.repo_details:
                                self._fetch_repo_details()
                        elif key == 'o':  # Open in browser
                            self._open_in_browser()
                        elif key == 'c':  # Clone repo
                            self._clone_repository()
                    else:
                        # Fallback to simpler key handling
                        key = self.console.input("")
                        
                        # Handle just the basic keys
                        if key in ('q', 'Q'):
                            running = False
                        elif key in ('k', 'K'):
                            self.selected_index = max(0, self.selected_index - 1)
                            self.repo_details = None
                        elif key in ('j', 'J'):
                            self.selected_index = min(len(self.repos) - 1, self.selected_index + 1)
                            self.repo_details = None
                        elif key in ('o', 'O'):
                            self._open_in_browser()
                        elif key in ('c', 'C'):
                            self._clone_repository()
                        elif key in ('', ' ', '\r', '\n'):
                            if not self.repo_details:
                                self._fetch_repo_details()
                    
                    # Update the display
                    live.update(self._compose_layout())
                    time.sleep(0.1)  # Small delay to prevent CPU usage
                    
        except Exception as e:
            self.console.print(f"[danger]Error in interactive browser: {str(e)}[/danger]")
            
    def _open_in_browser(self) -> None:
        """Open the selected repository in the browser."""
        selected_repo = self.repos[self.selected_index]
        repo_name = selected_repo.get("fullName", "")
        if repo_name:
            self.client.open_in_browser(repo_name)
            message = Text("Opened in browser", style="success")
            self.console.print(message)
    
    def _clone_repository(self) -> None:
        """Clone the selected repository."""
        selected_repo = self.repos[self.selected_index]
        repo_name = selected_repo.get("fullName", "")
        if repo_name:
            try:
                result = self.client.clone_repository(repo_name)
                message = Text("Repository cloned successfully", style="success")
                self.console.print(message)
                # Pause briefly to show message
                time.sleep(1.5)
            except Exception as e:
                message = Text(f"Error cloning repository: {str(e)}", style="danger")
                self.console.print(message)
                time.sleep(1.5)
