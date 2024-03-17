from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key='kjhbd67hjsk'

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
            new_password = request.form["new_password"]

            conn = MySQLdb.connect(host='localhost', user='root', password='<@Oumaima55>', database='capstone_project')

            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password, new_password))
                conn.commit()
                cur.close()
                conn.close() 
                flash("successful registration")
            else:
                flash("Failed to establish database connection")
            if password != new_password:
                flash("Passwords do not match!")
            
        except Exception as e:
            return render_template("error.html", error=str(e))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
