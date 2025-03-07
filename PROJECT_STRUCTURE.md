# GitHub Explorer: Project Structure

## Directory Structure

```
gh-explorer/
├── gh_explorer/                       # Main package
│   ├── __init__.py
│   ├── app.py                        # Main application class
│   ├── config.py                     # Configuration and settings
│   ├── api/                          # GitHub API integration
│   │   ├── __init__.py
│   │   ├── client.py                 # GitHub CLI wrapper
│   │   ├── models.py                 # Data models
│   │   ├── cache.py                  # API response caching
│   │   └── parsers.py                # Response parsing utilities
│   │
│   ├── ui/                           # User interface components
│   │   ├── __init__.py
│   │   ├── styles.css                # Textual CSS styles
│   │   ├── screens/                  # Full-screen UIs
│   │   │   ├── __init__.py
│   │   │   ├── main_menu.py          # Main menu screen
│   │   │   ├── repo_search.py        # Repository search screen
│   │   │   ├── repo_view.py          # Repository viewer screen
│   │   │   ├── code_search.py        # Code search screen
│   │   │   ├── code_view.py          # Code viewer screen
│   │   │   ├── gist_creator.py       # Gist creation screen
│   │   │   └── settings.py           # Settings screen
│   │   │
│   │   ├── widgets/                  # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── repo_card.py          # Repository card widget
│   │   │   ├── search_bar.py         # Search input with suggestions
│   │   │   ├── markdown_viewer.py    # Markdown renderer
│   │   │   ├── file_browser.py       # File navigation tree
│   │   │   ├── code_preview.py       # Syntax-highlighted code
│   │   │   └── stats_panel.py        # Repository statistics
│   │   │
│   │   └── dialogs/                  # Popup dialogs
│   │       ├── __init__.py
│   │       ├── filter_dialog.py      # Search filter dialog
│   │       ├── clone_dialog.py       # Repository clone dialog
│   │       └── confirmation.py       # Confirmation dialog
│   │
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── formatting.py             # Text formatting utilities
│   │   ├── terminal.py               # Terminal capability detection
│   │   └── logger.py                 # Logging utilities
│   │
│   └── data/                         # Data management
│       ├── __init__.py
│       ├── db.py                     # SQLite database interface
│       ├── history.py                # Search and view history
│       ├── favorites.py              # User favorites
│       └── schema.py                 # Database schema
│
├── bin/                             # Command-line scripts
│   └── gh-explorer                  # Entry point script
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_api.py                  # API tests
│   ├── test_models.py               # Data model tests
│   ├── test_ui.py                   # UI tests
│   └── fixtures/                    # Test fixtures
│       ├── __init__.py
│       ├── repositories.json        # Sample repository data
│       ├── code_samples.json        # Sample code search results
│       └── readme_samples.md        # Sample README content
│
├── docs/                            # Documentation
│   ├── index.md                     # Main documentation
│   ├── installation.md              # Installation guide
│   ├── usage.md                     # Usage guide
│   ├── api.md                       # API documentation
│   └── screenshots/                 # UI screenshots
│
├── .github/                         # GitHub-specific files
│   └── workflows/                   # GitHub Actions
│       ├── tests.yml                # Run tests on PRs
│       └── release.yml              # Create releases
│
├── README.md                        # Project overview
├── DEVELOPMENT_PLAN.md              # Development roadmap
├── requirements.txt                 # Python dependencies
├── setup.py                         # Package installation
└── pyproject.toml                   # Project metadata and configs
```

## Key Components

### Main Application

The `app.py` file serves as the entry point and contains the main `GitHubExplorer` class that:
- Initializes Textual
- Sets up screens
- Manages navigation
- Handles global keybindings

```python
from textual.app import App
from textual.binding import Binding

from gh_explorer.ui.screens.main_menu import MainMenuScreen
from gh_explorer.ui.screens.repo_search import RepoSearchScreen
# ... more imports

class GitHubExplorer(App):
    """A TUI for exploring GitHub."""

    CSS_PATH = "ui/styles.css"
    TITLE = "GitHub Explorer"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "toggle_help", "Help"),
        Binding("ctrl+s", "toggle_sidebar", "Sidebar"),
        # ... more global bindings
    ]
    
    def __init__(self):
        super().__init__()
        self.api_client = GitHubClient()
        self.history = SearchHistory()
        
    def on_mount(self):
        """Called when app is mounted."""
        # Push the main menu screen
        self.push_screen(MainMenuScreen())
        
    async def action_toggle_help(self):
        """Show the help screen."""
        # ... implementation

    async def action_toggle_sidebar(self):
        """Toggle the visibility of the sidebar."""
        # ... implementation
```

### Repository View Screen

The `repo_view.py` file contains the screen for viewing repository details:

```python
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from gh_explorer.ui.widgets.markdown_viewer import MarkdownViewer
from gh_explorer.ui.widgets.stats_panel import StatsPanel
from gh_explorer.ui.widgets.file_browser import FileBrowser


class RepoViewScreen(Screen):
    """A screen that displays repository details."""

    def __init__(self, repo_full_name):
        super().__init__()
        self.repo_full_name = repo_full_name
        self.repo_data = None
        
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Horizontal():
            with VerticalScroll():
                yield Static(id="repo-title")
                yield Static(id="repo-description")
                yield Static(id="repo-stats")
                yield MarkdownViewer(id="readme-content")
            
            yield StatsPanel(id="stats-panel")
            
        yield FileBrowser(id="file-browser")
        yield Footer()
        
    async def on_mount(self):
        """Called when screen is mounted."""
        # Fetch repository data
        self.repo_data = await self.app.api_client.get_repository(self.repo_full_name)
        
        # Update UI with repository data
        self.query_one("#repo-title").update(f"# {self.repo_data['name']}")
        self.query_one("#repo-description").update(self.repo_data['description'])
        
        # ... update other widgets
        
        # Fetch and render README
        readme = await self.app.api_client.get_readme(self.repo_full_name)
        self.query_one("#readme-content").update(readme)
```

### GitHub API Client

The `client.py` file handles interaction with the GitHub API through the GitHub CLI:

```python
import json
import subprocess
from typing import Dict, List, Optional, Any, Union

from gh_explorer.api.models import Repository, SearchResults
from gh_explorer.api.cache import ApiCache


class GitHubClient:
    """Client for interacting with GitHub through the GitHub CLI."""
    
    def __init__(self):
        self.cache = ApiCache()
        
    async def run_command(self, args: List[str]) -> str:
        """Run a gh command and return the output."""
        proc = await subprocess.create_subprocess_exec(
            "gh", *args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode \!= 0:
            raise Exception(f"Command failed: {stderr.decode()}")
            
        return stdout.decode()
        
    async def search_repositories(
        self, 
        query: str, 
        limit: int = 20,
        sort: Optional[str] = None,
        language: Optional[str] = None,
        topic: Optional[str] = None
    ) -> SearchResults:
        """Search for repositories matching query."""
        # Check cache first
        cache_key = f"search:repos:{query}:{limit}:{sort}:{language}:{topic}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
            
        # Build command arguments
        args = ["search", "repos", query, "--json", "fullName,description,stargazersCount,forksCount,updatedAt"]
        
        if limit:
            args.extend(["--limit", str(limit)])
        if sort:
            args.extend(["--sort", sort])
        if language:
            args.extend(["--language", language])
        if topic:
            args.extend(["--topic", topic])
            
        # Execute command
        output = await self.run_command(args)
        results = json.loads(output)
        
        # Convert to model
        repos = [Repository.from_dict(r) for r in results]
        search_results = SearchResults(query=query, items=repos)
        
        # Cache results
        self.cache.set(cache_key, search_results)
        
        return search_results
    
    async def get_repository(self, full_name: str) -> Repository:
        """Get detailed information about a repository."""
        # ... implementation
        
    async def get_readme(self, full_name: str) -> str:
        """Get the README content for a repository."""
        # ... implementation
        
    async def search_code(self, query: str, limit: int = 20) -> SearchResults:
        """Search for code matching query."""
        # ... implementation
```

### Rich Markdown Viewer Widget

The `markdown_viewer.py` file provides a widget for rendering Markdown content:

```python
from rich.console import RenderableType
from rich.markdown import Markdown
from textual.widgets import Static


class MarkdownViewer(Static):
    """A widget for displaying rendered markdown."""
    
    def __init__(self, markdown_text="", **kwargs):
        super().__init__("", **kwargs)
        self.markdown_text = markdown_text
        
    def update(self, markdown_text: str) -> None:
        """Update the markdown content."""
        self.markdown_text = markdown_text
        self.refresh()
        
    def render(self) -> RenderableType:
        """Render the markdown content."""
        return Markdown(self.markdown_text)
```

## Data Flow

1. **User Input**
   - User interacts with UI through key presses or mouse clicks
   - Textual handles input and dispatches events to appropriate handlers

2. **Action Handling**
   - Screen or widget processes the action
   - May trigger API calls or navigation

3. **API Interaction**
   - GitHubClient executes commands via GitHub CLI
   - Results are parsed and converted to models
   - Responses are cached as appropriate

4. **UI Update**
   - Models are passed to UI components
   - Screens and widgets refresh to display new data

5. **Persistent Storage**
   - History and favorites are stored in SQLite
   - Configuration is saved to config file

## Key User Flows

1. **Repository Search Flow**
   - User navigates to search screen
   - Enters search terms
   - Filters and sorts results
   - Selects a repository to view
   - Views repository details
   - May star, watch, or clone repository

2. **Code Exploration Flow**
   - User navigates file browser in repository view
   - Selects a file to view
   - Views syntax-highlighted code
   - May navigate to different files or directories

3. **Gist Creation Flow**
   - User navigates to gist creation screen
   - Enters content or selects a file
   - Adds description and visibility settings
   - Creates gist
   - Views created gist URL or content
