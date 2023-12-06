from flask import Flask, request, render_template, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.secret_key = 'baba-yaga'
# toolbar = DebugToolbarExtension(app)

responses = []
@app.route("/")
def root():
    return render_template('home.html')


questions = surveys.satisfaction_survey.questions
current_question = 1 # start on the first question
@app.route("/questions/<int:num>")
def question_page(num):
    global current_question
    if current_question == num:
        current_question +=1 # indicate we are on the next question
        if num <= len(questions):  
            question = questions[num-1].question
            choices = questions[num-1].choices
            text = questions[num-1].allow_text
            return render_template('questions.html', number=num, question=question, choices=choices, text_option=text, last="False")
        else: 
            return redirect('/thank_you')
    else:
        current_question -= 1
        flash('Please answer the questions in order!')
        return redirect(f'/questions/{current_question}')   


@app.route("/answer/<int:num>", methods=["POST"])
def answer_response(num):
    user_choice = request.form.get('user_choice')
    responses.append(user_choice)
    return redirect(f'/questions/{num}')

@app.route("/thank_you")
def thank_you_page():
    global current_question
    if current_question >= len(questions):
        current_question = 1
        return render_template('thank_you.html')
    else:
        return redirect(f'/questions/{current_question}') 