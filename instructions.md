# Evaluation System Setup Instructions

## Overview

This container provides a Streamlit-based evaluation system that helps organizations assess their maturity level across different sections. The system supports both CSV and Supabase as data sources for questions and stores results with context isolation.

## Prerequisites

- Supabase account (for results storage and optional questions source)
- Docker and Docker Compose
- Questions dataset (CSV or Supabase table)

## Configuration Steps

### 1. Database Setup

Create the following tables in your Supabase instance:

```sql
-- For storing evaluation results with responses only
CREATE TABLE assessment_results (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    responses JSONB NOT NULL,          -- Store just {question_id: selected_option}
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

-- Create indexes for better performance
CREATE INDEX idx_assessment_results_email ON assessment_results(email);
CREATE INDEX idx_assessment_results_created ON assessment_results(created_at);
```

Note: The presence of an email in assessment_results indicates previous consent to store data, while presence in assessment_mailing_list indicates previous subscription to updates.

### 2. Environment Variables

Create a `.env` file in the project root directory with the following variables:

```
# Required configurations
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Note: The questions file path is configured in `compose.yml` and defaults to `/app/data/questions.csv`

### 3. Questions Format

#### Option 1: CSV Format

Create a CSV file with the following structure:

```csv
section,question,option1,option2,option3,option4,option5
"Section Name","Question text","Not implemented","Initial steps taken","Partially implemented","Mostly implemented","Fully implemented"
```

#### Option 2: Supabase Questions Table

If using Supabase for questions, insert them using:

```sql
INSERT INTO maturity_questions 
(context_id, section, question, option1, option2, option3, option4, option5)
VALUES 
('your_context_id', 'Section Name', 'Question text', 
 'Not implemented', 'Initial steps taken', 'Partially implemented', 'Mostly implemented', 'Fully implemented');
```

### 4. Deployment

1. Build and start the container:

   ```bash
   docker compose up --build
   ```

2. Access the application at `http://localhost:8501`

## Customization

### Scoring System

The system uses an exponential scoring progression to better reflect maturity levels:

Each question has five options with exponential point values:
1. Not implemented (0 points)
2. Initial steps taken (1 point)
3. Partially implemented (2 points)
4. Mostly implemented (4 points)
5. Fully implemented (8 points)

This exponential progression (0→1→2→4→8) emphasizes the value of full implementation while providing meaningful recognition for partial progress. The doubling of points at each level creates a clear distinction between maturity stages.

Scores are stored and displayed in two formats:
- Raw points: The actual points earned (e.g., "16/40" means 16 points out of a possible 40)
- Percentage: Points converted to a percentage for easier comparison (e.g., "40%")

### Data Storage

Results are stored with:
- Responses for each question (as {question_id: selected_option})
- Total score and maximum possible points
- Timestamp of submission
- Section scores are calculated on-the-fly from responses

### Question Options

Questions are grouped by sections, and each question offers five progressive options. The exponential scoring system encourages progression through maturity levels while making the differences between levels more significant.

## Troubleshooting

### Common Issues

1. Database Connection:
   - Verify Supabase URL and key in .env file
   - Check network connectivity
   - Ensure tables are created with correct structure

2. Questions Loading:
   - Check if questions.csv exists in the data directory
   - Verify CSV file format matches required structure

### Data Export

Results can be exported from Supabase using:

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

This will return complete evaluation data including all responses and detailed scores.
