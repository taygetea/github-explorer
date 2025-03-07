# GitHub Explorer: Development Plan

## Overview

GitHub Explorer aims to provide an enhanced, shell-integrated experience for exploring, searching, and interacting with GitHub repositories, code, and gists. Instead of remembering complex command-line arguments, users can navigate through intuitive menus while maintaining the composability and integration with the shell environment.

## Vision

Create a powerful "package manager"-like experience for GitHub exploration that makes discovery and interaction delightful in a terminal environment, without sacrificing the flexibility and composability of command-line tools. GitHub Explorer should feel like an extension of your shell rather than a separate application.

## Technology Stack

- **Text Formatting:** [Rich](https://github.com/Textualize/rich) - For beautiful terminal formatting and structured output
- **Menu System:** Simple interactive menus using Python's built-in input handling
- **Backend:** GitHub CLI (gh) - For authenticated GitHub API access
- **Terminal Utilities:** [pyfzf](https://github.com/nk412/pyfzf) or similar - For fuzzy finding when needed
- **Data Storage:** Simple JSON files - For storing history and configuration

## Features Roadmap

### Phase 1: Core Experience

- [x] Basic menu navigation
- [x] Repository search
- [x] Simple repository viewing
- [x] Code search
- [x] Topic & language search
- [x] Gist creation

### Phase 2: Rich Repository Exploration

- [ ] **Repository Browser**
  - Display repository details in a multi-panel interface
  - Show README with proper markdown rendering
  - Display repository stats, languages, and topics
  - Show directory structure in tree view
  - Support navigation through directories
  - Code viewing with syntax highlighting
  - Commit history browsing

- [ ] **Enhanced Search**
  - Real-time search suggestions
  - Filters panel for refining search results
  - Sort options (stars, forks, recently updated)
  - Advanced search query builder
  - Search history and saved searches

- [ ] **User Management**
  - User profile viewing
  - Follow/unfollow users
  - View user's repositories, stars, and followers

### Phase 3: GitHub Workflows

- [ ] **Issues & Pull Requests**
  - Browse issues with filters and sorting
  - View issue details, comments, and history
  - Browse pull requests
  - PR diff viewer with syntax highlighting
  - Comment on issues and PRs

- [ ] **Repository Management**
  - Star/unstar repositories
  - Watch/unwatch repositories
  - Fork repositories
  - Create new repositories
  - Edit repository settings

- [ ] **Gist Management**
  - Browse personal and public gists
  - Edit and update gists
  - Star gists
  - Fork gists

### Phase 4: Advanced Features

- [ ] **Trending Explorer**
  - Browse trending repositories by day, week, month
  - Filter trending by language
  - Discover new developers to follow

- [ ] **GitHub Actions**
  - View workflow runs
  - Trigger workflows
  - Monitor build status

- [ ] **GitHub Notifications**
  - View and manage notifications
  - Mark as read/unread
  - Filter by type
  - Action buttons appropriate to notification type

## UI Design

### Output Patterns

1. **Menu Navigation**
   ```
   GitHub Explorer
   
   1. Search Repositories
   2. Search Code
   3. Browse Recent Repositories
   4. Create a Gist
   5. Search by Topic
   6. Search by Language
   0. Exit
   
   Enter your choice (0-6): 
   ```

2. **Repository Search Output**
   ```
   GitHub Repository Search: "terminal ui"
   
   1. textual/textual
      ★ 18.2k  |  ⑂ 642  |  Updated 2 days ago
      Textual is a TUI framework for Python inspired by modern web development.
      
   2. charmbracelet/bubbletea
      ★ 17.4k  |  ⑂ 528  |  Updated 1 day ago
      A powerful little TUI framework for Go
      
   3. rivo/tview
      ★ 8.3k  |  ⑂ 455  |  Updated 3 weeks ago
      Terminal UI library with rich interactive widgets for Go
      
   4. peterbrittain/asciimatics
      ★ 3.2k  |  ⑂ 241  |  Updated 2 months ago
      A cross platform package to do curses-like operations, plus higher level APIs
      
   Enter number to view, 'f' for filters, 's' for sort, or 'q' to return: 
   ```

3. **Repository Details Output**
   ```
   ╭─ textual/textual ──────────────────────────────────────────────────╮
   │                                                                     │
   │ Textual: TUI Framework for Python                                   │
   │                                                                     │
   │ ★ 18.2k  |  ⑂ 642  |  👀 131 watchers  |  MIT License              │
   │                                                                     │
   │ Description:                                                        │
   │ Textual is a TUI (Text User Interface) framework for Python         │
   │ inspired by modern web development.                                 │
   │                                                                     │
   │ Languages: Python (85.2%), TypeScript (10.4%), Other (4.4%)         │
   │                                                                     │
   │ README:                                                             │
   │ # Textual                                                           │
   │                                                                     │
   │ A TUI (Text User Interface) framework for Python inspired by        │
   │ modern web development.                                             │
   │                                                                     │
   │ <more README content with syntax highlighting>                      │
   │                                                                     │
   ╰─────────────────────────────────────────────────────────────────────╯
   
   Options:
   1. View files
   2. Open in browser
   3. Clone repository
   4. Star/unstar repository
   5. Back to search results
   
   Enter your choice (1-5): 
   ```

4. **Command Outputs**
   ```
   $ ghx search-repos "terminal ui"
   
   GitHub Repository Search: "terminal ui"
   
   1. textual/textual
      ★ 18.2k  |  ⑂ 642  |  Updated 2 days ago
      Textual is a TUI framework for Python inspired by modern web development.
      
   2. charmbracelet/bubbletea
      ★ 17.4k  |  ⑂ 528  |  Updated 1 day ago
      A powerful little TUI framework for Go
   
   ... more results ...
   
   $ ghx view-repo textual/textual
   
   ... repository details ...
   
   $ ghx repo-files textual/textual | grep ".py$" | head -5
   src/textual/app.py
   src/textual/binding.py
   src/textual/color.py
   src/textual/css_types.py
   src/textual/events.py
   ```

### UI Patterns

1. **Color Scheme**
   - Use Rich for consistent, terminal-friendly color formatting
   - Color-code language tags, repository stats, and action types
   - Maintain readability on both light and dark terminals
   - Use sparingly to highlight important information

2. **Interactive Elements**
   - Simple numbered menus for most interactions
   - Consistent navigation patterns (numbers for selection, q to quit, etc.)
   - Clear prompts and input validation
   - Support for both direct commands and interactive mode

3. **Shell Integration**
   - Support for piping output to other commands
   - Accept input from stdin when appropriate
   - Provide machine-readable output formats (JSON, CSV) for scripting
   - Respect terminal width for formatting

4. **Information Display**
   - Focus on content over decoration
   - Clear, hierarchical presentation of data
   - Consistent formatting of similar information
   - Support for displaying rich content (markdown, code syntax) in a readable way

## Implementation Details

### Command Structure

1. **Core Commands**
   - `ghx search-repos <query>` - Search repositories
   - `ghx search-code <query>` - Search code
   - `ghx view-repo <repo>` - View repository details
   - `ghx repo-files <repo>` - List repository files
   - `ghx view-file <repo> <path>` - View file content
   - `ghx create-gist [file]` - Create a gist

2. **Interactive Mode**
   - `ghx` - Launch interactive menu
   - `ghx search` - Interactive search with filters
   - `ghx explore <repo>` - Interactive repository explorer

3. **Format Control**
   - `--format=json|text|csv` - Control output format
   - `--no-color` - Disable color output
   - `--compact` - Use compact output format

### Data Handling

1. **Shell Integration**
   - All commands support STDIN/STDOUT piping
   - Output formatted for easy parsing with tools like grep, awk, etc.
   - Support for redirecting output to files

2. **Local Storage**
   - `~/.config/ghx/history.json` - Search and view history
   - `~/.config/ghx/config.json` - User configuration
   - `~/.config/ghx/cache/` - Simple cache directory

### GitHub API Integration

- Primary interaction through `gh` CLI 
- Parsing output from gh commands
- JSON output for machine-readable data
- Authentication handled through gh CLI

## Technical Challenges

1. **Command Output Formatting**
   - Pretty-printing complex data structures in the terminal
   - Handling wide content and terminal width constraints
   - Supporting both human-readable and machine-readable formats
   - Syntax highlighting for code and markdown

2. **Shell Integration**
   - Preserving ANSI colors when appropriate
   - Ensuring proper pipe handling
   - Maintaining compatibility with common Unix tools
   - Supporting both interactive and non-interactive usage

3. **API Rate Limits**
   - Simple caching to reduce API calls
   - Clear user feedback on rate limit status
   - Graceful handling of API errors

4. **Terminal Compatibility**
   - Supporting basic terminals without color/unicode
   - Ensuring compatibility with different shells (bash, zsh, etc.)
   - Adapting to different terminal widths

## Testing Strategy

1. **Command Execution Tests**
   - Test each command with various inputs
   - Verify correct output formats
   - Test piping between commands

2. **Integration Tests**
   - GitHub API interaction
   - Command execution
   - Response parsing

3. **Shell Compatibility Tests**
   - Test in different shells (bash, zsh, fish)
   - Test in constrained environments (like SSH sessions)

4. **Mock GitHub CLI**
   - Mock responses for testing without API calls
   - Simulate different output formats and error conditions

## Development Workflow

1. **Setup Development Environment**
   - Install dependencies (Rich, gh)
   - Configure GitHub authentication
   - Setup simple development environment

2. **Command Implementation**
   - Implement one command at a time
   - Start with core functionality
   - Build interactive layer on top

3. **Integration**
   - Ensure all commands work together
   - Test pipelines between commands
   - Implement interactive menu system

4. **Polish**
   - Optimize output formatting
   - Improve error handling
   - Add helpful documentation
   - Create examples and workflows

## Getting Started

To start contributing to GitHub Explorer:

1. Install Rich and GitHub CLI:
   ```bash
   pip install rich
   # Install GitHub CLI according to your OS
   ```

2. Ensure GitHub CLI is installed and authenticated:
   ```bash
   gh auth status
   ```

3. Run the development version:
   ```bash
   python gh-explorer.py
   ```

## References

- [Rich Documentation](https://rich.readthedocs.io/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
