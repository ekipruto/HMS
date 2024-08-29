from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


#my db connection
local_server=True
app=Flask(__name__)
app.secret_key='ekiprutobii'

#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hms'
#pymysql.install_as_MySQLdb()
db=SQLAlchemy(app)

#create db models/tables
class Test(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

#End points and functions

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/doctors')
def doctors():
    return render_template ('doctors.html')

@app.route('/patients')
def patients():
    return render_template ('patients.html')

@app.route('/bookings')
def bookings():
    return render_template ('bookings.html')

@app.route('/signup')
def signup():
    return render_template ('signup.html')

@app.route('/login')
def login():
    return render_template ('login.html')

@app.route('/logout')
def logout():
    return render_template ('login.html')


@app.route('/kazi')
def kazi():
    try:
         Test.query.all()
         return 'Db Connected Successfully'
    except:
         return 'Db not connected'
    

app.run(debug=True)