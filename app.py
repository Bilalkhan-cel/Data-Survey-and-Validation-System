import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from Data_extraction_XML import extract_columns

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

cols = extract_columns("data.xml")


class survey_data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)



for col in cols:
    setattr(
        survey_data,
        col,
        db.Column(db.String(20), nullable=False)
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


if __name__ == "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)