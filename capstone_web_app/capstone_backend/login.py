from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

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
    return render_template('login.html')

@app.route('/login', methods=['GET' ,'POST'])
def login():
    message = ''
    if  request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        if user:
            session['login']= True
            session['userid']= user ['userid']
            session['name']= user ['name']
            session['email']= user ['email']
            message= 'Logged is successfully'
            return render_template('app.html', message = message)
        else:
            message = 'Invalid email or password! Please try again'
    return render_template(login.html, message= message)



if __name__ == '__main__':
    app.run(debug=True)
