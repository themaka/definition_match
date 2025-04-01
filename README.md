# Streamlit Template

A modern Python template for Streamlit applications using `uv` for dependency management. This template demonstrates best practices for Streamlit app development, including testing, CI/CD, and code quality tools.

## Features

- 📊 Streamlit application template with sample components
- 🧪 Full test suite using pytest
- 📦 Modern Python packaging with `pyproject.toml`
- 🚀 Fast dependency management with `uv`
- ⚡ GitHub Actions CI/CD pipeline
- 🔍 Code quality tools (ruff, black, mypy)
- 🪝 Pre-commit hooks for code quality

## Quick Start

1. Create a new project:
```bash
# Initialize new project with uv
uv init --lib streamlit-template
cd streamlit-template

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
# Install project in editable mode with development dependencies
uv pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

3. Run the application:
```bash
python -m streamlit run src/streamlit_template/app.py
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

### Testing
Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=streamlit_template
```

### Code Quality
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

All of these checks run automatically on git commit through pre-commit hooks and in the CI pipeline.

## Deployment

### Local Development
For local development:
```bash
streamlit run src/streamlit_template/app.py
```

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Select your main file: `src/streamlit_template/app.py`

The GitHub Actions workflow will run tests automatically on push and pull requests.

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
5. Commit your changes
6. Push to your fork
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing framework
- [uv](https://github.com/astral-sh/uv) - For fast Python package management
- [ruff](https://github.com/astral-sh/ruff) - For the lightning-fast Python linter
