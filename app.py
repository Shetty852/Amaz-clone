from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/ROHAN SHETTY/Desktop/Amaz-clone/instance/User.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)


def create_db():
    with app.app_context():
        db.create_all()

create_db()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign')
def sign():
    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.password == hashlib.md5(password.encode()).hexdigest()[:10]:  
        return redirect(url_for('index'))
    else:
        return "Invalid email or password. Please try again."
    

if __name__ == '__main__':
    app.run(debug=True)