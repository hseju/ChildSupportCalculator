from email.policy import default
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///respondents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initializat the database
db = SQLAlchemy(app)

#create a database model
class Respondents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string
    def __repr__(self):
        return f"Respondents('{self.email}')"



@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/thanks", methods=['GET', 'POST'])
def thanks():
    
        emails = Respondents.query.all()
        print(emails)
        return render_template("thanks.html", emails=emails)

@app.route("/data", methods= ['GET','POST'])
def get_data():
    emails = Respondents.query.all()
    return render_template("data.html", emails= emails)


@app.route("/form", methods=['GET', 'POST'])
def form():
    email = request.form.get("email") 

    if not email:
        error = "Please enter email"
        return render_template("home.html", error=error)

    if request.method == "POST":
        email_entered = request.form['email']
        new_entry = Respondents(email=email_entered)

        #push to database
        try:
            db.session.add(new_entry)
            db.session.commit()
            return render_template("thanks.html")
        except:
            return  "There was an error adding the email."

    return render_template("thanks.html")



print(Respondents.date_created)

if __name__ == "__main__":
    app.run()

