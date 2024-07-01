from flask import Flask 
from flask_bcrypt import Bcrypt 
  
app = Flask(__name__) 
bcrypt = Bcrypt(app) 
  
@app.route('/') 
def index(): 
    password = 'password'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
    is_valid = bcrypt.check_password_hash(hashed_password, password) 
    return f"Password: {password}<br>Hashed Password:  
                          {hashed_password}<br>Is Valid: {is_valid}" 
  
if __name__ == '__main__': 
    app.run() 