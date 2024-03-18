from flask import Flask, Blueprint ,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb

# create Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key" 

# configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<@Oumaima55>'
app.config['MYSQL_DB'] = 'capstone_project'
mysql = MySQL(app)

# index
@app.route('/')
def home():
    return render_template('home.html')

# About us
@app.route('/about')
def about():
    return redirect(url_for('about'))

# login
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
                session['username'] = user[1] 
                return redirect(url_for('dashboard'))
            else:
                return render_template("error.html", error="Invalid username or password")

    return render_template('login.html')

# register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            conn = MySQLdb.connect(host='localhost', user='root', password='<@Oumaima55>', database='capstone_project')

            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for("login"))  #return to the login page after successful registration
            else:
                return render_template("error.html", error="Invalid username or email")
        except Exception as e:
            return render_template("error.html", error=str(e))

    return render_template('register.html')


# dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html", username=session['username'])
    else:
        return redirect(url_for('login'))

# logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# run the app
if __name__ == '__main__':
    app.run(debug=True)
