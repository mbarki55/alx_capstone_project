from flask import Flask, render_template, request, redirect, url_for, session
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
    return render_template('about.html')

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

                # Check if username or email already exists
                cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
                existing_user = cur.fetchone()

                if existing_user:
                    # Username or email already exists, render registration template with error message
                    return render_template("register.html", message="Username or email already exists!")

                # Insert the new user if username and email are unique
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for("login"))  #return to the login page after successful registration
        except Exception as e:
            return render_template("error.html", error=str(e))

    return render_template('register.html')

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
                session['user_id'] = user[0]  # Store user_id in session
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", message="Invalid username or password !")

    return render_template('login.html')

# Python code

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        conn = MySQLdb.connect(host='localhost', user='root', password='<@Oumaima55>', database='capstone_project')
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts WHERE user_id = %s", (session['user_id'],))
        posts = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("dashboard.html", username=session['username'], posts=posts)
    else:
        return redirect(url_for('login'))

# logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# create post
@app.route('/dashboard/create_post', methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        user_id = session.get('user_id')

        conn = MySQLdb.connect(host='localhost', user='root', password='<@Oumaima55>', database='capstone_project')
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s)", (title, content, user_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('dashboard'))  # Redirect to home page after creating the post

    return render_template('dashboard')

# create comment
@app.route('/dashboard/create_comment', methods=["POST"])
def create_comment():
    if request.method == "POST":
        post_id = request.form["post_id"]
        comment_text = request.form["comment_text"]
        user_id = session.get('user_id')

        conn = MySQLdb.connect(host='localhost', user='root', password='<@Oumaima55>', database='capstone_project')
        cur = conn.cursor()
        cur.execute("INSERT INTO comments (post_id, user_id, comment_text) VALUES (%s, %s, %s)", (post_id, user_id, comment_text))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('dashboard'))  # Redirect to home page after creating the comment

    return redirect(url_for('dashboard'))  # If request method is not POST, redirect to home page


# run the app
if __name__ == '__main__':
    app.run(debug=True)
