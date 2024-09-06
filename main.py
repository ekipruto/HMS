from flask import Flask, render_template,request,session,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin, login_user, logout_user, login_manager, LoginManager
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash, hashlib

app = Flask(__name__)
app.secret_key = 'ekiprutobii'

#This is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hms'
db = SQLAlchemy(app)

# Model definitions
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))  # Fixed typo here

# Endpoints
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            print("Email Already Exists")
            return render_template('login.html')

        encpassword = generate_password_hash(password)
        
        new_user = Users(username=username, email=email, password=encpassword)
        try:
            db.session.add(new_user)
            db.session.commit()
            print("User added successfully")
            return render_template('login.html')
        except Exception as e:
            print(f"Error adding user: {str(e)}")
            db.session.rollback()
            return "An error occurred while signing up"
        

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if not password:
            print("No password provided")
            return "Please provide a password"

        user = Users.query.filter_by(email=email).first()
        
        if not user or not user.password:
            print("Invalid email or no password in database")
            return "Invalid credentials"

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            print("Invalid Credentials")
            return render_template('login.html')

    return render_template('login.html')


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == "POST": 

#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = Users.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             return redirect(url_for(''))
        
#         else:
#             print("Invalid Credentials")
#             return render_template('login.html')

#     return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('login.html')

# @app.route('/kazi')
# def kazi():
#     try:
#         Test.query.all()
#         return 'Db Connected Successfully'
#     except:
#         return 'Db not connected'

@app.route('/doctors')
def doctors():
    return render_template ('doctors.html')

@app.route('/patients')
def patients():
    return render_template ('patients.html')

@app.route('/bookings')
def bookings():
    return render_template ('bookings.html')

if __name__ == '__main__':
 app.run(debug=True)
