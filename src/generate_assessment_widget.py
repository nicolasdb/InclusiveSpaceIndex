import csv
import os

def generate_assessment_widget(csv_file):
    # Get the absolute path to the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)
    widget_file_path = os.path.join(os.path.dirname(csv_path), 'widget.html')



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
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inclusion and Accessibility Assessment</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        
        .header {{
            background-color: #f2f2f2;
            padding: 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1;
        }}
        
        .questions-container {{
            margin-top: 270px;
            padding: 20px;
            max-height: calc(100vh - 240px);
            overflow-y: auto;
        }}
        
        table {{
            width: auto;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 10px;
            text-align: left;
        }}
        
        th {{
            background-color: #f2f2f2;
        }}
        
        td.question {{
            width: 300px;
        }}
        
        button {{
            margin: 5px;
            padding: 10px;
            font-size: 14px;
        }}
        
        .section-header {{
            background-color: #e0e0e0;
            font-weight: bold;
        }}
        
        .question-row:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .question-row:nth-child(odd) {{
            background-color: #e6f7ff;
        }}
    </style>
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
    <div class="header">
        <h2>Inclusion and Accessibility Assessment</h2>
        <p>When marking this assessment, please use the following guidelines:</p>
        <ul>
            <li>1 - No accessibility considerations</li>
            <li>2 - Awareness of needs, planning stage</li>
            <li>3 - Some accommodations (like a temporary ramp)</li>
            <li>4 - Permanent ramp, wide doors</li>
            <li>5 - Automatic doors, multiple access options</li>
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
        <div id="results"></div>
    </body>
</html>
    """

    # Write HTML content to file
    with open(widget_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_assessment_widget('assessment-data-L1.csv')
