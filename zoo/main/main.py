from flask import Flask
from flask import flash, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/main')
def user_main():
    return render_template('user_main.html')

if __name__ == '__main__':
    app.run(debug=True)