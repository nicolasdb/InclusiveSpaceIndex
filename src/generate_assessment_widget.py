import os
import pandas as pd

def load_assessment_data():
    """Load assessment data from CSV file"""
    try:
        # Get the absolute path to the CSV file
        csv_path = os.path.join(os.path.dirname(__file__), 'assessment-data-L1.csv')
        
        # Read the CSV file using pandas
        data = pd.read_csv(csv_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Assessment data file not found at {csv_path}. Please ensure the CSV file is in the src directory.")
    except Exception as e:
        raise Exception(f"Error loading assessment data: {str(e)}")

def generate_assessment_widget():
    """Generate HTML widget for assessment"""
    try:
        # Load assessment data
        assessment_data = load_assessment_data()
        
        # Generate HTML widget
        widget_html = '<div class="assessment-container">'
        
        # Track categories for scoring
        total_questions = len(assessment_data)
        max_possible_score = total_questions * 5

        for idx, row in assessment_data.iterrows():
            section = row['section']
            question_number = row['question_number']
            question_text = row['question']
            
            # Collect descriptions for different scoring levels
            descriptions = [
                row['none_description'],
                row['basic_description'],
                row['partial_description'],
                row['good_description'],
                row['strong_description']
            ]
            
            # Create radio button group for this question
            widget_html += f'''
            <div class="assessment-section">
                <div class="category-header">{section} - Question {question_number}</div>
                <label for="q{idx}">{question_text}</label>
                <div class="assessment-options">
                    <div class="radio-group">
                        <input type="radio" id="q{idx}_0" name="q{idx}" value="0" onclick="calculateScore()">
                        <label for="q{idx}_0">{descriptions[0]}</label>
                    </div>
                    <div class="radio-group">
                        <input type="radio" id="q{idx}_0.5" name="q{idx}" value="0.5" onclick="calculateScore()">
                        <label for="q{idx}_0.5">{descriptions[1]}</label>
                    </div>
                    <div class="radio-group">
                        <input type="radio" id="q{idx}_1" name="q{idx}" value="1" onclick="calculateScore()">
                        <label for="q{idx}_1">{descriptions[2]}</label>
                    </div>
                    <div class="radio-group">
                        <input type="radio" id="q{idx}_2" name="q{idx}" value="2" onclick="calculateScore()">
                        <label for="q{idx}_2">{descriptions[3]}</label>
                    </div>
                    <div class="radio-group">
                        <input type="radio" id="q{idx}_5" name="q{idx}" value="5" onclick="calculateScore()">
                        <label for="q{idx}_5">{descriptions[4]}</label>
                    </div>
                </div>
            </div>
            '''
        
        widget_html += f'''
        </div>
        <script>
        const MAX_POSSIBLE_SCORE = {max_possible_score};
        const TOTAL_QUESTIONS = {total_questions};

        function calculateScore() {{
            let totalScore = 0;
            let answeredQuestions = 0;
            let inputs = document.querySelectorAll('input[type=radio]:checked');

            inputs.forEach(input => {{
                totalScore += parseFloat(input.value);
                answeredQuestions++;
            }});

            // Update score
            let scoreDisplay = document.getElementById('totalScore');
            let maxScoreDisplay = document.getElementById('maxScore');
            if (scoreDisplay && maxScoreDisplay) {{
                scoreDisplay.textContent = totalScore.toFixed(2);
                maxScoreDisplay.textContent = MAX_POSSIBLE_SCORE;
            }}

            // Update progress
            let progressPercent = (answeredQuestions / TOTAL_QUESTIONS) * 100;
            let progressFill = document.getElementById('progressFill');
            let progressText = document.getElementById('progressText');
            if (progressFill && progressText) {{
                progressFill.style.width = progressPercent + '%';
                progressText.textContent = Math.round(progressPercent) + '%';
            }}
        }}
        </script>
        <div class="score-tracker">
            <div class="progress-bar">
                <div id="progressFill" class="progress-fill" style="width: 0%"></div>
            </div>
            <p>Completion: <span id="progressText">0%</span></p>
            <p>Total Score: <span id="totalScore">0</span> / <span id="maxScore">{max_possible_score}</span> points</p>
        </div>
        '''
        
        return widget_html
    except Exception as e:
        raise Exception(f"Error generating assessment widget: {str(e)}")

if __name__ == "__main__":
    print(generate_assessment_widget())
