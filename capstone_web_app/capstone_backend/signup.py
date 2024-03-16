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
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username,new_password))
    mysql.connection.commit()
    cur.close()
    # Add your sign up logic here
    return f'Sign up attempt with username: {new_username} and password: {new_password}'

if __name__ == '__main__':
    app.run(debug=True)

