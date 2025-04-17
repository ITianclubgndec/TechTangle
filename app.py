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

DATA_FILE = 'data.jsonl'
MCQ_DATA_FILE = 'mcq_data.jsonl'

# Check if the files exist, otherwise create them
if not os.path.exists(DATA_FILE):
    open(DATA_FILE, 'w').close()

if not os.path.exists(MCQ_DATA_FILE):
    open(MCQ_DATA_FILE, 'w').close()

def read_jsonl(file_type='quiz'):
    """
    Read data from a JSONL file based on the type ('quiz' or 'mcq').
    """
    data = []
    file_name = DATA_FILE if file_type == 'quiz' else MCQ_DATA_FILE
    with open(file_name, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass
    return data

def write_jsonl_entry(entry, file_type='quiz'):
    """
    Write a new entry to the corresponding JSONL file based on the type ('quiz' or 'mcq').
    """
    file_name = DATA_FILE if file_type == 'quiz' else MCQ_DATA_FILE
    with open(file_name, 'a') as f:
        f.write(json.dumps(entry) + '\n')

@app.route('/')
def index():
    select_questions = dict(random.sample(list(questions.items()), 20))
    return render_template('index.html', questions=select_questions)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    urn = request.form.get('urn')
    email = request.form.get('email') 
    asked_questions = {q: questions[q] for q in request.form if q in questions}

    data = read_jsonl(DATA_FILE)

    # Check for duplicate
    for entry in data:
        if entry['name'] == name or entry['urn'] == urn or entry['email']==email:
            return render_template(
                'index.html',
                questions=asked_questions,
                duplicate=True,
                name=name,
                urn=urn,
                email=email
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

    # Save result
    new_entry = {"name": name, "urn": urn,"email":email, "marks": score}
    write_jsonl_entry(new_entry,DATA_FILE)

    return render_template(
        'index.html',
        questions=asked_questions,
        submitted=True,
        results=results,
        name=name,
        urn=urn,
        email=email,
        score=score
    )

questions_round = {
    "What is the output of print(2 ** 3)?": {
        "options": ["6", "8", "9", "5"],
        "answer": "8"
    },
    "Which of the following is a mutable data type in Python?": {
        "options": ["tuple", "str", "list", "int"],
        "answer": "list"
    },
    "What does the 'len()' function do in Python?": {
        "options": [
            "Deletes an element",
            "Returns the length of an object",
            "Changes the case of a string",
            "Prints data"
        ],
        "answer": "Returns the length of an object"
    },
    "What keyword is used to define a function in Python?": {
        "options": ["function", "define", "def", "fun"],
        "answer": "def"
    },
    "What is the correct file extension for Python files?": {
        "options": [".pt", ".pyt", ".py", ".p"],
        "answer": ".py"
    },
    "Which of the following is a valid variable name?": {
        "options": ["1name", "name!", "_name", "class"],
        "answer": "_name"
    },
    "What does '=='' operator do in Python?": {
        "options": ["Assigns value", "Checks equality", "Checks identity", "None of the above"],
        "answer": "Checks equality"
    },
    "What data type is the result of: 5 / 2 in Python 3?": {
        "options": ["int", "float", "str", "bool"],
        "answer": "float"
    },
    "Which of these is used to handle exceptions in Python?": {
        "options": ["if-else", "for", "try-except", "switch-case"],
        "answer": "try-except"
    },
    "What is the output of: print('Hello' + 'World')?": {
        "options": ["Hello World", "Hello+World", "HelloWorld", "Error"],
        "answer": "HelloWorld"
    }
}


@app.route('/round')
def round():
    selected = dict(random.sample(list(questions_round.items()), 5))

    question_list = [
        {
            "question": q,
            "options": data["options"]
        }
        for q, data in selected.items()
    ]

    return render_template('round.html', questions=question_list)

@app.route('/round_submit', methods=['POST'])
def round_submit():
    name = request.form.get('name')
    urn = request.form.get('urn')
    email = request.form.get('email')

    data = read_jsonl(MCQ_DATA_FILE)

    # Check for duplicates
    for entry in data:
        if entry['name'] == name or entry['urn'] == urn or entry['email'] == email:
            asked_questions = []
            for key in request.form:
                if key.startswith('q'):
                    q_index = int(key[1:])
                    question = request.form.get(f"question{q_index}")
                    if question and question in questions_round:
                        asked_questions.append({
                            "question": question,
                            "options": questions_round[question]["options"],
                            "selected": request.form.get(f"q{q_index}"),
                            "correct": questions_round[question]["answer"]
                        })
            return render_template(
                'round.html',
                questions=asked_questions,
                duplicate=True,
                name=name,
                urn=urn,
                email=email
            )

    score = 0
    results = []

    for key in request.form:
        if key.startswith('q') and key[1:].isdigit():
            q_index = int(key[1:])
            question = request.form.get(f"question{q_index}")
            user_answer = request.form.get(f"q{q_index}")

            if question and question in questions_round:
                correct_answer = questions_round[question]["answer"]
                is_correct = (user_answer.strip().lower() == correct_answer.lower())
                if is_correct:
                    score += 1

                results.append({
                    "question": question,
                    "options": questions_round[question]["options"],
                    "selected": user_answer,
                    "correct": correct_answer,
                    "is_correct": is_correct
                })

    # Save new result
    new_entry = {"name": name, "urn": urn, "email": email, "marks": score}
    write_jsonl_entry(new_entry,MCQ_DATA_FILE)

    return render_template(
        'round.html',
        questions=results,
        submitted=True,
        name=name,
        urn=urn,
        email=email,
        score=score
    )
if __name__ == '__main__':
    app.run(debug=True)
