# Streamlit Template

A modern Python template

## Prerequisites

- Python 3.9 or higher
- `uv` for dependency management
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- `pipx` for tool installation
  ```bash
  # On macOS
  brew install pipx
  pipx ensurepath

  # On Ubuntu/Debian
  python -m pip install --user pipx
  pipx ensurepath
  ```
- `pre-commit` installed via pipx
  ```bash
  pipx install pre-commit
  ```
- `act` for testing GitHub Actions locally (optional)
  ```bash
  brew install act  # On macOS
  ``` for Streamlit applications using `uv` for dependency management. This template demonstrates best practices for Streamlit app development, including testing, CI/CD, and code quality tools.

## Quick Start

1. Create a new project using uv:
```bash
# Initialize new project
uv init --lib streamlit-template
cd streamlit-template

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
# Add required packages
uv add streamlit pandas numpy

# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit using pipx (recommended)
pipx install pre-commit
# Or alternatively using uv
# uv pip install pre-commit

# Setup pre-commit hooks
pre-commit install
```

3. Run the application:
```bash
# Run using uv (recommended)
uv run streamlit run src/streamlit_template/app.py
```

## Development

### Project Structure
```
streamlit-template/
├── src/
│   ├── streamlit_template/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── utils.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_utils.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
└── README.md
```

### Testing and Quality Checks

#### Local Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=streamlit_template
```

#### Code Quality
The project uses several tools to maintain code quality:

- **ruff**: Fast Python linter
  ```bash
  ruff check .
  ```

- **black**: Code formatter
  ```bash
  black .
  ```

- **mypy**: Static type checker
  ```bash
  mypy src
  ```

#### GitHub Actions Local Testing
Test GitHub Actions workflows locally using act:
```bash
# Install act (macOS)
brew install act

# Run GitHub Actions locally
act
```

### GitHub Setup

1. Create a new repository on GitHub

2. Initialize git and push:
```bash
git init
git add .
git commit -m "Initial commit: Streamlit template project"
git remote add origin git@github.com:username/streamlit-template.git
git push -u origin main
```

## Deployment

### Local Development
For local development:
```bash
uv run streamlit run src/streamlit_template/app.py
```

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Select your main file: `src/streamlit_template/app.py`

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run tests and quality checks:
   ```bash
   pytest
   ruff check .
   black .
   mypy src
   ```
5. Commit your changes (pre-commit hooks will run automatically)
6. Push to your fork
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
