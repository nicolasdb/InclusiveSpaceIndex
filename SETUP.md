# Setup and Deployment Guide

This guide provides detailed instructions for setting up and deploying the Inclusive Space Index Assessment Tool.

## Prerequisites

- Docker and Docker Compose
- Supabase account (for results storage)
- Questions dataset (CSV or Supabase table)

## Database Setup

### 1. Create Required Tables

Execute the following SQL in your Supabase instance:

```sql
-- For storing evaluation results
CREATE TABLE assessment_results (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    responses JSONB NOT NULL,          -- {question_id: selected_option}
    total_score INTEGER NOT NULL,      -- Raw total score
    total_max INTEGER NOT NULL,        -- Maximum possible score
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- For mailing list subscriptions
CREATE TABLE assessment_mailing_list (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create indexes
CREATE INDEX idx_assessment_results_email ON assessment_results(email);
CREATE INDEX idx_assessment_results_created ON assessment_results(created_at);
```

Note: Email presence in assessment_results indicates data storage consent, while presence in assessment_mailing_list indicates subscription consent.

## Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Required configurations
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 2. Questions Data

Choose one of these options:

#### Option A: CSV Format

Create a CSV file with this structure:

```csv
section,question,option1,option2,option3,option4,option5
"Section Name","Question text","Not implemented","Initial steps taken","Partially implemented","Mostly implemented","Fully implemented"
```

#### Option B: Supabase Table

Create and populate the questions table:

```sql
CREATE TABLE maturity_questions (
    id SERIAL PRIMARY KEY,
    context_id TEXT NOT NULL,
    section TEXT NOT NULL,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    option5 TEXT NOT NULL
);

-- Example insertion
INSERT INTO maturity_questions 
(context_id, section, question, option1, option2, option3, option4, option5)
VALUES 
('default', 'Section Name', 'Question text', 
 'Not implemented', 'Initial steps taken', 'Partially implemented', 
 'Mostly implemented', 'Fully implemented');
```

## Deployment

1. Build and start the container:

   ```bash
   docker compose up --build
   ```

2. Access the application at `http://localhost:8501`

## Troubleshooting

### Common Issues

1. **Database Connection**
   - Verify Supabase URL and key in .env file
   - Check network connectivity
   - Ensure tables exist with correct structure

2. **Questions Loading**
   - Verify questions.csv exists in data directory
   - Check CSV format matches required structure
   - For Supabase: verify table permissions

### Data Management

#### Exporting Results

```sql
SELECT 
    email,
    responses,
    total_score,
    total_max,
    created_at
FROM assessment_results 
ORDER BY created_at DESC;
```

#### Backup Recommendations

- Regularly export assessment data
- Keep CSV backups of questions
- Document any custom modifications

See [TECHNICAL.md](TECHNICAL.md) for implementation details and [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.
