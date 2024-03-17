# import necessary modules
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb

# create Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # set a secret key for session management

# configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<@Oumaima55>'
app.config['MYSQL_DB'] = 'capstone_project'
mysql = MySQL(app)

# login route 
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = MySQLdb.connect(host='localhost', user='root', password='<@Oumaima55>', database='capstone_project')

        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user and user[3] == password:
                session['username'] = user[1]  # Assuming username is the second column in the table
                return redirect(url_for('dashboard'))
            else:
                return render_template("error.html", error="Invalid username or password")

    return render_template('login.html')

# dashboard route (example of a protected route)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html", username=session['username'])
    else:
        return redirect(url_for('login'))

# logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# D'ont have account 
@app.route('/register')
def register():
    return render_template('register.html')

# run the app
if __name__ == '__main__':
    app.run(debug=True)
