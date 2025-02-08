# Technical Documentation

This document provides detailed technical information about the Inclusive Space Index Assessment Tool's architecture, implementation, and development status.

## Project Structure

```plaintext
app/
├── utils/
│   ├── scoring.py      # Scoring and radar chart calculations
│   ├── data_loader.py  # CSV/Supabase data handling
│   ├── state.py        # Session state + phase management
│   ├── styles.py       # Theme-aware CSS + chart styles
│   ├── supabase.py     # Database connection and operations
│   └── validators.py   # Input validation utilities
├── components/
│   ├── sidebar.py      # Dashboard with progress
│   ├── questions.py    # Question display and management
│   └── results.py      # Radar chart + export handling
└── streamlit_app.py    # Main application entry point
```

## Technical Implementation

### Scoring System

```python
# Exponential scoring progression for better maturity reflection
OPTION_SCORES = [0, 1, 2, 4, 8]  # Exponential progression
MAX_POINTS_PER_QUESTION = 8

# Score calculation example:
def calculate_section_score(responses: dict) -> tuple[int, int]:
    """Calculate score for a section
    Returns: (points_earned, max_possible_points)
    """
    earned = sum(OPTION_SCORES[response] for response in responses.values())
    maximum = len(responses) * MAX_POINTS_PER_QUESTION
    return earned, maximum
```

### State Management

```python
# Application phases
ASSESSMENT_PHASE = "assessment"
RESULTS_PHASE = "results"

# Session state variables
state = {
    'phase': str,           # Current application phase
    'responses': dict,      # User's question responses
    'scores': dict,         # Calculated section scores
    'email': str,           # User's email (results phase)
    'previous_results': dict # Historical results for comparison
}
```

### Visualization

```python
# Chart styling configuration
CHART_COLORS = {
    'current': {
        'fill': 'rgba(52, 152, 219, 0.5)',
        'stroke': 'rgb(52, 152, 219)'
    },
    'previous': {
        'fill': 'rgba(46, 204, 113, 0.3)',
        'stroke': 'rgb(46, 204, 113)'
    }
}
```

## User Flow Implementation

### Phase 1: Assessment

- Main area displays sections as tabs
- Each section contains its questions
- Sidebar components:
  - Dashboard title
  - Total score display
  - Progress tracking (answered/total)
  - Submit button (enabled when complete)
  - Reset functionality

### Phase 2: Results

- Side-by-side layout:
  - Radar chart (60% width)
  - Results management (40% width)
- Email validation system
- Previous results comparison
- Consent management:
  - Results sharing
  - Mailing list subscription
- Export functionality:
  - Detailed CSV export
  - Email copy (pending)

## Development Status

### Completed Features ✅

- Core assessment functionality
- Real-time scoring system
- Theme-aware styling
- Session state management
- Progress tracking
- Section navigation
- Radar chart visualization
- Email & GDPR form
- Previous results comparison
- CSV export
- Supabase integration
- Results storage
- Previous results lookup

### Pending Features 🚧

- Email delivery system
- Analytics tracking
- Loading states for async operations
- Enhanced error handling

## Next Steps

1. Email System Integration
   - Setup email service
   - Implement templates
   - Add delivery queue

2. Analytics Implementation
   - User journey tracking
   - Usage statistics
   - Error monitoring

3. Performance Optimization
   - State management refinement
   - Caching implementation
   - Query optimization

4. UX Improvements
   - Loading indicators
   - Error messages
   - Navigation enhancements

See [SETUP.md](SETUP.md) for deployment instructions and [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
