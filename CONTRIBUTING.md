# Contributing Guidelines

## Project Structure

```plaintext
app/
├── modules/           # Core functionality modules
│   ├── data_loader.py      # Question loading and management
│   ├── score_calculator.py # Score calculation logic
│   ├── visualization.py    # Chart generation
│   └── ui_components.py    # Streamlit UI components
├── utils/            # Utility functions and constants
│   ├── constants.py        # Configuration constants
│   └── validators.py       # Input validation
└── streamlit_app.py  # Main application entry point
```

## Development Guidelines

1. **Code Style**
   - Use type hints for all function parameters and return values
   - Include docstrings for all modules, classes, and functions
   - Keep functions focused and single-purpose

2. **Error Handling**
   - Use try/except blocks for external operations (file I/O, database)
   - Provide meaningful error messages
   - Log errors appropriately
   - Validate inputs before processing

3. **Testing**
   - Write unit tests for new functionality
   - Ensure existing tests pass before submitting changes
   - Include edge cases in test coverage

4. **Documentation**
   - Update relevant documentation when making changes
   - Include inline comments for complex logic
   - Keep README.md and INSTRUCTIONS.md up to date

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes following the guidelines above
4. Update documentation as needed
5. Submit a pull request with a clear description of changes

## Development Setup

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

3. Create a `.env` file with required variables
4. Run the application:

   ```bash
   docker compose up --build
   ```

## Questions or Issues?

Feel free to open an issue for:

- Bug reports
- Feature requests
- Documentation improvements
- General questions
