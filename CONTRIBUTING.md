# Contributing to TalentScout Hiring Assistant

Thank you for your interest in contributing to TalentScout! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## Getting Started

### 1. Fork and Clone

```bash
git clone <your-fork-url>
cd "Talent Scout Hiring Assistant"
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Format code with Black: `black .`
- Check with Flake8: `flake8 . --max-line-length=100`

### Testing

```bash
# Run tests
pytest tests.py -v

# Run with coverage
pytest tests.py --cov=. --cov-report=html
```

### Commit Messages

Use clear, descriptive commit messages:

```
[FEATURE] Add sentiment analysis to chatbot
[FIX] Resolve phone number parsing issue
[DOCS] Update README with new features
[REFACTOR] Optimize conversation manager performance
```

### Pull Request Process

1. Create descriptive PR title and description
2. Reference related issues (#123)
3. Ensure all tests pass
4. Update documentation if needed
5. Wait for review before merging

## Areas for Contribution

### High Priority
- [ ] Multi-language support
- [ ] Sentiment analysis integration
- [ ] Email notifications
- [ ] Admin dashboard

### Medium Priority
- [ ] Resume parsing
- [ ] Video interview support
- [ ] Analytics dashboard
- [ ] Performance optimization

### Low Priority
- [ ] UI theme customization
- [ ] Additional export formats
- [ ] Advanced reporting

## Bug Reports

Report bugs using the GitHub Issues template:

```
**Describe the bug**
Clear description of the issue

**Steps to reproduce**
1. Step one
2. Step two
3. ...

**Expected behavior**
What should happen

**Actual behavior**
What actually happened

**Environment**
- Python version: 
- OS: 
- Library versions:
```

## Feature Requests

Suggest features using GitHub Issues:

```
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
How the feature should work

**Additional context**
Any other relevant information
```

## Project Structure

```
├── core.py              # Conversation logic
├── main.py              # LLM integration
├── streamlit_app.py     # UI interface
├── config.py            # Configuration
├── utils/
│   └── data_handler.py  # Data storage
├── tests.py             # Unit tests
└── docs/                # Documentation
```

## Documentation Guidelines

- Use clear, simple language
- Include code examples
- Update README for new features
- Add docstrings to functions

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When validation fails
    """
    pass
```

## Performance Guidelines

- Keep API calls minimal
- Cache responses when appropriate
- Optimize database queries
- Monitor token usage

## Security Guidelines

- Never commit API keys or secrets
- Use environment variables for configuration
- Hash sensitive data
- Follow GDPR requirements
- Validate all user input

## Release Process

1. Update version in config.py
2. Update CHANGELOG
3. Update README
4. Create release on GitHub
5. Tag with version number

## Questions?

- Open an issue for discussion
- Check existing documentation
- Review closed issues for solutions

Thank you for contributing! 🚀
