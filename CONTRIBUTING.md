# Contributing to Drowsiness Detection System

Thank you for considering contributing to the **Drowsiness & Yawn Detection System**! We welcome contributions, bug reports, feature requests, and documentation improvements.

## How to Contribute

### 1. Reporting Bugs
- Search existing GitHub Issues before opening a new issue.
- Clearly describe the problem, steps to reproduce, OS environment, and relevant error tracebacks.

### 2. Feature Requests
- Open a GitHub issue detailing the proposed feature, implementation rationale, and potential use cases.

### 3. Pull Request Guidelines
1. Fork the repository and create a new feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Ensure code follows **PEP8** standard conventions:
   - Use 4-space indentations.
   - Add type hints to function signatures.
   - Include Google-style docstrings for public classes and functions.
3. Run unit tests to verify changes:
   ```bash
   python -m unittest discover -s tests
   ```
4. Commit your changes with conventional messages (`feat:`, `fix:`, `docs:`, `test:`).
5. Push to your branch and submit a Pull Request.

---

## Code Style & Testing
- Format Python files with `black` or `flake8` prior to submission.
- Ensure all test cases pass cleanly without warnings.
