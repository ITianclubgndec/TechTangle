from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Define quiz questions and correct answers
questions = {
    "What is the capital of France?": "Paris",
    "2 + 2 = ?": "4",
    "Which planet is known as the Red Planet?": "Mars"
}

DATA_FILE = 'data.json'
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    urn = request.form.get('urn')

    # Load existing data
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Check for duplicate submission
    for entry in data:
        if entry['name'] == name and entry['urn'] == urn:
            return render_template(
                'index.html',
                questions=questions,
                duplicate=True,
                name=name
            )

    score = 0
    results = {}

    for question, correct_answer in questions.items():
        user_answer = request.form.get(question)
        is_correct = (user_answer.strip().lower() == correct_answer.lower())
        results[question] = {
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        }
        if is_correct:
            score += 1

    # Add new result
    data.append({"name": name, "urn": urn, "marks": score})
    data.sort(key=lambda x: x["marks"], reverse=True)

    # Save updated results
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return render_template(
        'index.html',
        questions=questions,
        submitted=True,
        results=results,
        name=name
    )

if __name__ == '__main__':
    app.run(debug=True)
