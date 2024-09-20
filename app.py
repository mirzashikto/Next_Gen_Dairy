from flask import Flask , render_template,redirect,request,flash,url_for,session
from flask_login import UserMixin, LoginManager,login_user,login_required,logout_user,current_user
from flask_sqlalchemy import SQLAlchemy
import datetime
import urllib.request
import os
from werkzeug.utils import secure_filename
import urllib.request

db = SQLAlchemy()
app=Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Next_Gen_Dairy.db"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db.init_app(app)
app.secret_key = 'Hello_Dairy'

class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(500), nullable=False)
    mobile = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)  
    address = db.Column(db.String(500), nullable=False)
    member_since=db.Column(db.String(500), nullable=False)
    logo=db.Column(db.String(500),nullable=True)
    slider_images=db.Column(db.String(2000),nullable=True)
    others=db.Column(db.String(2000),nullable=True)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(500), nullable=False)
    mobile = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    farm = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    images=db.Column(db.String(2000),nullable=True)
    
    def __repr__(self):
        return list(self.id,self.username,self.password,self.type,self.name,self.email,self.phone,self.house,self.street,self.area,self.country,self.zip,self.zip)
 

class Cows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cow_id=db.Column(db.String(500),nullable=False)
    purchase_date=db.Column(db.String(500),nullable=True)
    purchase_price=db.Column(db.String(500),nullable=True)
    purchase_age=db.Column(db.String(500),nullable=True)
    purchase_weight=db.Column(db.String(500),nullable=True)
    cow_color=db.Column(db.String(500),nullable=True)
    batch_id=db.Column(db.String(500),nullable=True)
    cow_type=db.Column(db.String(500),nullable=True)
    cow_sub_type=db.Column(db.String(500),nullable=True)
    cow_gender=db.Column(db.String(500),nullable=True)
    farm=db.Column(db.String(500),nullable=True)
    purchase_place=db.Column(db.String(500),nullable=True)
    vendor_contact_number=db.Column(db.String(500),nullable=True)
    paternal_history=db.Column(db.String(500),nullable=True)
    maternal_history=db.Column(db.String(500),nullable=True)
    deworming=db.Column(db.String(500),nullable=True)
    deworming_date=db.Column(db.String(500),nullable=True)
    vaccination=db.Column(db.String(500),nullable=True)
    vaccination_date=db.Column(db.String(500),nullable=True)
    estimate_weight=db.Column(db.String(500),nullable=True)
    expected_selling_price=db.Column(db.String(500),nullable=True)
    estimate_sale_date=db.Column(db.String(500),nullable=True)
    cow_status=db.Column(db.String(500),nullable=True)
    available_status=db.Column(db.String(500),nullable=True)
    publication_status=db.Column(db.String(500),nullable=True)
    video_link=db.Column(db.String(500),nullable=True)
    images=db.Column(db.String(2000),nullable=True)
    
    def __repr__(self):
        return self.cow_id

with app.app_context():
    db.create_all()

def list_to_str(lst):
    st=','.join(lst)
    return st
def str_to_list(st):
    lst=st.split(',')
    return lst

def checkLogged():
    if session.get('logged') is not None:
        return True
    else:
        return False


@app.route('/test', methods=['GET','POST'])
def test():
    if request.method=='GET':
        return render_template('temp.html')
    
    if request.method=="POST":
        pass






@app.route("/superadmin",methods=['GET','POST'])
def superadmin():
    if request.method=="GET":
        if session.get('logged') is not None and session.get('superadmin') is not None:
            data=Farm.query.all()
            return render_template("superadmin.html",data=data)

        else:
            return redirect('/')

    if request.method=="POST":
        pass

@app.route('/add_farm',methods=["GET",'POST'])
def add_farm():
    if request.method=="GET":
        return render_template('add_farm.html')
    if request.method=="POST":
        pass

@app.route('/farm_edit/<string:username>',methods=["GET","POST"])
def farm_edit(username):
    if request.method=="GET":
        data=Farm.query.filter_by(username=username).first()
        return render_template('farm_edit.html',data=data)
    if request.method=="POST":
        pass


@app.route('/farm_delete/<string:username>')
def farm_delete(username):
    farm=Farm.query.filter_by(username=username).first()
    farm_users=User.query.filter_by(farm=username)
    farm_cows=Cows.query.filter_by(farm=username)
    
    try:
        for farm_cow in farm_cows:
            db.session.delete(farm_cow)

        for farm_user in farm_users:
            db.session.delete(farm_user)

        db.session.delete(farm)

        db.session.commit()
        flash('Farm Delete Successful')

        return redirect('/superadmin')
    except:
        flash('Sorry. No permission to delete farm')
        return redirect('/superadmin')





@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    
    username =request.form.get('username') 
    password =request.form.get('password') 
    
    user_exists=User.query.filter_by(username=username).first()

    if user_exists and user_exists.password==password:
        session['logged']=username
        
        if user_exists.type=='Superadmin':
            session['superadmin']=username
            return redirect('/superadmin')
        else:
            flash('Login Successful', 'Success')
            return redirect("/")
    else:
        flash('Login failed. Try again', 'Success')
        return redirect("/")

@app.route('/logout',methods=['GET'])
def logout():
    if session.get('superadmin') is not None:
        session.pop('superadmin',None)
        
    session.pop('logged',None)
    return redirect("/")

@app.route("/register",methods=['GET','POST'])
def register():
    
    if request.method=="GET":
        return render_template('register.html')
    username =request.form.get('username') 
    password =request.form.get('password')
    re_enter_password=request.form.get('re_enter_password')
    if password!=re_enter_password:
        flash('Password does not match. Try again', 'Success')
        return redirect("/register")
    type = request.form.get('type')
    name =request.form.get('name') 
    email =request.form.get('email') 
    mobile=request.form.get('mobile')
    status="active"
    farm=request.form.get('farm')
    address=request.form.get('address')
    images="default_user.jpg"
    
    
    already_registered=User.query.filter_by(username=username).first()
    
    if not already_registered:
        user=User(username=username,password=password,mobile=mobile,status=status,type=type,name=name,email=email,farm=farm,address=address,images=images)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful. Please Login', 'Success')
        return render_template('login.html')
    else:
        flash('Already Registered', 'Success')
        return redirect("/")

@app.route("/public_portal",methods=["GET","POST"])
def public_portal():
    if request.method=="GET":
        data=Cows.query.all()
        return render_template('home.html',data=data)
    if request.method=="POST":
        pass

@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/")
def home():
    
    if session.get('logged') is not None:
        if session['logged']!=-1:

            return render_template("dashboard.html")

    else:
        return redirect('/login')
    
@app.route('/users',methods=["GET"])
def users():
    if request.method=="GET":
        data=User.query.all()

        return render_template("users.html",data=data)

@app.route('/add_user',methods=["GET",'POST'])
def add_user():
    if request.method=="GET":
        return render_template('add_user.html')
    if request.method=="POST":
        pass

@app.route('/user_profile',methods=["GET",'POST'])
def user_profile():
    if request.method=="GET":
        data=User.query.filter_by(username=session.get('logged')).first()
        return render_template("user_profile.html",data=data)
    if request.method=="POST":
        username=request.form.get('username')
        farm=request.form.get('farm')
        type=request.form.get('type')

        name =request.form.get('name') 
        email =request.form.get('email') 
        mobile=request.form.get('mobile')
        status=request.form.get('status')
        address=request.form.get('address')
        images=request.form.get('images')

        # images=request.form.get('images')
        user=User.query.filter_by(username=session.get('logged')).first()
        user.email=email
        user.name=name
        user.status=status
        user.mobile=mobile
        user.address=address
        user.images=images
        db.session.commit()
        flash('Update Successful')
        return redirect('/user_profile')




@app.route('/user_edit/<string:username>')
def user_edit(username):
    data=User.query.filter_by(username=username).first()
    return render_template("user_edit.html",data=data)

@app.route('/user_delete/<string:username>')
def user_delete(username):
    user=User.query.filter_by(username=username).first()
    if (user.username!=session.get('logged')):
        try:
            db.session.delete(user)
            db.session.commit()
            flash('User Delete Successful')

            return redirect('/users')
        except:
            flash('Sorry. No permission to delete user')
            return redirect('/users')
    else:
        flash('Sorry. No permission to delete user')
        return redirect('/users')




@app.route('/cows',methods=["GET","POST"])
def cows():
    
    
    if request.method=="GET":
        data=Cows.query.all()

        return render_template("cows.html",data=data)
    
@app.route('/addcow',methods=["GET",'POST'])
def addcow():
    if request.method=="GET":
        return render_template('addcow.html')
    if request.method=="POST":
        cow_id=request.form.get('cow_id')
        purchase_date=request.form.get('purchase_date')
        purchase_price=request.form.get('purchase_price')
        purchase_age=request.form.get('purchase_age')
        purchase_weight=request.form.get('purchase_weight')
        cow_color=request.form.get('cow_color')
        batch_id=request.form.get('batch_id')
        cow_type=request.form.get('cow_type')
        cow_sub_type=request.form.get('cow_sub_type')
        cow_gender=request.form.get('cow_gender')
        farm=request.form.get('farm')
        purchase_place=request.form.get('purchase_place')
        vendor_contact_number=request.form.get('vendor_contact_number')
        paternal_history=request.form.get('paternal_history')
        maternal_history=request.form.get('maternal_history')
        deworming=request.form.get('deworming')
        deworming_date=request.form.get('deworming_date')
        vaccination=request.form.get('vaccination')
        vaccination_date=request.form.get('vaccination_date')
        estimate_weight=request.form.get('estimate_weight')
        expected_selling_price=request.form.get('expected_selling_price')
        estimate_sale_date=request.form.get('estimate_sale_date')
        cow_status=request.form.get('cow_status')
        available_status=request.form.get('available_status')
        publication_status=request.form.get('publication_status')
        video_link=request.form.get('video_link')
        images=""
        already_registered=Cows.query.filter_by(cow_id=cow_id).first()
        #image saving
        if 'files[]' not in request.files:
                            
            images='default_cow.jpg'
        else:
            files = request.files.getlist('files[]')
            count=0
            filenames=[]
            for file in files:
                #sample name->  Cow_profile_6756_2.png
                filename = "Cow_profile_"+str(cow_id)+'_'+str(count)+'.'+file.filename.split('.')[-1]  
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
                count+=1    
            images = list_to_str(filenames)         
        
        
        if not already_registered:
            

            cow=Cows(cow_id=cow_id,purchase_date=purchase_date,purchase_price=purchase_price,purchase_age=purchase_age,purchase_weight=purchase_weight,cow_color=cow_color,batch_id=batch_id,cow_type=cow_type,cow_sub_type=cow_sub_type,cow_gender=cow_gender,farm=farm,purchase_place=purchase_place,vendor_contact_number=vendor_contact_number,paternal_history=paternal_history,maternal_history=maternal_history,deworming=deworming,deworming_date=deworming_date,vaccination=vaccination,vaccination_date=vaccination_date,estimate_weight=estimate_weight,expected_selling_price=expected_selling_price,estimate_sale_date=estimate_sale_date,cow_status=cow_status,available_status=available_status,publication_status=publication_status,video_link=video_link,images=images)
        
            db.session.add(cow)
            db.session.commit()

            # #extra add in database
            # for x in range (200):

            #     cow=Cows(cow_id=x,purchase_date=purchase_date,purchase_price=purchase_price,purchase_age=purchase_age,purchase_weight=purchase_weight,cow_color=cow_color,batch_id=batch_id,cow_type=cow_type,cow_sub_type=cow_sub_type,cow_gender=cow_gender,farm=farm,purchase_place=purchase_place,vendor_contact_number=vendor_contact_number,paternal_history=paternal_history,maternal_history=maternal_history,deworming=deworming,deworming_date=deworming_date,vaccination=vaccination,vaccination_date=vaccination_date,estimate_weight=estimate_weight,expected_selling_price=expected_selling_price,estimate_sale_date=estimate_sale_date,cow_status=cow_status,available_status=available_status,publication_status=publication_status,video_link=video_link,images=images)
            
            #     db.session.add(cow)
            #     db.session.commit()


            flash('Cow Successfully Added', 'Success')
            return redirect('/cows')
        else:
            flash('Cow Already Exist', 'Success')
            return redirect("/cows")
    

@app.route('/cow_edit/<string:cow_id>',methods=["GET",'POST'])
def cow_edit(cow_id):
    if request.method=="GET":
        data=Cows.query.filter_by(cow_id=cow_id).first()
        return render_template("cow_edit.html",data=data)
    if request.method=='POST':    
        cow=Cows.query.filter_by(cow_id=cow_id).first()

        cow.purchase_date=request.form.get('purchase_date')
        cow.purchase_price=request.form.get('purchase_price')
        cow.purchase_age=request.form.get('purchase_age')
        cow.purchase_weight=request.form.get('purchase_weight')
        cow.cow_color=request.form.get('cow_color')
        cow.batch_id=request.form.get('batch_id')
        cow.cow_type=request.form.get('cow_type')
        cow.cow_sub_type=request.form.get('cow_sub_type')
        cow.cow_gender=request.form.get('cow_gender')
        cow.farm=request.form.get('farm')
        cow.purchase_place=request.form.get('purchase_place')
        cow.vendor_contact_number=request.form.get('vendor_contact_number')
        cow.paternal_history=request.form.get('paternal_history')
        cow.maternal_history=request.form.get('maternal_history')
        cow.deworming=request.form.get('deworming')
        cow.deworming_date=request.form.get('deworming_date')
        cow.vaccination=request.form.get('vaccination')
        cow.vaccination_date=request.form.get('vaccination_date')
        cow.estimate_weight=request.form.get('estimate_weight')
        cow.expected_selling_price=request.form.get('expected_selling_price')
        cow.estimate_sale_date=request.form.get('estimate_sale_date')
        cow.cow_status=request.form.get('cow_status')
        cow.available_status=request.form.get('available_status')
        cow.publication_status=request.form.get('publication_status')
        cow.video_link=request.form.get('video_link')
        images=""
        already_registered=Cows.query.filter_by(cow_id=cow_id).first()
        #image saving
        if 'files[]' not in request.files:
                            
            images='default_cow.jpg'
        else:
            files = request.files.getlist('files[]')
            if files[0].filename.split('.')[-1]!="": #user kono file upload na korleo ekta file upload hoiche hisave count kore. oi jonno check kore nicchi je file name empty kina
                count=0
                filenames=[]
                for file in files:
                    #sample name->  Cow_profile_6756_2.png
                    filename = "Cow_profile_"+str(cow_id)+'_'+str(count)+'.'+file.filename.split('.')[-1]  
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filenames.append(filename)
                    count+=1    
                images = list_to_str(filenames)         
                cow.images=images
        
        db.session.commit()
        flash('Update Successful')
        return redirect('/cow_edit/'+cow_id)




@app.route('/cow_delete/<string:cow_id>')
def cow_delete(cow_id):
    cow=Cows.query.filter_by(cow_id=cow_id).first()

    try:
        db.session.delete(cow)
        db.session.commit()
        flash('Cow Delete Successful')

        return redirect('/cows')
    except:
        flash('Sorry. No permission to delete user')
        return redirect('/cows')
    
    
    
if __name__=="__main__":
    app.run(debug=True)
