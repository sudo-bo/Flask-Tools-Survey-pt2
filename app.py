from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'baba-yaga'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

@app.route("/")
def root():
    return render_template('home.html')

@app.route('/user-responses', methods=["POST"])
def store_responses():
    session['responses'] = []
    return redirect('/questions/1')

questions = surveys.satisfaction_survey.questions
@app.route("/questions/<int:num>")
def question_page(num):
    current_question = session.get('current_question', 1)  # Retrieve current_question from session, defaulting to 1
    if current_question == num: # checks if we are on the right question
        if num <= len(questions):  # checks if the current question is out of bounds
            question = questions[num-1].question
            choices = questions[num-1].choices
            text = questions[num-1].allow_text
            current_question +=1 # increment for preparation of next question, since work with the current question is finished
            return render_template('questions.html', number=num, question=question, choices=choices, text_option=text, last="False")
        else: 
            return redirect('/thank_you')
    else:
        # current_question -= 1 # go back to proper question
        flash('Please answer the questions in order!')
        return redirect(f'/questions/{current_question}')   


@app.route("/answer/<int:num>", methods=["POST"])
def answer_response(num):
    user_choice = request.form.get('user_choice')

    responses = session['responses']
    responses.append(user_choice)
    session['responses'] = responses
    session['current_question'] = num + 1

    print(f'{responses[num - 1]}')
    return redirect(f'/questions/{num + 1}')

@app.route("/thank_you")
def thank_you_page():
    current_question = session['current_question']
    if current_question >= len(questions):
        session['current_question'] = 1
        return render_template('thank_you.html')
    else:
        return redirect(f'/questions/{current_question}') 
    
# some thoughts:
# why use a post request instead of a get request for the home page when starting the survey, 
# is there a better way to store the current page and stop a user from skipping ahead, 
# is session the right way to go, and would this be considered refactoring code
# using two tabs to answer the survey leads to some issues