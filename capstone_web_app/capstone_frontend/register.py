from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'      
app.config['MYSQL_PASSWORD'] = '<@Oumaima55>'       
app.config['MYSQL_DB'] = 'capstone_project'        
mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def index():
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
                return render_template("success.html")
            else:
                return render_template("error.html", error="Failed to establish database connection")
        except Exception as e:
            return render_template("error.html", error=str(e))

    return render_template('register.html')

# D'ont have account 
@app.route('/register')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
