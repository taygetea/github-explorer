# GitHub Explorer (ghx) Guidance

## Build & Test Commands
- Install: `pip install -e .`
- Run app: `python gh-explorer.py` or `bin/ghx`
- Run tests: `pytest`
- Run single test: `pytest tests/path_to_test.py::test_name`
- Lint code: `black .` && `isort .` && `ruff check .`

## Code Style
- Line length: 88 characters
- Indentation: 4 spaces
- Naming: snake_case for functions/variables, PascalCase for classes
- Imports: grouped by stdlib, third-party, local (isort with black profile)
- Type hints: required for all function parameters and return values
- Docstrings: all modules, classes, and functions
- Error handling: specific exception types, descriptive messages, exception chaining
- UI: use Rich library for console formatting
- CLI: Click library for command parsing

## Project Structure
- API client in `gh_explorer/api/`
- UI components in `gh_explorer/ui/`
- Utility functions in `gh_explorer/utils/`
- CLI entry point: `gh_explorer.cli:main`