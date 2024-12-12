import csv
import os

def generate_assessment_widget(csv_file):
    # Get the absolute path to the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)
    # Set output path to root directory with index.html
    widget_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index.html')

    with open(csv_path, 'r') as f:
        reader = list(csv.reader(f))
        
        # Count total number of questions (excluding header)
        total_questions = len(reader) - 1
        max_possible_score = total_questions * 5

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
    
    # Generate question rows
    question_rows = []
    for category, questions in categories.items():
        for question_number, question_details in questions.items():
            row = f"""
            <tr class='section-header'><td colspan='6'>{category} - Question {question_number}</td></tr>
            <tr class="question-row">
                <td class="question">{question_details[0]}</td>
                <td><label><input type="radio" name="{category}-{question_number}" value="0" onclick="calculateScore()">{question_details[1]}</label></td>
                <td><label><input type="radio" name="{category}-{question_number}" value="0.5" onclick="calculateScore()">{question_details[2]}</label></td>
                <td><label><input type="radio" name="{category}-{question_number}" value="1" onclick="calculateScore()">{question_details[3]}</label></td>
                <td><label><input type="radio" name="{category}-{question_number}" value="2" onclick="calculateScore()">{question_details[4]}</label></td>
                <td><label><input type="radio" name="{category}-{question_number}" value="5" onclick="calculateScore()">{question_details[5]}</label></td>
            </tr>
        """
            question_rows.append(row)

    # HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inclusion and Accessibility Assessment</title>
    <link rel="stylesheet" href="styles.css">
    <script>
        const MAX_POSSIBLE_SCORE = {max_possible_score};

        function calculateScore() {{
            let totalScore = 0;

            // Get all radio input elements
            let inputs = document.querySelectorAll('input[type=radio]:checked');

            // Calculate total score
            inputs.forEach(input => {{
                totalScore += parseFloat(input.value);
            }});

            // Update score display
            document.getElementById('totalScore').textContent = totalScore.toFixed(2);
            document.getElementById('maxScore').textContent = MAX_POSSIBLE_SCORE;
        }}
    // Trigger the initial calculation when the page loads
    window.addEventListener('load', calculateScore);
    </script>
</head>
<body>
    <div class="main-content">
        <div class="header">
            <h1>Begin Your Inclusion Journey</h1>        
            <p>Your first steps focus on the essentials of creating a welcoming space. Here, you'll explore basic accessibility and inclusion through practical, achievable goals. From physical accessibility to welcome practices, this assessment will help you reflect on how welcoming your space truly is and you'll discover opportunities to make your space more safe for everyone.</p>
            
            <p>This isn't about achieving a perfect score - it's about honest reflection and identifying areas for growth. Each question is an opportunity to think deeply about your space and community.</p>
            
            <p>Before you begin:</p>
            <ul>
                <li>Take your time to reflect honestly</li>
                <li>If you're unsure about a question, leave it blank - it's better than guessing</li>
                <li>Consider gathering input from different community members</li>
                <li>Remember: this is a starting point for growth, not a final judgment</li>
            </ul>
            
            
            <div id="score">
                <p>Total Score: <span id="totalScore">0</span> / <span id="maxScore">0</span> points</p>
            </div>
        </div>
   
        <div class="questions-container">
            <form>
                <table>
                    {''.join(question_rows)}
                </table>
                <br>
            </form>
        </div>
        <div id="results">
            <p>Want to understand more about the scoring system and what your results mean? <a href="https://github.com/nicolasdb/InclusiveSpaceIndex/blob/diagnostic_inclusion/Framework/level1-scoring.md">Check out our detailed scoring guide</a></p>
        </div>
    </div>
    </body>
</html>"""

    # Write HTML content to file
    with open(widget_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_assessment_widget('assessment-data-L1.csv')
