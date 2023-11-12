from flask import Flask, request, render_template , session, redirect, flash
from surveys import satisfaction_survey as survey

app = Flask(__name__)
responses = []
app.config['SECRET_KEY'] = 'balls'

@app.route('/')
def show_home():
    return render_template('home.html', survey = survey)

@app.route('/questions/<int:id>')
def show_question(id):
    if (len(responses) != id):
        flash('invalid question id')
        return redirect(f'/questions/{len(session["responses"])}')
    
    question = survey.questions[id]
    return render_template('question.html', question = question, survey = survey, id = id)

@app.route('/answer', methods = ["POST"])
def log_ans_next_quest():
    
    if request.form:
        choice = request.form['answer']
        responses.append(choice)
        session['responses'] = responses
        
        if len(session['responses']) == len(survey.questions):
            responses.clear()
            session.clear()
            return redirect('/done')

        return redirect(f'/questions/{len(session["responses"])}')
    else:
        flash('You must choose one!')
        return redirect(f'/questions/{len(session["responses"])}')

@app.route('/done')
def done():
    return render_template('done.html')