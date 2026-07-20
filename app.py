import os
from flask import Flask, render_template, request, url_for, session, redirect
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from Data_extraction_XML import extract_columns, extract_questions_ans_value , extract_images

# bad ka task ke question categoty bhi print karnani he form pe
load_dotenv()
app = Flask(__name__)

database_url = os.getenv('DATABASE_URL')
# # SQLAlchemy 1.4+ requires "postgresql://", but many hosts still hand you
# # "postgres://" in the env var. Normalize it so this doesn't blow up at runtime.
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] =database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SESSION_SECRET_KEY")
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

db = SQLAlchemy(app)

cols = extract_columns("data.xml")
question = extract_questions_ans_value("data.xml")
questions = list(question.items())
images=extract_images("data.xml")


class survey_data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_bad = db.Column(db.Integer, default=0)


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



with app.app_context():
    init_db()


@app.after_request
def allow_iframe(response):
    response.headers.pop("X-Frame-Options", None)
    response.headers["Content-Security-Policy"] = "frame-ancestors *;"
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html", question_length=len(cols))


@app.route('/survey', methods=['GET', 'POST'])
def survey():

    if "index" not in session:
        session["index"] = 0
        session["answers"] = []

    if "fast_ans" not in session:
        session["fast_ans"] = 0

    if request.method == "POST":
        col_id=cols[session["index"]]
        img=images.get(col_id)
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

        fast_answer = session["fast_ans"]
        survey_answers = session['answers']
        data = {}
        for col, ans in zip(cols, survey_answers):
            data[col] = ans

        survey = survey_data(
            is_bad=1 if fast_answer > len(questions) / 2 else 0,
            **data,
        )
        db.session.add(survey)
        db.session.commit()
        session["survey_completed"] = True

        return render_template("thanks.html")

    question, options = questions[session["index"]]

    return render_template(
        "survey.html",
        question=question,
        options=options,
        img=img,
        col_id=col_id,
        last_question=session["index"] == len(questions) - 1
    )


if __name__ == "__main__":
    # Only used for local development — on Vercel this block never runs;
    # the `app` object above is imported directly by the serverless runtime.
    app.run()