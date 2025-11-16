# Contributing to ScAInner

Thank you for your interest in contributing to ScAInner! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Fork and Clone

1. **Fork the repository** on GitHub by clicking the "Fork" button at the top of the repository page.

2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/scainner.git
   cd scainner
   ```

3. **Add the upstream repository** as a remote:
   ```bash
   git remote add upstream https://github.com/black-cape/scainner.git
   ```

4. **Verify your remotes**:
   ```bash
   git remote -v
   ```
   You should see both `origin` (your fork) and `upstream` (the original repository).

## Making Changes

### Creating a Branch

1. **Update your fork** with the latest changes from upstream:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Or for bug fixes:
   ```bash
   git checkout -b fix/your-bug-description
   ```

   **Branch naming conventions:**
   - `feature/` - New features
   - `fix/` - Bug fixes
   - `docs/` - Documentation changes
   - `refactor/` - Code refactoring
   - `test/` - Test additions or changes

### Making Your Changes

1. **Make your changes** to the codebase.

2. **Follow code style guidelines** (see below).

3. **Test your changes** to ensure they work as expected.

4. **Run linting**:
   ```bash
   just lint
   ```

## Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines.
- Use type hints where appropriate.
- Keep functions focused and single-purpose.
- Write clear, descriptive variable and function names.

### Linting

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting. Before submitting a pull request, ensure your code passes:

```bash
just lint
```

### Documentation

- Add docstrings to functions and classes following Google or NumPy style.
- Update README.md if you add new features or change behavior.
- Update example.env if you add new environment variables.

## Commit Messages

Write clear, descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Reference issues and pull requests when applicable.

## Submitting a Pull Request

### Before Submitting

1. **Ensure your code works** and doesn't break existing functionality.
2. **Run linting** and fix any issues.
3. **Update documentation** if needed.
4. **Test your changes** thoroughly.

### Creating the Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub:
   - Go to the original repository on GitHub.
   - Click "New Pull Request".
   - Select "compare across forks".
   - Choose your fork and branch.
   - Fill out the pull request template.

3. **Write a clear description**:
   - What changes does this PR make?
   - Why are these changes needed?
   - How was this tested?
   - Reference any related issues.

### Pull Request Review Process

- Maintainers will review your PR and may request changes.
- Address review comments by making additional commits to your branch.
- Once approved, a maintainer will merge your PR.

### Keeping Your PR Up to Date

If the upstream repository has new commits while your PR is open:

1. **Fetch and merge** the latest changes:
   ```bash
   git fetch upstream
   git checkout feature/your-feature-name
   git merge upstream/main
   ```

2. **Resolve any conflicts** if they occur.

3. **Push the updated branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Reporting Issues

### Before Reporting

- Check if the issue has already been reported.
- Ensure you're using the latest version.
- Try to reproduce the issue with a minimal example.

### Creating an Issue

When creating an issue, please include:

- **Clear title** describing the issue.
- **Description** of the problem.
- **Steps to reproduce** (if applicable).
- **Expected behavior** vs. **actual behavior**.
- **Environment information** (OS, Python version, etc.).
- **Error messages** or logs (if applicable).

## Code of Conduct

- Be respectful and inclusive.
- Welcome newcomers and help them get started.
- Focus on constructive feedback.
- Respect different viewpoints and experiences.

## Questions?

If you have questions about contributing, you can:

- Open an issue for discussion.
- Check existing issues and pull requests.
- Review the project documentation.

Thank you for contributing to ScAInner! 🎉

