# GitHub Explorer: Roadmap & Milestones

## Current Status

The GitHub Explorer is a shell-integrated GitHub exploration tool that allows users to:

1. Search for repositories and code on GitHub
2. View repository details, READMEs, and file structures
3. Clone repositories and open them in a web browser
4. Operate with better UX (sensible defaults, improved keyboard handling)

## Recent Improvements

- Added support for running the tool via UV tool installation
- Improved error handling and fallback mechanisms
- Better keyboard support (j/k navigation, escape handling)
- Enhanced CLI to accept arguments without quotes
- Simplified repository search with better defaults
- Added an interactive repository browser (currently disabled, needs further terminal compatibility work)

## Development Instructions

To develop and test changes:

1. Make your code changes in the source directory
2. Reinstall the tool with UV:
   ```bash
   cd /path/to/github-explorer && uv tool install -e .
   ```
3. Run the tool to test your changes:
   ```bash
   ghx [command] [arguments]
   ```

For testing the interactive browser locally (when fixed):
```bash
GHX_INTERACTIVE=true ghx search-repos [query]
```

To disable the interactive mode:
```bash
GHX_INTERACTIVE=false ghx search-repos [query]
```

## Release Milestones

### v0.2.0 - Textual-based UI
- Convert from simple TUI to Textual framework
- Implement core screens with proper layouts
- Basic styling and keyboard navigation
- Repository view with formatted README
- Repository search with visual results

### v0.3.0 - Enhanced Repository Browsing
- File browser with navigation
- Code viewing with syntax highlighting
- Repository stats panel
- Star/Watch/Fork actions
- README rendering with images (as ASCII art)

### v0.4.0 - Advanced Search & Filtering
- Search filters sidebar
- Real-time search suggestions
- Sort options and advanced filters
- Trending repositories view
- Search history and favorites

### v0.5.0 - Issues & PRs
- Issues list with filters
- Issue viewing with comments
- PR list with status indicators
- PR diff viewer
- Comment on issues and PRs

### v0.6.0 - User Profiles & Social
- User profile viewing
- Follow/unfollow users
- User repositories and activity
- Star management
- Discover new users

### v0.7.0 - GitHub Actions & CI
- View workflow runs
- Workflow status and logs
- Trigger workflows
- Build status indicators

### v0.8.0 - Notifications & Updates
- Notification center
- Read/unread management
- Action buttons for notifications
- Real-time updates

### v0.9.0 - Advanced Features
- Terminal-based image preview
- Graph visualizations for contributors
- Code intelligence (jump to definition, etc.)
- GitHub Copilot integration

### v1.0.0 - Stable Release
- Performance optimizations
- Comprehensive documentation
- Plugin system
- Theme customization
- Configuration options

## Detailed Feature Specifications

### Repository Search & Exploration

#### Search Interface
- **Search Box**
  - Real-time suggestions as you type
  - Search history with up/down arrow navigation
  - Support for GitHub search syntax
  - Clear button and keyboard shortcut

- **Filters Panel**
  - Language filter with multi-select
  - Date range selector
  - Star count range selector
  - Topic selector
  - License filter

- **Results Display**
  - Card-based layout for each repository
  - Star count, fork count, and last updated time
  - Language indicator with color coding
  - Description with highlight of matching terms
  - Pagination or infinite scroll

#### Repository View
- **Header Section**
  - Repository name and owner
  - Description
  - Website link (if available)
  - Tags and topics

- **Stats Overview**
  - Star count with star/unstar action
  - Fork count with fork action
  - Watch count with watch/unwatch action
  - Issue count with link to issues
  - PR count with link to PRs
  - Last updated timestamp

- **README Display**
  - Markdown rendering with proper formatting
  - Code block syntax highlighting
  - Tables with proper alignment
  - Lists (ordered and unordered)
  - Images represented as ASCII art or placeholder
  - Links with highlighting and action on selection

- **File Browser**
  - Tree view of repository files
  - Directory collapsing/expanding
  - File type icons
  - Last updated indicator for each file
  - Size indicator for files
  - Preview on selection

### Code Viewing & Searching

#### Code Search
- **Search Query Builder**
  - Syntax highlighting for search queries
  - Autocomplete for language, repository, and path
  - Search history
  - Recent searches

- **Search Results**
  - File path and repository info
  - Code snippet with highlighted matches
  - Line numbers
  - Context lines before and after match
  - Jump to file action

#### Code Viewer
- **Syntax Highlighting**
  - Language detection
  - Theme-based highlighting
  - Line numbers
  - Word wrap option

- **Navigation**
  - Jump to line
  - Find in file
  - Scroll with keybindings
  - Go to definition (for supported languages)

- **Code Actions**
  - Copy to clipboard
  - View raw
  - View blame
  - View history
  - Edit (if permissions allow)

### Issues & Pull Requests

#### Issues List
- **Filter Options**
  - Open/closed state
  - Assigned to me
  - Created by me
  - Mentioned me
  - Labels
  - Milestones

- **Issue Cards**
  - Title with issue number
  - Labels with colors
  - Open/closed status
  - Created date and author
  - Comment count
  - Assignees
  - Preview of description

#### Issue View
- **Header**
  - Title and issue number
  - Open/close button
  - Labels with add/remove
  - Assignees with add/remove
  - Milestone

- **Description**
  - Markdown rendered content
  - Author and creation time
  - Edit button (if permissions allow)

- **Timeline**
  - Comments with markdown
  - Events (assigned, labeled, etc.)
  - References to other issues or PRs
  - Add comment interface

#### Pull Request View
- Similar to Issue View plus:
  - Branch info (source and target)
  - Merge status
  - CI status
  - Reviewers with status
  - Diff viewer

#### Diff Viewer
- **File Tree**
  - Changed files list
  - Added/modified/deleted indicators
  - File type grouping

- **Diff Display**
  - Side-by-side or unified view
  - Syntax highlighting
  - Line numbers
  - Added/deleted/modified highlighting
  - Comment buttons on lines
  - Expand/collapse sections

### Gist Management

#### Gist Creation
- **Content Input**
  - Multi-file support
  - Syntax highlighting as you type
  - File name input
  - Description input
  - Public/secret toggle

- **Options**
  - Add file button
  - Remove file button
  - File type selection
  - Create/cancel buttons

#### Gist Browsing
- **List View**
  - Gist description and ID
  - Created date
  - File count and names
  - Public/secret indicator
  - Star count

- **Detail View**
  - Similar to repository code view
  - Edit/delete actions
  - Fork button
  - Star button
  - Share button

### User Management

#### Profile View
- **User Info**
  - Avatar (ASCII representation)
  - Name and username
  - Bio
  - Location and company
  - Email and website
  - Follower and following counts
  - Follow/unfollow button

- **Activity Section**
  - Recent commits
  - Recent issues and PRs
  - Recent gists
  - Contribution graph (ASCII representation)

- **Repositories Section**
  - List of user repositories
  - Filter by type (sources, forks, etc.)
  - Sort options
  - Quick actions for each repository

#### Social Features
- **Following Management**
  - List followers
  - List following
  - Follow/unfollow actions
  - Discover users based on interests

### GitHub Actions & CI

#### Workflow List
- **Repository Workflows**
  - Workflow name
  - Status indicator
  - Last run time
  - Success/failure count
  - Trigger method

#### Workflow Run View
- **Run Info**
  - Status and conclusion
  - Trigger event
  - Started by user
  - Duration
  - Artifacts

- **Jobs List**
  - Job name
  - Status
  - Duration
  - Runner info

- **Job Details**
  - Step list with status
  - Log output with ANSI color support
  - Environment variables
  - Annotations (warnings, errors)

#### Actions
- **Trigger Workflow**
  - Workflow selection
  - Input parameters
  - Branch selection
  - Confirmation

## Implementation Priorities

### Priority 1: Core Experience
- Setup Textual app infrastructure
- Repository search and basic viewing
- File navigation and code viewing
- Markdown rendering for READMEs

### Priority 2: User Experience
- Keyboard shortcuts and navigation
- Consistent UI patterns
- Loading indicators and error handling
- Search filters and sorting

### Priority 3: Advanced GitHub Integration
- Star/Watch/Fork actions
- Issues and PRs
- Gist management
- User profiles

### Priority 4: Advanced Features
- GitHub Actions integration
- Notifications
- Social features
- Terminal-friendly visualizations

## Success Metrics

- **User Adoption**
  - Downloads and active installations
  - GitHub stars
  - Community contributions

- **Feature Completeness**
  - Coverage of GitHub API functionality
  - Feature parity with web interface
  - Unique terminal-specific features

- **Performance**
  - Startup time
  - Search response time
  - UI responsiveness

- **User Satisfaction**
  - Feedback and reviews
  - Feature requests
  - Issue reports
