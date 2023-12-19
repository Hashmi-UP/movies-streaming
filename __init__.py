import json
import os
import re
from threading import active_count
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, url_for, flash
from werkzeug.utils import redirect, secure_filename
from flask_mail import Mail, Message
from flask_paginate import Pagination, get_page_parameter
from datetime import date, timedelta





local_server = True

app = Flask(__name__)
app.secret_key = "haideraamir"
app.config['POSTER_UPLOAD'] = "static\\poster"
app.config['MOVIE_UPLOAD'] = "static\\movies"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'mkv', 'mpg', 'mov'])
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "haideraamir07@gmail.com"
app.config['MAIL_PASSWORD'] = "haider072021"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)





#database connection with xampp
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://haider:haider0007@localhost/database"
db = SQLAlchemy(app)



class Movies(db.Model):

    # Sno, Name, Age, Email, Address, Post, Phone, Photo

    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    genre = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String(3000), unique=False, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)
    duration = db.Column(db.String(120), unique=False, nullable=False)
    languages = db.Column(db.String(120), unique=False, nullable=False)
    poster = db.Column(db.String(length=5056), unique=False, nullable=False)
    movie = db.Column(db.String(length=5056), unique=False, nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.genre} - {self.description} - {self.date} - {self.duration} - {self.languages} - {self.poster} - {self.movie}"


class Users(db.Model):

    # Sno, Name, Age, Email, Address, Post, Phone, Photo

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    first_name = db.Column(db.String(3000), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    start_date = db.Column(db.String(120), unique=False, nullable=False)
    end_date = db.Column(db.String(120), unique=False, nullable=False)
    package = db.Column(db.String(length=5056), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name} - {self.email} - {self.first_name} - {self.last_name} - {self.password} - {self.package} - {self.start_date} - {self.end_date} "


class Regusers(db.Model):

    # Sno, Name, Age, Email, Address, Post, Phone, Photo

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    first_name = db.Column(db.String(3000), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    package = db.Column(db.String(length=5056), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name} - {self.email} - {self.first_name} - {self.last_name} - {self.password} - {self.package}"



class Likes(db.Model):

    # Sno, Name, Age, Email, Address, Post, Phone, Photo

    no = db.Column(db.Integer, primary_key=True, nullable=False)
    moviesno = db.Column(db.String(120), unique=False, nullable=False)
    moviename = db.Column(db.String(100), unique=False, nullable=False)
    usersno = db.Column(db.String(200), unique=False, nullable=False)
    username = db.Column(db.String(3000), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"{self.no} - {self.moviesno} - {self.moviename} - {self.username} - {self.usersno}"




#app route for user index
@app.route('/', methods = ['POST', 'GET'])
def index():

    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.paginate(page=page, per_page = 15)
        return render_template('index.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        
        if record:
            session['loggedin'] = True
            session['username'] = username
            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.paginate(page=page, per_page = 15)
            return render_template('index.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)


#app route for user registaration
@app.route('/register', methods = ['POST', 'GET'])
def registration():
    if (request.method == "POST"):
        details = request.form
        username = details['user_login']
        firstname = details['first_name']
        lastname = details['last_name']
        email1 = details['user_email']
        password1 = details['pass1']
        password2 = details['pass2']
        subplan = details['subscription_plans']

        #for username
        recordname = Users.query.filter_by(name = username).first()
    
        #for email id
        recordemail = Users.query.filter_by(email = email1).first()

        if recordname:
            flash("This username and email is already in user!", "danger")

        elif recordemail:
            flash("Email is already registerd!", "danger")
            
        else:
            if(password1==password2):
                msg = Message('Welcome to MovieVerse', sender = "haideraamir07@gmail.com", recipients = [email1])
                msg.body = username + '"We welcome you to join our community. You can stream Movies with good quailty at minimum price."'
                msg.html = "<b> Hey"+ username+"</b><br><p>We welcome you to join our community</p><br><p>Now you have to pay "+subplan+" with you jazz cash acccount at this account number and email the recipt at this email address bilaljanbaz@gmail.com </p><br><a href='http://127.0.0.1:19000/forget'>Foget Password</a><br>If that was not you ignore this emial.<br><br><b>MoviesVerse</b>"
                mail.send(msg)
                flash("The mail is successfully send", "success")
                datainsert = Regusers(name=username, email=email1, first_name = firstname, last_name=lastname, password=password2, package=subplan)
                db.session.add(datainsert)
                db.session.commit()
                return redirect('/')

            else:
                flash ("password is not matched", "danger")

    return render_template('register.html')



#app route for user logout and admin logout
@app.route("/logout")
def logout():
    session.pop('username')
    return redirect('/')


#app route for user logout and admin logout
@app.route("/logoutadmin")
def logout1():
    session.pop('user')
    return redirect('/')

#app route for uploading movies only allow for admin
@app.route("/uploadmovie", methods = ['GET', 'POST'])
def uploadmovie():
    if ('user' in session and session['user'] == "admin"):
    
        if request.method == 'POST':
            details = request.form
            moviename = details['moviename']
            genre1 = details['genre']
            description1 = details['description']
            mdate = details['mdate']
            duration1 = details['duration']
            languages1 = details['languages']
        
            m_poster = request.files['poster']
            m_poster.filename = moviename + '.png'
            p_filename = secure_filename(m_poster.filename)
            p = p_filename 

            m_file = request.files['moviefile']
            m_file.filename = moviename + '.mp4'
            m_filename = secure_filename(m_file.filename)
            m = m_filename 

            #user session register
            session['user'] = "admin"
            session['password'] = "abc123"
                
            m_poster.save(os.path.join(app.config['POSTER_UPLOAD'], secure_filename(m_poster.filename)))
            m_file.save(os.path.join(app.config['MOVIE_UPLOAD'], secure_filename(m_file.filename)))
                

            datamovie = Movies(name=moviename, genre=genre1, description=description1, date=mdate, poster=p, movie=m, duration=duration1, languages=languages1)
            db.session.add(datamovie)
            db.session.commit()
            flash ("secsussfully uploaded", "success")
            
        return render_template("upload-video.html")

    return redirect('/admin-index')



#app route for watching movie for user
@app.route("/watch/<string:id>", methods = ['GET', 'POST'])
def watch(id):

    if 'username' in session:
        username = session['username']

        
        recordmovie = Movies.query.filter_by(sno=id).first()

        #movies = Movies.query.filter(Movies.genre == recordmovie.genre).all()
        page = request.args.get('page', 1, type=int)
        movies = Movies.query.filter(Movies.genre == recordmovie.genre).paginate(page=page, per_page = 5)
   
        filename = Movies.query.filter(Movies.movie == recordmovie.movie).first()

        #listToStr = ' '.join([str(elem) for elem in filename])
    return render_template("video-page.html", recordmovie=recordmovie, movies=movies, username=username, code=301)
    


#app route for admin index
@app.route("/admin-index", methods=['POST', 'GET'])
def userindex():

    if ('user' in session and session['user'] == "admin"):
        #count query will be executed
        userdata = Users.query.all()
        session['user'] = "admin"
        session['password'] = "abc123"
        return render_template('admin-index.html', userdata=userdata)

    if request.method=='POST':
        details = request.form
        username = details['uname']
        userpass = details['password']
        if(username == "admin" and userpass == "abc123"):
            session['user'] = username
            session['password'] = userpass
            userdata = Users.query.all()
            return render_template('admin-index.html', userdata=userdata)
        else:
            flash("Incorrect Username or Password", "danger")
    return render_template('admin-login.html',)



#app route for admin to see data of user
@app.route("/admin-regusers", methods=['POST', 'GET'])
def adminreguser():

    if ('user' in session and session['user'] =="admin"):
        session['user'] = "admin"
        session['password'] = "abc123"
        userdata = Regusers.query.all()
        return render_template('admin-regusers.html', userdata=userdata)

    if request.method=='POST':
        details = request.form
        username = details['uname']
        userpass = details['password']

        if(username == "admin" and userpass == "abc123"):
            session['user'] = username
            session['password'] = userpass
            userdata = Regusers.query.all()
            return render_template('admin-regusers.html', userdata=userdata)

        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('admin-login.html',)



#app route for admin to see data of user
@app.route("/admin-users", methods=['POST', 'GET'])
def adminuser():

    if ('user' in session and session['user'] == "admin"):
        session['user'] = "admin"
        session['password'] = "abc123"
        userdata = Users.query.all()
        return render_template('admin-users.html', userdata=userdata)

    if request.method=='POST':
        details = request.form
        username = details['uname']
        userpass = details['password']

        if(username =="admin" and userpass == "abc123"):
            session['user'] = username
            session['password'] = userpass
            userdata = Users.query.all()
            return render_template('admin-users.html', userdata=userdata)

        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('admin-login.html',)




#app route for admin to see movie data
@app.route("/admin-movies", methods=['POST', 'GET'])
def adminmovies():

    if ('user' in session and session['user'] == "admin"):
        
        
        moviesdata = Movies.query.all()
        session['user'] = "admin"
        session['password'] = "abc123"
        return render_template('admin-movies.html', moviesdata=moviesdata)

    if request.method=='POST':
        details = request.form
        username = details['uname']
        userpass = details['password']

        if(username == "admin" and userpass == "abc123"):
            
            moviesdata = Movies.query.all()
            session['user'] = username
            session['password'] = userpass
            return render_template('admin-movies.html', moviesdata=moviesdata)

        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('admin-login.html',)



#app route for delete movie data
@app.route("/delete/<string:sno>", methods = ['GET', 'POST'])
def delete(sno):

    if ('user' in session and session['user'] == "admin"):

        username = session['user']
        userpass = session['password']

        deletedata = Movies.query.filter_by(sno=sno).first()

        poster = deletedata.poster 
        poster = secure_filename(poster)
        os.remove(os.path.join(app.config['POSTER_UPLOAD'], poster))
        
        mfile = deletedata.movie 
        mfile = secure_filename(mfile)
        os.remove(os.path.join(app.config['MOVIE_UPLOAD'], mfile))

        db.session.delete(deletedata)
        db.session.commit()
        flash("Record is deleted", "success")

    else:
        return ("Some files are missing")

    return redirect('/admin-movies')



#app route for like page of user liked videos
@app.route("/like/<string:sno>", methods = ['GET', 'POST'])
def like(sno):

    if 'username' in session:
        username = session['username']

        
        data = Movies.query.filter_by(sno=sno).first()

        
        data2 = Users.query.filter_by(name=username).first()

        
        datainsert = Likes(moviesno=sno, moviename=data.name, usersno=data2.id, username=username)
        db.session.add(datainsert)
        db.session.commit()

    return redirect("/")



#app route for delete data of users by admin
@app.route("/delete1/<string:sno>", methods = ['GET', 'POST'])
def delete1(sno):
    if ('user' in session and session['user'] == "admin"):

        deldata = Users.query.filter_by(id=sno).first()
        db.session.delete(deldata)
        db.session.commit()
        
        flash("The record is deleted succesfully", "success")
    return redirect('/admin-users')




@app.route("/horror", methods = ['GET', 'POST'])
def horror():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="horror").paginate(page=page, per_page = 15)
        return render_template('horror.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="horror").paginate(page=page, per_page = 15)
            return render_template('horror.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)



@app.route("/comedy", methods = ['GET', 'POST'])
def comedy():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="comedy").paginate(page=page, per_page = 15)
        return render_template('comedy.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="comedy").paginate(page=page, per_page = 15)
            return render_template('comedy.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)



@app.route("/action", methods = ['GET', 'POST'])
def action():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="action").paginate(page=page, per_page = 15)
        return render_template('action.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="action").paginate(page=page, per_page = 15)
            return render_template('action.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)




@app.route("/scifi", methods = ['GET', 'POST'])
def scifi():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="scifi").paginate(page=page, per_page = 15)
        return render_template('scifi.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="scifi").paginate(page=page, per_page = 15)
            return render_template('scifi.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)



@app.route("/romantic", methods = ['GET', 'POST'])
def romantic():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="romantic").paginate(page=page, per_page = 15)
        return render_template('romantic.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="romantic").paginate(page=page, per_page = 15)
            return render_template('romantic.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)



@app.route("/drama", methods = ['GET', 'POST'])
def drama():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="drama").paginate(page=page, per_page = 15)
        return render_template('drama.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="drama").paginate(page=page, per_page = 15)
            return render_template('drama.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)



@app.route("/animated", methods = ['GET', 'POST'])
def animated():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="animated").paginate(page=page, per_page = 15)
        return render_template('animated.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="animated").paginate(page=page, per_page = 15)
            return render_template('animated.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)



@app.route("/thriller", methods = ['GET', 'POST'])
def thriller():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(genre="thriller").paginate(page=page, per_page = 15)
        return render_template('thriller.html', recordmovie=recordmovie, username=username)

    if request.method == 'POST':
        username = request.form['log']
        userpass = request.form['pwd']
        record = Users.query.filter_by(name=username).first()
        
        if record.name==username and record.password==userpass:
            session['loggedin'] = True
            session['username'] = record[1]

            page = request.args.get('page', 1, type=int)
            recordmovie = Movies.query.filter_by(genre="thriller").paginate(page=page, per_page = 15)
            return render_template('thriller.html', recordmovie=recordmovie, username=username)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('log-in.html',)




@app.route("/recoverpassword", methods = ['GET', 'POST'])
def recover():
    if request.method == 'POST':
        emailid = request.form['pms_username_email']
        data = Users.query.filter_by(email=emailid).first()

        if data:
             msg = Message('Recover Password', sender = "haideraamir07@gmail.com", recipients = [data.email])
             msg.body = data.name + '"This email is about to reset your password. click on the following link to reset."+ /index+"if you are not want to change just ignore this email"'
             msg.html = "<b> Hey "+ data.name + "</b><br><p>We recieved a request from you to reset your password.</p><br><p>If you want to reset your password click on the following link. </p><br><a href='http://127.0.0.1:19000/forget'>Foget Password</a><br>If that was not you ignore this emial.<br><br><b>MoviesVerse</b>"
             mail.send(msg)
             flash("The mail is successfully send", "success")
        else:
            flash("The mail cannot send by some reason", "warning")
    return render_template("recover-password.html")



@app.route("/forget", methods = ['GET', 'POST'])
def forget():
    if request.method == 'POST':
        emailid = request.form['emailid']
        newpass = request.form['newpass']
        confirmpass = request.form['confirmpass']

        data = Users.query.filter_by(email=emailid).first()

        if data:
            if newpass == confirmpass:
                
                data.password = confirmpass
                db.session.commit()
                flash("The password successfuly reset", "success")
            else:
                flash("The password and confirm password is not matching", "warning")
        else:
            flash("The email with this address is not present in database")
    return render_template("forget.html")



@app.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        searchname = request.form['searchname']

        page = request.args.get('page', 1, type=int)
        recordmovie = Movies.query.filter_by(name=searchname).paginate(page=page, per_page = 15)
        return render_template('search.html', recordmovie=recordmovie)

    return render_template("index.html")


@app.route("/reguser/<string:id>", methods = ['GET', 'POST'])
def regusers(id):
    if ('user' in session and session['user'] == "admin"):
        reg = Regusers.query.filter_by(id=id).first()
        checkdata = Users.query.filter_by(email=reg.email).first()

        if checkdata:
            flash("The email is already in used", "warning")
        else:
            startdate = date.today()
            enddate = (date.today()+timedelta(days=30)).isoformat() 
            datainsert = Users(name=reg.name, email=reg.email, first_name=reg.first_name, last_name=reg.last_name, password=reg.password, package=reg.package, start_date=startdate, end_date=enddate)
            db.session.add(datainsert)
            db.session.commit()
            db.session.delete(reg)
            db.session.commit()
            msg = Message('MoviesVerse', sender = "haideraamir07@gmail.com", recipients = [reg.email])
            msg.html = "<b> Hey"+ reg.name +"</b><br><p>We welcome you to join our community</p><br><p>The request of MoviesVerse is allowed. You can now use your account to access the website</p><br><a href='http://127.0.0.1:19000/'>MoviesVerse</a><br>Regards<br><b>MoviesVerse</b>"
            mail.send(msg)
            flash("The record is added succesfully", "success")
    return redirect('/admin-regusers')



@app.route("/deleteexpire", methods = ['GET', 'POST'])
def deleteexpire():
    if ('user' in session and session['user'] == "admin"):
        current_date = date.today()
        Users.query.filter_by(end_date=current_date).delete()
        
        #db.session.delete(deldata)
        db.session.commit()
        flash("The record is deleted succesfully", "success")
    return redirect('/admin-users')

@app.route("/sendendmail", methods=['GET', 'POST'])
def sendendmail():
    if ('user' in session and session['user'] == "admin"):
        current_date = date.today()
        datamail = Users.query.filter_by(end_date=current_date).all()
        for users in datamail:
            msg = Message('MoviesVerse', sender = "haideraamir07@gmail.com", recipients = [users.email])
            msg.html = "<b> Hey"+ users.name +"</b><br><p>Dear User!</p><br><p>Your account is going to expire today. Thanks for your subscription. For again subscribe register yourself again.</p><br><a href='http://127.0.0.1:19000/'>MoviesVerse</a><br>Regards<br><b>MoviesVerse</b>"
            mail.send(msg)
        #db.session.delete(deldata)
        
        flash("The mails send succesfully", "success")
    return redirect('/admin-users')


@app.route("/myliked")
def myliked():
     if 'username' in session:
        username = session['username']

        
        data = Movies.query.filter_by(sno=sno).first()

        
        data2 = Users.query.filter_by(name=username).first()

        
        datainsert = Likes(moviesno=sno, moviename=data.name, usersno=data2.id, username=username)
        db.session.add(datainsert)
        db.session.commit()

        return redirect("/")




    
