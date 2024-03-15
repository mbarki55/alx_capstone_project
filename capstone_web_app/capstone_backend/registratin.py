from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Add your login logic here
    return f'Login attempt with username: {username} and password: {password}'

@app.route('/signup', methods=['POST'])
def signup():
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    # Add your sign up logic here
    return f'Sign up attempt with username: {new_username} and password: {new_password}'

if __name__ == '__main__':
    app.run(debug=True)
