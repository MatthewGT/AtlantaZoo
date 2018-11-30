from flask import Flask
from flask import flash, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/main')
def user_main():
    return render_template('user_main.html')

@app.route('/exhibits/result')
def exhibits_result():
    return render_template('search_exhibits.html')

@app.route('/exhibits/history')
def exhibits_history():
    return render_template('exhibit_history.html')

@app.route('/shows/result')
def shows_result():
    return render_template('search_shows.html')

@app.route('/shows/history')
def shows_history():
    return render_template('show_history.html')

@app.route('/animals/result')
def animals_result():
    return render_template('search_animals.html')

if __name__ == '__main__':
    app.run(debug=True)