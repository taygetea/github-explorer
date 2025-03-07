# GitHub Explorer (ghx)

A shell-integrated tool for exploring GitHub repositories, code, and more.

![GitHub Explorer Demo](https://github.com/yourusername/gh-explorer/raw/main/docs/demo.gif)

## Features

- **Repository Search:** Find repos by keyword, language, and topic
- **Code Search:** Find code snippets across GitHub
- **Rich Formatting:** Beautiful terminal output with syntax highlighting
- **Interactive UI:** Menu-driven interface for easy exploration
- **Shell Integration:** Use as direct commands or in pipes

## Why GitHub Explorer?

GitHub Explorer bridges the gap between raw command-line tools and full-screen TUI applications:

- **Discoverable:** Menu-driven but still command-line friendly
- **Composable:** Plays well with other shell tools through piping and redirection
- **Lightweight:** No need to learn complex keyboard shortcuts
- **Beautiful:** Modern terminal UI with rich output formatting

## Installation

### Prerequisites

- Python 3.8 or higher
- GitHub CLI (`gh`) installed and authenticated

### Install from PyPI (coming soon)

```bash
pip install gh-explorer
```

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/gh-explorer.git
cd gh-explorer

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### Interactive Mode

Simply run `ghx` without any arguments to enter interactive mode:

```bash
ghx
```

### Direct Commands

```bash
# Search repositories
ghx search-repos "terminal ui"

# View repository details
ghx view-repo textual/textual

# Search code
ghx search-code "def factorial"

# Output as JSON for scripting
ghx search-repos "cli tools" --json | jq '.[] | .nameWithOwner'
```

## Project Structure

The project follows a modular design:

- `gh_explorer/api/` - GitHub API client using GitHub CLI
- `gh_explorer/ui/` - User interface components
- `gh_explorer/utils/` - Utility functions
- `gh_explorer/data/` - Data storage and history

## Development

### Setting up for development

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies for development
pip install -e ".[dev]"
```

### Run tests (coming soon)

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [GitHub CLI](https://cli.github.com/) - For providing the API access
- [Rich](https://github.com/Textualize/rich) - For beautiful terminal formatting
- [Click](https://click.palletsprojects.com/) - For the command-line interface