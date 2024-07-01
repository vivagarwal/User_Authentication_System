from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_mail import Mail, Message
import random
import string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "secret_key"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ash781391@gmail.com'
app.config['MAIL_PASSWORD'] = 'usxy nhsq mfgi bnmc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
posta = Mail(app)
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250))
	password = db.Column(db.String(250))
	email = db.Column(db.String(250))
	hashCode = db.Column(db.String(250))

db.init_app(app)

with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
	return User.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = User(username=request.form.get("username"),
					password=request.form.get("password"),email=request.form.get("email"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = User.query.filter_by(
			username=request.form.get("username")).first()
		if user.password == request.form.get("password"):
			login_user(user)
			return redirect(url_for("home"))
	return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/")
def home():
	return render_template("home.html")

@app.route('/forgot-password',methods=["POST","GET"])
def forgot_password():
    if request.method=="POST":
        mail = request.form['mail']
        check = User.query.filter_by(email=mail).first()

        if check:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'ash', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            posta.send(msg)
            return render_template("login.html")
        else:
            return '''
            <form action="/forgot-password" method="post">
                <small>enter the email address of the account you forgot your password</small> <br>
                <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                <input type="submit" value="Submit">
            </form>
        '''
    else:
        return '''
        <form action="/forgot-password" method="post">
            <small>enter the email address of the account you forgot your password</small> <br>
            <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
            <input type="submit" value="Submit">
        </form>
    '''    


@app.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash('yanlış girdin')
                return '''
                    <form method="post">
                        <small>enter your new password</small> <br>
                        <input type="password" name="passw" id="passw" placeholder="password"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                        <input type="submit" value="Submit">
                    </form>
                '''
        else:
            return '''
                <form method="post">
                    <small>enter your new password</small> <br>
                    <input type="password" name="passw" id="passw" placeholder="password"> <br>
                    <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return render_template('/')

	
if __name__ == "__main__":
    app.run()
