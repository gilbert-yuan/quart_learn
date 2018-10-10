from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, eamil):
        self.username = username
        self.email = eamil

    def __repr__(self):
        return '<p>%r' % self.username


@app.route('/adduser')
def add_user():
    user1 = User('ethan', 'ethan@example.com')
    user2 = User('admin', 'admin@example.com')
    user3 = User('guest', 'guest@example.com')
    user4 = User('joe', 'joe@example.com')
    user5 = User('michael', 'michael@example.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.commit()
    return "<p>add succssfully!"

@app.route('/delete/user/<name>')
def delete_user_name(name):
    admin = User.query.filter_by(username=name).first()
    db.session.delete(admin)
    db.session.commit()


@app.route('/getalluser')
def get_all_user():
    users = User.query.all()
    print(users)
    return '---'.join([user.username for user in users])


@app.route('/getuser/<name>')
def get_user_by_name(name):
    user = User.query.filter_by(username=name).first()
    return user.email


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)














