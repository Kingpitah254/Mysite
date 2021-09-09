from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,current_user,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database1'
app.config['SECRET_KEY']='secret_key1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=False)
    email = db.Column(db.String(40),unique=True,nullable=False)
    password = db.Column(db.String(200),primary_key=False,unique=False,nullable=False)
    
    def __repr__(self,username,email):
        self.username=username
        self.email=email
        

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        password1=request.form['password1']
        
        #cheking_checking_if_the_detail_are_right.
        new_user=User.query.filter_by(email=email,username=username).first()
        if new_user:
            flash('User already exist',category='success') 
        elif len(username)< 2:
            flash('Username must have more than 1 character!!',category='error')           
        elif len(email)< 4:
            flash('Email must have more than 3 character!!',category='error')   
        elif len(password)< 4:
            flash('Password must have more than 3 character!!',category='error')
        elif password1 != password:
            flash('Password does not match!!',category='error')
        else:
            new_user=User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully')
            return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/users')
def show_user():
    users = User.query.all()
    return render_template('show_user.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
