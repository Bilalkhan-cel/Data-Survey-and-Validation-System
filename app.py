import os
from flask import Flask, render_template , request ,url_for , session ,redirect

from flask_sqlalchemy import SQLAlchemy
from Data_extraction_XML import extract_columns , extract_questions_ans_value
# bad ka task ke question categoty bhi print karnani he form pe
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'testing123de'
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

    if request.method == "POST":
        answer = request.form.get("answer")

        answers = session["answers"]
        answers.append(answer)
        session["answers"] = answers

        session["index"] += 1

    if session["index"] >= len(questions):
        if session.get("survey_completed"):
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