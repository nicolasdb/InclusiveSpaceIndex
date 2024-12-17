import csv
import os

def generate_assessment_markdown(csv_file):
    # Get the absolute path to the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)
    # Set output path to root directory with assessment.md
    markdown_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assessment.md')

    with open(csv_path, 'r') as f:
        reader = list(csv.reader(f))
        
        # Count total number of questions (excluding header)
        total_questions = len(reader) - 1
        max_possible_score = total_questions * 5

    # Generate markdown content
    markdown_content = f"""# Inclusion and Accessibility Assessment

## Introduction

Your first steps focus on the essentials of creating a welcoming space. This assessment will help you explore basic accessibility and inclusion through practical, achievable goals.

### Before You Begin:
- Take your time to reflect honestly
- If you're unsure about a question, leave it blank
- Consider gathering input from different community members
- Remember: this is a starting point for growth, not a final judgment

## Assessment Questionnaire

| Category | Question | None (0) | Basic (0.5) | Partial (1) | Good (2) | Strong (5) |
|----------|----------|----------|-------------|-------------|----------|------------|
"""

    # Organize questions by category
    categories = {}
    for row in reader[1:]:  # Skip header row
        category = row[0]
        question_number = row[1]
        question_text = row[2]
        none_description = row[3]
        basic_description = row[4]
        partial_description = row[5]
        good_description = row[6]
        strong_description = row[7]

        if category not in categories:
            categories[category] = {}

        categories[category][question_number] = [
            question_text,
            none_description,
            basic_description,
            partial_description,
            good_description,
            strong_description
        ]

    # Add questions to markdown table
    for category, questions in categories.items():
        for question_number, question_details in questions.items():
            markdown_content += f"| {category} | Q{question_number}: {question_details[0]} | {question_details[1]} | {question_details[2]} | {question_details[3]} | {question_details[4]} | {question_details[5]} |\n"

    # Add scoring information
    markdown_content += f"""
## Scoring Information

- Total Questions: {total_questions}
- Maximum Possible Score: {max_possible_score} points

### Scoring Guide
- **None (0)**: No evidence of practice
- **Basic (0.5)**: Minimal or initial steps
- **Partial (1)**: Some implementation
- **Good (2)**: Substantial progress
- **Strong (5)**: Comprehensive and exemplary practice

[Detailed Scoring Guide](https://github.com/nicolasdb/InclusiveSpaceIndex/blob/diagnostic_inclusion/Framework/level1-scoring.md)
"""

    # Write markdown content to file
    with open(markdown_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Assessment markdown generated at {markdown_file_path}")

if __name__ == "__main__":
    generate_assessment_markdown('assessment-data-L1.csv')
