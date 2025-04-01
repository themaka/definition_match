# Development and Deployment Workflow Guide

This guide explains the development workflow and deployment process for the Streamlit template project.

## Local Development Setup

### Prerequisites
- Python 3.12 or higher
- Git
- Docker Desktop (for local GitHub Actions testing)
- pipx (for tool installation)
- pre-commit

### Initial Setup

1. Clone the repository:
```bash
git clone git@github.com:RutgersGRID/streamlit-template.git
cd streamlit-template
```

2. Install development tools:
```bash
# Install pre-commit using pipx
pipx install pre-commit

# Install pre-commit hooks
pre-commit install
```

3. Install project dependencies:
```bash
pip install -e ".[dev]"
```

## Development Workflow

### Code Quality and Testing

1. **Pre-commit Checks**
   ```bash
   # Run pre-commit checks on all files
   pre-commit run --all-files
   ```
   This will run:
   - trailing-whitespace removal
   - end-of-file-fixer
   - yaml checking
   - black (Python formatter)
   - ruff (Python linter)

2. **Running Tests**
   ```bash
   # Run Python tests with coverage
   pytest src/tests/ --cov=src/streamlit_template
   ```

3. **Running the Streamlit App Locally**
   ```bash
   streamlit run src/streamlit_template/app.py
   ```

### Git Workflow

1. **Create and Switch to Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Commit Changes**
   ```bash
   # Stage changes
   git add .

   # Commit (this will trigger pre-commit hooks)
   git commit -m "type: descriptive message"
   ```
   Commit message types:
   - feat: new features
   - fix: bug fixes
   - docs: documentation changes
   - style: formatting, missing semi colons, etc
   - refactor: code restructuring
   - test: adding tests
   - chore: maintenance

3. **Push Changes**
   ```bash
   git push origin feature/your-feature-name
   ```

## GitHub Actions Workflow

### Testing Workflows Locally

1. **Install Act**
   ```bash
   brew install act
   ```

2. **Run Individual Jobs**
   ```bash
   # Test quality checks
   act -j quality --container-architecture linux/amd64

   # Test Python tests
   act -j test --container-architecture linux/amd64

   # Test deployment
   act -j deploy --container-architecture linux/amd64
   ```

### Workflow Structure

The GitHub Actions workflow (`python-test-deploy.yml`) consists of three main jobs:

1. **Quality**
   - Runs pre-commit checks
   - Ensures code formatting and style

2. **Test**
   - Runs Python tests
   - Generates coverage reports

3. **Deploy**
   - Builds Streamlit app
   - Deploys to GitHub Pages

### GitHub Pages Deployment

1. **Setup**
   - Go to repository Settings → Pages
   - Set source to "GitHub Actions"

2. **Access**
   - After successful deployment, the app will be available at:
   - `https://rutgersgrid.github.io/streamlit-template/`

## Troubleshooting

### Common Issues

1. **Pre-commit Failures**
   - Run `pre-commit run --all-files` locally
   - Let the hooks fix the issues
   - Commit the changes

2. **Test Failures**
   - Check test output for specific failures
   - Run tests locally with `-v` flag for more detail
   ```bash
   pytest -v src/tests/
   ```

3. **Deployment Issues**
   - Check Actions tab for detailed logs
   - Verify GitHub Pages settings
   - Check if all dependencies are properly specified

### Getting Help

For issues with:
- GitHub Actions: Check the Actions tab logs
- Pre-commit: Run with `--verbose` flag
- Streamlit: Check the Streamlit logs in the deployment job

## Maintenance

### Updating Dependencies

1. **Pre-commit Hooks**
   ```bash
   pre-commit autoupdate
   ```

2. **Python Dependencies**
   - Update versions in `pyproject.toml`
   - Reinstall with `pip install -e ".[dev]"`

### Regular Checks

- Run pre-commit checks before pushing
- Keep dependencies updated
- Monitor GitHub Actions for any failures
