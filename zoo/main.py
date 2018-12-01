from flask import Flask
from flask import flash, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, LoginManager, login_user, logout_user
from forms import LoginForm, RegistrationForm, ExhibitForm
from models import User, Admin, Visitor, Staff, Animal, Show, Exhibit, AnimalCare, \
VisitShow, VisitExhibit, db
from exhibit_table import Results

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guessing'
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(Username):
    return User.query.get(str(Username))

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/visitor/main')
def visitor_main():
    return render_template('visitor_main.html')

@app.route('/staff/main')
def staff_main():
    return render_template('staff_main.html')

@app.route('/admin/main')
def admin_main():
    return render_template('admin_main.html')

def search_exhibit(search):
    ### copy of musicdb start here
    results = []
    exhibit_name = search.data['exhibit_name']
    min_size = search.data['min_size']
    max_size = search.data['max_size']

    qry = db.session.query(Exhibit).filter(
                Exhibit.Name.contains(exhibit_name), \
                Exhibit.Size > min_size, \
                Exhibit.Size < max_size)
    results = qry.all()
    # print(search_string)
    # # check if the user has entered a search string in the search box
    # if search_string:
    #     # check to see which filter the user has chosen from the combobox:
    #     # Artist, Album or Publisher
    #     if search.data['exhibit_name'] == 'Pacific':
    #         qry = db.session.query(Exhibit).filter(
    #             Exhibit.Name.contains(search_string))
    #         results = qry.all()
    #     # elif search.data['select'] == 'Album':
    #     #     qry = db_session.query(Album).filter(
    #     #         Album.title.contains(search_string))
    #     #     results = qry.all()
    #     # elif search.data['select'] == 'Publisher':
    #     #     qry = db_session.query(Album).filter(
    #     #         Album.publisher.contains(search_string))
    #     #     results = qry.all()
    #     # else:
    #     #     qry = db_session.query(Album)
    #     #     results = qry.all()
    # else:
    #     qry = db.session.query(Exhibit)
    #     results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/exhibits/result')
    else:
        # Use Results() function to tablized the results list
        table = Results(results)
        table.border = True
        return render_template('exhibit_result.html', table=table)

@app.route('/exhibits/result', methods=['GET', 'POST'])
def exhibits_result():
    print("insied exhibit")
    exhibit = ExhibitForm(request.form)
    # print("exhibit name", exhibit.data['exhibit_name'])
    if request.method == 'POST':
        print("inside POST")
        return search_exhibit(exhibit)
    return render_template('search_exhibits.html', form=exhibit)

@app.route('/exhibits/history')
def exhibits_history():
    return render_template('exhibit.html')

@app.route('/shows/result')
def shows_result():
    return render_template('search_shows.html')

@app.route('/shows/history')
def shows_history():
    return render_template('show_history.html')

@app.route('/animals/result')
def animals_result():
    return render_template('search_animals.html')

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    flash('hello')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if (user.UserType == 'visitor'):
                return redirect(url_for('visitor_main'))
            if (user.UserType == 'staff'):
                return url_for('staff_main')
            if (user.UserType == 'admin'):
                return url_for('admin_main')
            #return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u'Invalid username or password.', 'error')
    return render_template('login.html', form=form)

app.route('/user/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if(form.usertype.data == 'visitor'):
            user = User(Username=form.username.data,
                    password=form.password.data,
                    Email=form.email.data,
                    UserType=form.usertype.data
                    )
            visitorname = Visitor(user_visitor=username)
            db.session.add_all([user,visitorname])
            db.session.commit()
        if (form.usertype.data == 'staff'):
            user = User(Username=form.username.data,
                    password=form.password.data,
                    Email=form.email.data,
                    UserType=form.usertype.data
                    )
            staffname = Staff(user_staff=user)
            db.session.add_all([user,staffname])
            db.session.commit()
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)