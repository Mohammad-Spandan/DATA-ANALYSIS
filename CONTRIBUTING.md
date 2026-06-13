# Contributing to Agricultural Crop Data Analysis

First off, thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/DATA-ANALYSIS.git
   cd DATA-ANALYSIS
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

## Development Workflow

### Writing Code

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions
- Include type hints
- Keep functions focused and modular

**Example**:
```python
def calculate_yield(production: float, area: float) -> float:
    """
    Calculate crop yield (production per unit area).
    
    Args:
        production: Total production amount
        area: Cultivated area
        
    Returns:
        Yield value (production/area)
        
    Raises:
        ValueError: If area is zero or negative
    """
    if area <= 0:
        raise ValueError("Area must be positive")
    return production / area
```

### Testing

Write tests for new features:

```python
import pytest
from src.data_cleaner import DataCleaner

def test_remove_duplicates():
    """Test duplicate removal functionality."""
    cleaner = DataCleaner()
    test_data = pd.DataFrame({'crop': [1, 1, 2], 'year': [2020, 2020, 2021]})
    result = cleaner.remove_duplicates(test_data)
    assert len(result) == 2
```

Run tests:
```bash
pytest tests/ -v --cov=src
```

### Code Quality

1. **Format code with Black**
   ```bash
   black src/ tests/ scripts/
   ```

2. **Check style with Flake8**
   ```bash
   flake8 src/ tests/ scripts/ --max-line-length=100
   ```

3. **Check type hints**
   ```bash
   mypy src/ --ignore-missing-imports
   ```

## Commit Guidelines

Write clear, descriptive commit messages:

```
Format: <type>(<scope>): <subject>

Types:
  feat:     New feature
  fix:      Bug fix
  docs:     Documentation
  style:    Code style changes (formatting, missing semicolons, etc)
  refactor: Code refactoring
  test:     Adding or updating tests
  chore:    Build process, dependencies

Examples:
  feat(eda): add correlation analysis for crop production
  fix(data_cleaner): handle missing values in production column
  docs(readme): update installation instructions
```

## Pull Request Process

1. **Before submitting**
   - Run all tests: `pytest tests/`
   - Format code: `black .`
   - Check style: `flake8 .`
   - Update documentation if needed

2. **Create a pull request**
   - Give it a clear, descriptive title
   - Fill out the PR template
   - Link related issues
   - Provide context and rationale

3. **PR template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   
   ## How Has This Been Tested?
   Describe the tests you ran
   
   ## Checklist
   - [ ] Code follows PEP 8
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] All tests pass
   ```

## Contribution Areas

### High Priority
- [ ] Fix missing Tea production data (2016-2024)
- [ ] Implement data imputation strategies
- [ ] Add forecasting models
- [ ] Create interactive dashboard

### Medium Priority
- [ ] Add regional analysis
- [ ] Implement price correlation
- [ ] Optimize performance for large datasets
- [ ] Add more visualization types

### Low Priority
- [ ] Documentation improvements
- [ ] Code refactoring
- [ ] Test coverage expansion
- [ ] Example notebook improvements

## Issues

### Reporting Bugs

Include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Error message/traceback

### Suggesting Features

Include:
- Clear description of feature
- Use case and motivation
- Proposed implementation (optional)
- Related issues

## Documentation

- Update README.md for major changes
- Add docstrings to all functions
- Update DATA_DICTIONARY.md if schema changes
- Add comments for complex logic

## Review Process

1. Code review by maintainers
2. Automated tests must pass
3. Code coverage must not decrease
4. Feedback and revisions
5. Approval and merge

## Questions?

Feel free to open an issue or ask in discussions!

Thank you for contributing! 🎉
