from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
app.secret_key='I will do that later'

#MySQL configuration
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']='alx_flask_db'

mysql =MySQL(app)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message=''
    if  request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s)", (new_username, new_password, confirm_new_password, new_email))
        mysql.connection.commit()
        account = cur.fetchone()
        if account:
            message = 'Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', new_email): 
            message = 'Invalid email address !'
        elif new_password != confirm_new_password:
            message = 'Passwords do not match!'
        elif not new_username or not new_password or not confirm_new_password or not new_email:
            message= 'Please fill out the form '
        else:
            cur.execute('INSERT INTO user VALUES(NULL,% s, % s, % s, % s)',(new_username, new_email, new_password, confirm_new_password))
            mysql.connection.commit()
            message = 'You have successfully registered!' 
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message= message)
        

if __name__ == '__main__':
    app.run(debug=True)

