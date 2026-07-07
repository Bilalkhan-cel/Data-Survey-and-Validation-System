import os
from flask import Flask, render_template , request ,url_for , session ,redirect
from dotenv import load_dotenv
import os

from flask_sqlalchemy import SQLAlchemy
from Data_extraction_XML import extract_columns , extract_questions_ans_value
# bad ka task ke question categoty bhi print karnani he form pe
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = os.getenv("SESSION_SECRET_KEY")
db = SQLAlchemy(app)


cols = extract_columns("data.xml")
question=extract_questions_ans_value("data.xml")
questions = list(question.items())


class survey_data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)



for col in cols:
    setattr(
        survey_data,
        col,
        db.Column(db.String(250), nullable=False)
    )

def init_db():
    try:
        db.create_all()
        print("DB initialized")
    except Exception as e:
        print("DB error:", e)
        raise  


@app.route('/', methods=['GET', 'POST'])
def home():
   
        
     return render_template("index.html",question_length=len(cols))


@app.route('/survey',methods=['GET','POST'])
def survey():

    if "index" not in session:
       session["index"] = 0
       session["answers"] = []
    
    if "fast_ans" not in session:
        session["fast_ans"]=0
        
    if request.method == "POST":
        answer = request.form.get("answer")
        response_time = float(request.form["response_time"])

        answers = session["answers"]
        answers.append(answer)
        session["answers"] = answers
        if response_time <= 3:
          session["fast_ans"] += 1

        session["index"] += 1

    if session["index"] >= len(questions):
        if session.get("survey_completed"):
            return render_template("thanks.html")
        
        fast_answer=session["fast_ans"]
        if fast_answer > len(questions)/2:
            print(fast_answer)
            return render_template("thanks.html")
            
        
        print(session["answers"]) 
        survey_answers=session['answers']
        data={}
        for col, ans in zip(cols, survey_answers):
           data[col] = ans

        survey = survey_data(**data)
        db.session.add(survey)
        db.session.commit()
        session["survey_completed"]=True
        
        return render_template("thanks.html")
    

    question, options = questions[session["index"]]

    return render_template(
        "survey.html",
        question=question,
        options=options,
        last_question=session["index"] == len(questions)-1
    )

    
if __name__ == "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)