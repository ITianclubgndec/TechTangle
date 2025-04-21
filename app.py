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
MCQ_DATA_FILE_ROUND2 = 'mcq_data2.jsonl'

# Check if the files exist, otherwise create them
if not os.path.exists(DATA_FILE):
    open(DATA_FILE, 'w').close()

if not os.path.exists(MCQ_DATA_FILE):
    open(MCQ_DATA_FILE, 'w').close()
if not os.path.exists(MCQ_DATA_FILE_ROUND2):
    open(MCQ_DATA_FILE_ROUND2, 'w').close()

def read_jsonl(file_type='quiz', sort_by=None, descending=False):
    data = []
    if file_type == 'quiz':
        file_name = DATA_FILE
    elif file_type == 'mcq':
        file_name = MCQ_DATA_FILE
    elif file_type == 'round2':
        file_name = MCQ_DATA_FILE_ROUND2
    else:
        return data  # unknown type, return empty

    with open(file_name, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass

    if sort_by:
        try:
            data.sort(key=lambda x: x.get(sort_by, 0), reverse=descending)
        except Exception as e:
            print(f"Error while sorting: {e}")

    return data



def write_jsonl_entry(entry, file_type='quiz'):
    if file_type == 'quiz':
        file_name = DATA_FILE
    elif file_type == 'mcq':
        file_name = MCQ_DATA_FILE
    elif file_type == 'round2':
        file_name = MCQ_DATA_FILE_ROUND2
    else:
        return  # unknown type, don't write

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

    data = read_jsonl('quiz',sort_by='marks',descending=True)

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
    write_jsonl_entry(new_entry,'quiz')

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
    "Who is known as the \"Father of the Computer\"?": {
        "options": ["Alan Turing", "Charles Babbage", "John von Neumann", "Steve Jobs"],
        "answer": "Charles Babbage"
    },
    "Who is the current chairman of ISRO (as of 2025)?": {
        "options": ["K. Sivan", "G. Madhavan Nair", "S. Somanath", "Vikram Sarabhai"],
        "answer": "S. Somanath"
    },
    "Which company originally developed the Android OS?": {
        "options": ["Microsoft", "Google", "Android Inc.", "IBM"],
        "answer": "Android Inc."
    },
    "Which programming language is known as the \"mother of all languages\"?": {
        "options": ["Python", "Java", "Assembly", "C"],
        "answer": "C"
    },
    "Which Indian city is known as the Silicon Valley of India?": {
        "options": ["Mumbai", "Hyderabad", "Pune", "Bengaluru"],
        "answer": "Bengaluru"
    },
    "Who invented the World Wide Web?": {
        "options": ["Bill Gates", "Vint Cerf", "Tim Berners-Lee", "Steve Jobs"],
        "answer": "Tim Berners-Lee"
    },
    "What does RFID stand for?": {
        "options": ["Radio Frequency Interface Device", "Random Frequency Identification", "Radio Frequency Identification", "Rapid Frequency Internal Data"],
        "answer": "Radio Frequency Identification"
    },
    "What is the name of India’s first indigenous aircraft carrier?": {
        "options": ["INS Arihant", "INS Vikrant", "INS Viraat", "INS Shivalik"],
        "answer": "INS Vikrant"
    },
    "Which language is primarily used for iOS app development?": {
        "options": ["Kotlin", "Java", "Swift", "Objective-J"],
        "answer": "Swift"
    },
    "What is the name of the Indian space mission to study the Sun?": {
        "options": ["Gaganyaan", "Chandrayaan-3", "Aditya-L1", "Surya-X"],
        "answer": "Aditya-L1"
    },
    "What does HTTP stand for?": {
        "options": ["HyperText Transfer Page", "HighText Transfer Protocol", "HyperText Transfer Protocol", "Hyper Transport Transfer Protocol"],
        "answer": "HyperText Transfer Protocol"
    },
    "Who is known as the father of artificial intelligence?": {
        "options": ["Marvin Minsky", "Alan Turing", "John McCarthy", "Elon Musk"],
        "answer": "John McCarthy"
    },
    "What is the full form of CAPTCHA?": {
        "options": ["Completely Automated Public Turing test to tell Computers and Humans Apart", "Computerized Automated Program for Testing", "Certified AI Programming Challenge", "Code Automated Program Test"],
        "answer": "Completely Automated Public Turing test to tell Computers and Humans Apart"
    },
    "What does USB stand for?": {
        "options": ["Unique Serial Bus", "Universal Serial Bus", "Unified System Base", "Universal System Board"],
        "answer": "Universal Serial Bus"
    },
    "Which tech company has a fruit as its logo?": {
        "options": ["Blackberry", "Apple", "Banana", "CherrySoft"],
        "answer": "Apple"
    },
    "Which is the most commonly used computer keyboard layout?": {
        "options": ["AZERTY", "QWERTY", "DVORAK", "ABCDEF"],
        "answer": "QWERTY"
    },
    "What is the brain of the computer called?": {
        "options": ["RAM", "Hard Drive", "CPU", "GPU"],
        "answer": "CPU"
    },
    "What does BIOS stand for?": {
        "options": ["Binary Integrated Operating System", "Basic Input Output System", "Basic Internal Operation Service", "Base IO Stream"],
        "answer": "Basic Input Output System"
    },
    "What is the shortcut key to paste in most operating systems?": {
        "options": ["Ctrl + P", "Ctrl + C", "Ctrl + V", "Ctrl + X"],
        "answer": "Ctrl + V"
    },
    "Which device is used to connect to the Internet?": {
        "options": ["Router", "Scanner", "Printer", "CPU"],
        "answer": "Router"
    },
    "Which planet is known as the Red Planet?": {
        "options": ["Earth", "Mars", "Venus", "Jupiter"],
        "answer": "Mars"
    },
    "Who wrote the play Romeo and Juliet?": {
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": "William Shakespeare"
    },
    "What is the capital of Japan?": {
        "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"],
        "answer": "Tokyo"
    },
    "What is the largest mammal in the world?": {
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "answer": "Blue Whale"
    },
    "In which year did World War II end?": {
        "options": ["1939", "1942", "1945", "1950"],
        "answer": "1945"
    },
    "What is the chemical symbol for Gold?": {
        "options": ["Au", "Ag", "Gd", "Go"],
        "answer": "Au"
    },
    "Who was the first person to step on the Moon?": {
        "options": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"],
        "answer": "Neil Armstrong"
    },
    "Which continent is the Sahara Desert located in?": {
        "options": ["Asia", "Australia", "Africa", "South America"],
        "answer": "Africa"
    },
    "What is the hardest natural substance on Earth?": {
        "options": ["Steel", "Iron", "Diamond", "Quartz"],
        "answer": "Diamond"
    },
    "Which organ in the human body is primarily responsible for filtering blood?": {
        "options": ["Heart", "Liver", "Lungs", "Kidneys"],
        "answer": "Kidneys"
    }
}

questions_round2={
    "Which protocol is used to send emails?": {
        "options": ["FTP", "SMTP", "HTTP", "SNMP"],
        "answer": "SMTP"
    },
    "Which layer of the OSI model is responsible for routing?": {
        "options": ["Data Link Layer", "Network Layer", "Session Layer", "Application Layer"],
        "answer": "Network Layer"
    },
    "What does DNS stand for?": {
        "options": ["Digital Network System", "Domain Name System", "Direct Node Setup", "Dynamic Network Setup"],
        "answer": "Domain Name System"
    },
    "What is the default port for HTTP?": {
        "options": ["80", "21", "443", "25"],
        "answer": "80"
    },
    "What is Git primarily used for?": {
        "options": ["Hosting websites", "Database management", "Version control", "Virtualization"],
        "answer": "Version control"
    },
    "What is the use of an API?": {
        "options": ["Anti-virus Protocol Interface", "Application Programming Interface", "Automated Program Interaction", "Application Protection Integrator"],
        "answer": "Application Programming Interface"
    },
    "What is the time complexity of binary search?": {
        "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
        "answer": "O(log n)"
    },
    "Which language runs in a browser and on the server (Node.js)?": {
        "options": ["Python", "Java", "JavaScript", "C++"],
        "answer": "JavaScript"
    },
    "What does CSS stand for?": {
        "options": ["Central Style Script", "Cascading Style Sheets", "Computer Style Syntax", "Custom Styling Software"],
        "answer": "Cascading Style Sheets"
    },
    "Which database is known for being document-oriented?": {
        "options": ["MySQL", "PostgreSQL", "MongoDB", "Oracle"],
        "answer": "MongoDB"
    },
    "What is a loop that never ends called?": {
        "options": ["Closed loop", "Infinite loop", "Dead loop", "While loop"],
        "answer": "Infinite loop"
    },
    "Which tag is used to create a hyperlink in HTML?": {
        "options": ["<link>", "<href>", "<a>", "<url>"],
        "answer": "<a>"
    },
    "What does CRUD stand for in databases?": {
        "options": ["Create Read Update Delete", "Control Run Update Deploy", "Create Replicate Use Delete", "Copy Read Upload Dump"],
        "answer": "Create Read Update Delete"
    },
    "Which language is compiled, not interpreted?": {
        "options": ["JavaScript", "Python", "Java", "PHP"],
        "answer": "Java"
    },
    "What is the output of 2 ** 3 in Python?": {
        "options": ["6", "9", "8", "Error"],
        "answer": "8"
    },
    "Which of the following is not a data type in Python?": {
        "options": ["int", "str", "real", "list"],
        "answer": "real"
    },
    "In OOP, what does 'inheritance' allow?": {
        "options": ["Hiding of data", "Polymorphism", "Code reuse from another class", "Looping"],
        "answer": "Code reuse from another class"
    },
    "Which HTTP method is used to update a resource?": {
        "options": ["GET", "POST", "PUT", "FETCH"],
        "answer": "PUT"
    },
    "In React, what is used to manage state in functional components?": {
        "options": ["setState", "useState", "this.state", "Redux"],
        "answer": "useState"
    },
    "What is Django?": {
        "options": ["Webbrowser", "Programming language", "Web framework for Python", "Java IDE"],
        "answer": "Web framework for Python"
    }
}



@app.route('/round')
def round():
    selected = dict(random.sample(list(questions_round.items()), 20))

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

    data = read_jsonl('mcq',sort_by='marks',descending=True)

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
    write_jsonl_entry(new_entry,'mcq')

    return render_template(
        'round.html',
        questions=results,
        submitted=True,
        name=name,
        urn=urn,
        email=email,
        score=score
    )
@app.route('/round_two')
def round_two():
    selected = dict(random.sample(list(questions_round2.items()),20))

    question_list = [
        {
            "question": q,
            "options": data["options"]
        }
        for q, data in selected.items()
    ]

    return render_template('round_two.html', questions=question_list)

@app.route('/round_two_submit', methods=['POST'])
def round_two_submit():
    name = request.form.get('name')
    urn = request.form.get('urn')
    email = request.form.get('email')

    data = read_jsonl('round2',sort_by='marks',descending=True)


    # Check for duplicates
    for entry in data:
        if entry['name'] == name or entry['urn'] == urn or entry['email'] == email:
            asked_questions = []
            for key in request.form:
                if key.startswith('q') and key[1:].isdigit():
                    q_index = int(key[1:])
                    question = request.form.get(f"question{q_index}")
                    if question and question in questions_round2:
                        asked_questions.append({
                            "question": question,
                            "options": questions_round2[question]["options"],
                            "selected": request.form.get(f"q{q_index}"),
                            "correct": questions_round2[question]["answer"]
                        })
            return render_template(
                'round_two.html',
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

            if question and question in questions_round2:
                correct_answer = questions_round2[question]["answer"]
                is_correct = (user_answer.strip().lower() == correct_answer.lower())
                if is_correct:
                    score += 1

                results.append({
                    "question": question,
                    "options": questions_round2[question]["options"],
                    "selected": user_answer,
                    "correct": correct_answer,
                    "is_correct": is_correct
                })

    # Save new result
    new_entry = {"name": name, "urn": urn, "email": email, "marks": score}
    write_jsonl_entry(new_entry, 'round2')


    return render_template(
        'round_two.html',
        questions=results,
        submitted=True,
        name=name,
        urn=urn,
        email=email,
        score=score
    )
@app.route('/results')
def results():
    data = read_jsonl('quiz')
    sorted_data = sorted(data, key=lambda x: x.get('marks', 0), reverse=True)
    return render_template('results.html', data=sorted_data, title='Quiz Results')
@app.route('/results_round_one')
def mcq_results():
    data = read_jsonl('mcq')
    sorted_data = sorted(data, key=lambda x: x.get('marks', 0), reverse=True)
    return render_template('results.html', data=sorted_data, title='Round1 Results')
@app.route('/results_round_two')
def results_round_two():
    data = read_jsonl('round2')
    sorted_data = sorted(data, key=lambda x: x.get('marks', 0), reverse=True)
    return render_template('results.html', data=sorted_data, title='Round2 Results')
if __name__ == '__main__':
    app.run(debug=True)
