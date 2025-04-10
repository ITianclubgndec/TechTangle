from flask import Flask, render_template, request
import json
import os
import random

app = Flask(__name__)

# Define quiz questions and correct answers
questions = {
    "What is the capital of France?": "Paris",
    "2 + 2 = ?": "4",
    "Which planet is known as the Red Planet?": "Mars",
    "What is the largest ocean?": "Pacific",
    "Who wrote 'Romeo and Juliet'?": "Shakespeare",
    "What is the boiling point of water in Celsius?": "100",
    "What is the square root of 16?": "4",
    "What gas do plants breathe in?": "Carbon dioxide",
    "Who painted the Mona Lisa?": "Da Vinci",
    "In which continent is Egypt located?": "Africa",
    "How many continents are there?": "7",
    "Which planet is closest to the sun?": "Mercury",
    "Who is the founder of Microsoft?": "Bill Gates",
    "What color do you get by mixing red and blue?": "Purple",
    "How many hours in a day?": "24",
    "How many sides does a hexagon have?": "6",
    "Which animal is known as the king of the jungle?": "Lion",
    "How many legs does a spider have?": "8",
    "What is H2O?": "Water",
    "How many days are in a leap year?": "366",
    "Which fruit is yellow and curved?": "Banana",
    "What is the largest mammal?": "Blue whale",
    "Which country is famous for pizza?": "Italy",
    "What is the capital of Japan?": "Tokyo",
    "How many bones are in the human body?": "206",
    "What is the currency of the USA?": "Dollar",
    "Which animal gives us wool?": "Sheep",
    "What do bees make?": "Honey",
    "What is the freezing point of water in Celsius?": "0",
    "What is 10 x 10?": "100"

}

DATA_FILE = 'data.json'
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    select_questions = dict(random.sample(list(questions.items()), 20))
    return render_template('index.html', questions=select_questions)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    urn = request.form.get('urn')
    asked_questions = {q: questions[q] for q in request.form if q in questions}


    # Load existing data
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Check for duplicate submission
    for entry in data:
        if entry['name'] == name or entry['urn'] == urn:
            return render_template(
                'index.html',
                questions=asked_questions,
                duplicate=True,
                name=name,
                urn=urn
            )

    score = 0
    results = {}



    for question, correct_answer in asked_questions.items():

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
        questions=asked_questions,
        submitted=True,
        results=results,
        name=name,
        urn=urn
    )

if __name__ == '__main__':
    app.run(debug=True)