from flask import Flask , render_template,redirect,request,flash,url_for,session
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Dental_Care.db"

db.init_app(app)
app.secret_key = 'Hello_Dental'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(500), nullable=False)
    house = db.Column(db.String(500), nullable=False)
    street = db.Column(db.String(500), nullable=False)
    area = db.Column(db.String(500), nullable=False)
    country = db.Column(db.String(500), nullable=False)
    zip = db.Column(db.String(500), nullable=False)
    dob = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return list(self.id,self.username,self.password,self.type,self.name,self.email,self.phone,self.house,self.street,self.area,self.country,self.zip,self.zip)


class BookedSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(500), nullable=False)
    reference = db.Column(db.String(500), nullable=False)
    
    
    def __repr__(self):
        return self.id,self.username, self.date,self.time,self.reference

with app.app_context():
    db.create_all()




@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/login',methods=['POST'])
def login():
    username =request.form.get('username') 
    password =request.form.get('password') 

    user_exists=User.query.filter_by(username=username).first()

    if user_exists and user_exists.password==password:
        session['logged']=username
        flash('Login Successful', 'Success')
        return redirect("/")
    else:
        flash('Login failed. Try again', 'Success')
        return redirect("/")

@app.route('/logout',methods=['GET'])
def logout():
    session['logged']=-1
    return redirect("/")

@app.route("/register",methods=['POST'])
def register():
     
    username =request.form.get('username') 
    password =request.form.get('password') 
    type ='0'
    name =request.form.get('name') 
    email =request.form.get('email') 
    phone =request.form.get('phone') 
    house =request.form.get('house') 
    street =request.form.get('street') 
    area =request.form.get('area') 
    country =request.form.get('country') 
    zip =request.form.get('zip') 
    dob =request.form.get('dob') 
    
    already_registered=User.query.filter_by(username=username).first()
    
    if not already_registered:
        user=User(username=username,password=password,type=type,name=name,email=email,phone=phone,house=house,street=street,area=area,country=country,zip=zip,dob=dob)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful', 'Success')
        return redirect("/")
    else:
        flash('Already Registered', 'Success')
        return redirect("/")

@app.route("/main")
def main():
    return render_template("main.html")
@app.route("/")
def home():
    return render_template("home.html")


if __name__=="__main__":
    app.run(debug=True)
