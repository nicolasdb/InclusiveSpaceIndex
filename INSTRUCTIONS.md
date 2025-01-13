# Technical Instructions

## Local Development Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
./setup.sh
```

3. Run the application:
```bash
PYTHONPATH=. uvicorn src.main:app --reload
```

4. Visit http://localhost:8000 in your browser

## Project Structure

- `src/` - Python source code
  - `main.py` - FastAPI application
  - `generate_assessment_widget.py` - Assessment form generation
  - `assessment-data-L1.csv` - Assessment questions and scoring data
- `templates/` - HTML templates
- `static/` - CSS and other static files

## Deployment

### Local Docker Deployment

1. Build the container:
```bash
docker build -t inclusive-space-index .
```

2. Run the container:
```bash
docker run -p 7860:7860 inclusive-space-index
```

### Hugging Face Spaces Deployment

1. Fork this repository to your GitHub account
2. Create a new Space on Hugging Face
3. Select Docker as the SDK
4. Connect your GitHub repository
5. Configure email credentials securely:
   - Go to your Space's Settings tab
   - Under "Repository secrets", add the following secrets:
     * `SMTP_HOST`
     * `SMTP_PORT`
     * `SMTP_USER`
     * `SMTP_PASS`
   - These will be securely stored and automatically available as environment variables
6. The Space will automatically build and deploy the application

Note: Never commit email credentials directly to the repository. Always use Hugging Face's secrets management for sensitive data.

## Technical Details

### Assessment Scoring

Each question has five scoring levels:
- None (0 points)
- Basic (0.5 points)
- Partial (1 point)
- Good (2 points)
- Strong (5 points)

### Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- Jinja2 - Template engine
- HTMX - Dynamic HTML updates
- Pandas - Data processing

### Features

#### Real-time Scoring
The assessment includes a real-time scoring system that:
- Shows current total score
- Displays completion progress
- Stays visible while scrolling through questions

#### Email Sharing
Users can opt to receive their results via email. This requires:
- Valid email address
- Consent checkbox for data sharing
- Configured SMTP server

### Environment Variables

#### Required for Basic Operation
- `PYTHONPATH` - Set to the project root
- `PORT` - Default: 7860 (for Hugging Face Spaces compatibility)

#### Required for Email Functionality
To enable email sharing of results, configure these SMTP settings:
- `SMTP_HOST` - Your SMTP server hostname (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP port (typically 587 for TLS)
- `SMTP_USER` - SMTP username/email
- `SMTP_PASS` - SMTP password or app-specific password

Example email setup using Gmail:
1. Create a Gmail account or use an existing one
2. Enable 2-Step Verification in Google Account settings
3. Generate an App Password:
   - Go to Google Account → Security
   - Under "2-Step Verification", select "App passwords"
   - Generate a new app password for "Mail"
4. Set environment variables:
```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your.email@gmail.com
export SMTP_PASS=your-app-password
```

Note: For production deployment:
- On Hugging Face Spaces: Use Repository Secrets as described above
- On other platforms: Use their respective secrets/environment management system

For contribution guidelines, please see CONTRIBUTING.md.
