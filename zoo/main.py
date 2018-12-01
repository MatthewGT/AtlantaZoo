from flask import Flask
from flask import flash, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, LoginManager, login_user, logout_user
from forms import LoginForm, RegistrationForm, ExhibitForm, SearchShowForm, \
AnimalCareForm, AnimalForm, ExhibitHistoryForm, ShowForm
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
    exhibit = ExhibitHistoryForm()
    return render_template('exhibit_history.html', form=exhibit)

@app.route('/shows/result')
def shows_result():
    show_form = SearchShowForm()
    return render_template('search_shows.html', form=show_form)

@app.route('/shows/history')
def shows_history():
    show_history = SearchShowForm()
    return render_template('show_history.html', form=show_history)

@app.route('/animals/result')
def animals_result():
    animal_form = AnimalForm()
    return render_template('search_animals.html', form=animal_form)

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
                return redirect(url_for('staff_main'))
            if (user.UserType == 'admin'):
                return redirect(url_for('admin_main'))
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

# Admin url routes
@app.route('/admin/main')
def admin_main():
    return render_template('admin_main.html')

# View Staff Button
@app.route('/staffs/all', methods=['GET', 'POST'])
def view_staff():
    return render_template('staff_list_ad.html')

# View Shows Button
@app.route('/shows/all', methods=['GET', 'POST'])
def view_show():
    form = SearchShowForm()
    return render_template('show_list_ad.html', form = form)

# View Animals Button
@app.route('/animals/all', methods=['GET', 'POST'])
def view_animals():
    animal_form = AnimalForm()
    return render_template('animal_list_ad.html', form=animal_form)

# View Visitors Button
@app.route('/visitors/all', methods=['GET', 'POST'])
def view_visitors():
    return render_template('visitor_list_ad.html')

# Add Show Button
@app.route('/shows/add', methods=['GET', 'POST'])
def add_show():
    show_form = ShowForm()
    return render_template('add_show.html', form=show_form)

# Add Animal Button
@app.route('/animals/add', methods=['GET', 'POST'])
def add_animal():
    animal_form = AnimalForm()
    return render_template('add_animal.html', form=animal_form)

if __name__ == '__main__':
    app.run(debug=True)