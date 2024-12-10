import csv

def generate_assessment_widget(csv_file):
    # Read the CSV file to load questions
    with open(csv_file, "r", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        questions = list(reader)

    # Group questions by category and question number
    categories = {}
    for question in questions:
        section, question_number, question_text, none_description, basic_description, partial_description, good_description, strong_description = question
        if section not in categories:
            categories[section] = {}
        if question_number not in categories[section]:
            categories[section][question_number] = []
        categories[section][question_number].append((question_text, none_description, basic_description, partial_description, good_description, strong_description))

    # Generate HTML for the widget
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inclusion and Accessibility Assessment</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            table {
                width: auto;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            td.question {
                width: 300px;
            }
            button {
                margin: 5px;
                padding: 10px;
                font-size: 14px;
            }
            .section-header {
                background-color: #e0e0e0;
                font-weight: bold;
            }
            .question-row:nth-child(even) {
                background-color: #f9f9f9;
            }
            .question-row:nth-child(odd) {
                background-color: #e6f7ff;
            }
        </style>
        <script>
            function calculateScore() {
                let categoryScores = {};
                let categoryCounts = {};

                let inputs = document.querySelectorAll('input[type=radio]:checked');

                inputs.forEach(input => {
                    let category = input.name.split('-')[0];
                    let questionNumber = input.name.split('-')[1];
                    let value = parseInt(input.value);

                    if (!categoryScores[category]) {
                        categoryScores[category] = { sum: 0 };
                        categoryCounts[category] = { count: 0 };
                    }

                    categoryScores[category].sum += value;
                    categoryCounts[category].count += 1;
                });

                let results = '';
                let totalScore = 0;
                let categoryNames = Object.keys(categoryScores);

                categoryNames.forEach(category => {
                    let sum = categoryScores[category].sum;
                    let n = categoryCounts[category].count;

                    let rawScore = sum;
                    let maxPossibleScore = 5 * n;

                    let normalizedScore = (rawScore / maxPossibleScore) * 100;

                    totalScore += normalizedScore;
                    results += `${category} Category Score: ${normalizedScore.toFixed(2)} / 100<br>`;
                });

                let aggregateScore = totalScore / categoryNames.length;
                results += `<br>Aggregate Score: ${aggregateScore.toFixed(2)} / 100`;

                document.getElementById('results').innerHTML = results;
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: "smooth",
                });
            }

            function debugSetAll(value) {
                let inputs = document.querySelectorAll('input[type=radio]');

                inputs.forEach(input => {
                    if (parseInt(input.value) === value) {
                        input.checked = true;
                    }
                });
            }
        </script>
    </head>
    <body>
        <h2>Inclusion and Accessibility Assessment</h2>
        <p>When marking this assessment, please use the following guidelines:</p>
        <ul>
            <li>1 - No accessibility considerations</li>
            <li>2 - Awareness of needs, planning stage</li>
            <li>3 - Some accommodations (like a temporary ramp)</li>
            <li>4 - Permanent ramp, wide doors</li>
            <li>5 - Automatic doors, multiple access options</li>
        </ul>
        <form>
            <table>
                <tr>
                    <th>Question</th>
                    <th>1</th>
                    <th>2</th>
                    <th>3</th>
                    <th>4</th>
                    <th>5</th>
                </tr>
    """

    # Generate the question rows for each category and question number
    for category, questions in categories.items():
        for question_number, question_details in questions.items():
            html_content += f"<tr class='section-header'><td colspan='6'>{category} - Question {question_number}</td></tr>"
            for question_text, none_description, basic_description, partial_description, good_description, strong_description in question_details:
                html_content += f"""
                    <tr class="question-row">
                        <td class="question">{question_text}</td>
                        <td><input type="radio" name="{category}-{question_number}" value="1" data-type="1">{none_description}</td>
                        <td><input type="radio" name="{category}-{question_number}" value="2" data-type="2">{basic_description}</td>
                        <td><input type="radio" name="{category}-{question_number}" value="3" data-type="3">{partial_description}</td>
                        <td><input type="radio" name="{category}-{question_number}" value="4" data-type="4">{good_description}</td>
                        <td><input type="radio" name="{category}-{question_number}" value="5" data-type="5">{strong_description}</td>
                    </tr>
                """

    # Close the HTML content
    html_content += """
            </table>
            <br>
            <button type="button" onclick="calculateScore()">Generate Score</button>
            <button type="button" onclick="debugSetAll(1)">Debug (Set All to 1)</button>
            <button type="button" onclick="debugSetAll(2)">Debug (Set All to 2)</button>
            <button type="button" onclick="debugSetAll(3)">Debug (Set All to 3)</button>
            <button type="button" onclick="debugSetAll(4)">Debug (Set All to 4)</button>
            <button type="button" onclick="debugSetAll(5)">Debug (Set All to 5)</button>
        </form>
        <div id="results"></div>
    </body>
    </html>
    """

    # Write HTML content to file
    with open('widget.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_assessment_widget('Framework/assessment-data-L1.csv')
