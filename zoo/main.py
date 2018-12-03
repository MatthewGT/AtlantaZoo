# Atlanta Zoo newest

from flask import Flask,session
from flask import flash, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, LoginManager, login_user, logout_user
from forms import LoginForm, RegistrationForm, ExhibitForm, SearchShowForm,SearchAnimalForm,ExhibitHistoryForm, ShowHistoryForm,\
VisitorForm,AdminAnimalForm,AdminShowForm, AnimalCareForm
from models import User, Admin, Visitor, Staff, Animal, Show, Exhibit, AnimalCare, \
VisitShow, VisitExhibit, db
from tables import exhibit_table, show_table, animal_table, viewexhibit_table,viewshow_table,\
admin_visitor_table,admin_staff_table,admin_show_table,admin_animal_table,exhibit_detail_table,\
animal_detail_table,exhibit_animal_table,staff_show_table,staff_animal_table,animal_care_table
from dbQuery import Database
import time
from werkzeug.security import generate_password_hash, check_password_hash


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
    
    if (session.get('usertype') == 'visitor'):
        return redirect(url_for('visitor_main'))
    if (session.get('usertype') == 'staff'):
        return redirect(url_for('staff_main'))
    if (session.get('usertype') == 'admin'):
        return redirect(url_for('admin_main'))
    return render_template('index.html')

@app.route('/visitor/main')
def visitor_main():
    if session.get('isLogin') == True and session['usertype'] == 'visitor':
        return render_template('visitor_main.html')
    else:
        return render_template('403.html')

@app.route('/staff/main')
def staff_main():
    if session.get('isLogin') == True and session['usertype'] == 'staff':
        return render_template('staff_main.html')
    else:
        return render_template('403.html')

#### visitor search exhibit button 
def search_exhibit(search):
    results = Database().search_exhibits_visitor(search.data['exhibit_name'],search.data['max_animals'],search.data['min_animals'],search.data['max_size'],search.data['min_size'],search.data['water_feature'])
    if not results:
        flash('No results found!')
        return redirect('/exhibits/result')
    else:
        # Use Results() function to tablized the results list
        table = exhibit_table(results)
        table.border = True
        return render_template('search_exhibit_result.html', table=table)

@app.route('/exhibits/result', methods=['GET', 'POST'])
def exhibits_result():
    exhibit = ExhibitForm(request.form)
    if request.method == 'POST':
        return search_exhibit(exhibit)
    return render_template('search_exhibits.html', form=exhibit)

#### visitor search show button 
def search_show(search):
    results = Database().search_show_visitor(search.data['show_name'],search.data['exhibit_name'],search.data['date'])
    if not results:
        flash('No results found!')
        return redirect('/shows/result')
    else:
        table = show_table(results)
        table.border = True
        return render_template('search_show_result.html', table=table)

@app.route('/shows/result/<Name>/<Datetime>', methods=['GET', 'POST'])
def show_log_visit(Name, Datetime):
    Database().show_log_visit(session['username'],Name,Datetime)
    flash('log show visit')
    return redirect('/shows/result')

@app.route('/shows/result', methods=['GET', 'POST'])
def shows_result():
    show = SearchShowForm(request.form)
    if request.method == 'POST':
        return search_show(show)
    return render_template('search_shows.html', form=show)

#### visitor search anima button 
def search_animal(search):
    results = Database().search_animal_visitor(search.data['animal_name'],search.data['exhibit_name'],search.data['min_age'],search.data['max_age'],search.data['species'],search.data['animal_type'])
    if not results:
        flash('No results found!')
        return redirect('/animals/result')
    else:
        table = exhibit_animal_table(results)
        table.border = True
        return render_template('search_animal_result.html', table=table)

@app.route('/animals/result', methods=['GET', 'POST'])
def animals_result():
    animal = SearchAnimalForm(request.form)
    if request.method == 'POST':
        return search_animal(animal)
    return render_template('search_animals.html',form=animal)

###visitor view exhibit history 
def view_exhibit_history(search):
    results = Database().search_exhibit_history(search.data['exhibit_name'],search.data['min_visits'],search.data['max_visits'],search.data['visit_time'],session['username'])
    if not results:
        flash('No results found!')
        return redirect('/exhibits/history')
    else:
        table = viewexhibit_table(results)
        table.border = True
        return render_template('view_exhibit_history.html', table=table)

@app.route('/exhibits/history', methods=['GET', 'POST'])
def exhibits_history():
    exhibit = ExhibitHistoryForm(request.form)
    if request.method == 'POST':
        return view_exhibit_history(exhibit)
    return render_template('exhibit_history.html',form=exhibit)

@app.route('/exhibits/history/<Exhibit>', methods=['GET', 'POST'])
def exhibit_history_detail(Exhibit):
    result1 = Database().visitor_exhibit_detail(Exhibit)
    result2 = Database().visitor_exhibit_animal(Exhibit)
    if (not result1) or (not result2):
        flash('No results found!')
        return redirect('/exhibits/history')
    else:
        table1 = exhibit_detail_table(result1)
        table2 = animal_detail_table(result2)
        table1.border = True
        table2.border = True
        return render_template('exhibit_detail.html', table1=table1,table2=table2)

###visitor view exhibit history 
def view_show_history(search):
    results = Database().search_show_history(search.data['show_name'],search.data['exhibit_name'],search.data['date'], session['username'])
    if not results:
        flash('No results found!')
        return redirect('/shows/history')
    else:
        table = viewshow_table(results)
        table.border = True
        return render_template('view_show_history.html', table=table)

@app.route('/shows/history', methods=['GET', 'POST'])
def shows_history():
    show = ShowHistoryForm(request.form)
    if request.method == 'POST':
        return view_show_history(show)
    return render_template('show_history.html',form=show)





@app.route('/user/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        session.pop('_flashes', None)
        user = Database().get_user(form.email.data)
        if len(user) != 0:
            username = Database().find_user_name(user[0]['Email'])
            session['username'] = username[0]['Username']
            session['isLogin'] = True
        if len(user) != 0 and check_password_hash(user[0]['Password_hash'],form.password.data):
            # login_user(user, form.remember_me.data)
            if (user[0]['UserType'] == 'visitor'):
                session['usertype'] = 'visitor'
                return redirect(url_for('visitor_main'))
            if (user[0]['UserType'] == 'staff'):
                session['usertype'] = 'staff'
                return redirect(url_for('staff_main'))
            if (user[0]['UserType'] == 'admin'):
                session['usertype'] = 'admin'
                return redirect(url_for('admin_main'))
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u'Invalid username or password.', 'error')
    return render_template('login.html', form=form)

@app.route('/user/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(Database().get_user(form.email.data)) != 0 or len(Database().get_user(form.username.data)) != 0:
            raise ValidationError('Email or usernamealready registered.')
        else:
            Database().register_user(form.username.data,form.email.data,form.usertype.data,generate_password_hash(form.password.data))
            flash('You can now login.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Admin url routes
@app.route('/admin/main')
def admin_main():
    if session.get('isLogin') == True and session['usertype'] == 'admin':
        return render_template('admin_main.html')
    else:
        return render_template('403.html')

###admin view visitor list 
def view_visitor_list():
    ## set order 
    results = Database().view_visitor_admin(0)
    if not results:
        flash('No results found!')
        return redirect('/admin/main')
    else:
        table = admin_visitor_table(results)
        table.border = True
        return render_template('admin_view_visitor.html', table=table)

@app.route('/visitors/all', methods=['GET', 'POST'])
def admin_view_visitor():
    return view_visitor_list()

###admin view Staff list 
def view_staff_list():
    ## set order 
    results = Database().view_staff_admin(0)
    if not results:
        flash('No results found!')
        return redirect('/admin/main')
    else:
        table = admin_staff_table(results)
        table.border = True
        return render_template('admin_view_staff.html', table=table)

@app.route('/staffs/all', methods=['GET', 'POST'])
def admin_view_staff():
    return view_staff_list()


# Admin View Shows Button
def admin_search_show(search):
    results = Database().search_show_visitor(search.data['show_name'],search.data['exhibit_name'],search.data['date'])
    if not results:
        flash('No results found!')
        return redirect('/shows/all')
    else:
        table = admin_show_table(results)
        table.border = True
        return render_template('search_show_result.html', table=table)

@app.route('/shows/all', methods=['GET', 'POST'])
def view_show():
    show = SearchShowForm(request.form)
    if request.method == 'POST':
        return admin_search_show(show)
    return render_template('search_shows.html', form=show)

# View Animals Button
def admin_search_animal(search):
    results = Database().search_animal_visitor(search.data['animal_name'],search.data['exhibit_name'],search.data['min_age'],search.data['max_age'],search.data['species'],search.data['animal_type'])
    if not results:
        flash('No results found!')
        return redirect('/animals/all')
    else:
        table = admin_animal_table(results)
        table.border = True
        return render_template('search_animal_result.html', table=table)
@app.route('/animals/all', methods=['GET', 'POST'])
def view_animals():
    animal = SearchAnimalForm(request.form)
    if request.method == 'POST':
        return admin_search_animal(animal)
    return render_template('search_animals.html',form=animal)

# Admin Add Animal Button
def admin_add_animal(search):
    ## set order 
    Database().admin_add_animal(search.data['animal_name'],search.data['species'],search.data['animal_type'],search.data['age'],search.data['exhibit_name'])
    flash('Add Animal Successfully!')
    return redirect('/animals/add')
    
@app.route('/animals/add', methods=['GET', 'POST'])
def add_animal():
    animal_form = AdminAnimalForm()
    if request.method == 'POST':
        return admin_add_animal(animal_form)
    return render_template('add_animal.html', form=animal_form)


# Admin Add Show Button
def admin_add_show(search):
    ## set order 
    Database().admin_add_show(search.data['show_name'],search.data['date']+search.data['time'],search.data['staff'],search.data['exhibit_name'])
    flash('Add Show Successfully!')
    time.sleep(1)
    return redirect('/shows/add')

@app.route('/shows/add', methods=['GET', 'POST'])
def add_show():
    show_form = AdminShowForm()
    if request.method == 'POST':
        #flash('Add Show Successfully!')
        return admin_add_show(show_form)
    return render_template('add_show.html', form=show_form)



####functions for admin operation 

# admin delete visitor
@app.route('/visitors/all/<Username>', methods=['GET', 'POST'])
def delete_visitor(Username):
    Database().admin_delete_visitor(Username)
    flash('delete visitor Successfully')
    return redirect('/visitors/all')

# admin delete visitor
@app.route('/staffs/all/<Username>', methods=['GET', 'POST'])
def delete_staff(Username):
    Database().admin_delete_staff(Username)
    flash('delete staff Successfully')
    return redirect('/staffs/all')

# admin delete show
@app.route('/shows/all/<Name>/<Datetime>', methods=['GET', 'POST'])
def delete_show(Name,Datetime):
    Database().admin_delete_show(Name,Datetime)
    flash('delete show Successfully')
    return redirect('/shows/all')

# admin delete show
@app.route('/animals/all/<Name>/<Species>', methods=['GET', 'POST'])
def delete_animal(Name,Species):
    Database().admin_delete_animal(Name,Species)
    flash('delete animal Successfully')
    return redirect('/animals/all')



####visitor operations
@app.route('/exhibits/result/<Name>', methods=['GET', 'POST'])
def exhibit_detail(Name):
    result1 = Database().visitor_exhibit_detail(Name)
    result2 = Database().visitor_exhibit_animal(Name)
    if (not result1) or (not result2):
        flash('No results found!')
        return redirect('/exhibits/result')
    else:
        table1 = exhibit_detail_table(result1)
        table2 = animal_detail_table(result2)
        table1.border = True
        table2.border = True
        return render_template('exhibit_detail.html', table1=table1,table2=table2)

@app.route('/exhibits/result/<Name>/<DName>', methods=['GET', 'POST'])
def log_visit(Name,DName):
    Database().exhibit_log_visit(session['username'],Name)
    flash('Log Exhibit Successfully')
    return redirect('/exhibits/result/'+Name)



@app.route('/exhibits/result/<Ename>/<Name>/<Species>', methods=['GET', 'POST'])
def view_animal_detail(Ename,Name,Species):
    result = Database().click_animal_detail(Name,Species)
    if not result:
        flash('No results found!')
        return redirect('/exhibits/result/'+Ename)
    else:
        table = animal_table(result)
        table.border = True
        return render_template('search_animal_result.html', table=table)

####staff operations
# staff View Shows Button

@app.route('/staff/shows/', methods=['GET', 'POST'])
def staff_view_show():
    result = Database().staff_view_show(session['username'],0)
    if not result:
        flash('No results found!')
        return redirect('/staff/main')
        #return redirect('/staff/shows/')
    else:
        table = staff_show_table(result)
        table.border = True
        return render_template('staff_shows_view.html', table=table)

#### staff search anima button 
def staff_search_animal(search):
    results = Database().search_animal_visitor(search.data['animal_name'],search.data['exhibit_name'],search.data['min_age'],search.data['max_age'],search.data['species'],search.data['animal_type'])
    if not results:
        flash('No results found!')
        return redirect('/staff/animals/')
    else:
        table = staff_animal_table(results)
        table.border = True
        return render_template('search_animal_result.html', table=table)

@app.route('/staff/animals/<Name>/<Species>', methods=['GET', 'POST'])
def animal_care_detail(Name,Species):
    result1 = Database().click_animal_detail(Name,Species)
    result2 = Database().staff_view_note(Name,Species,0)
    if (not result1) and (not result2):
        flash('No results found!')
        return redirect('/staff/animals/')
    else:
        table1 = animal_table(result1)
        table2 = animal_care_table(result2)
        table1.border = True
        table2.border = True
        return render_template('staff_animal_care.html', table1=table1,table2=table2, name=result1[0].get('Name'), species=result1[0].get('Species'))

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    if request.method=='POST':
        Database().staff_log_notes(request.form['name'],request.form['Species'],session['username'],request.form['note'])
        flash('Insert Note Successfully')
        return redirect('/staff/animals/'+request.form['name']+'/'+request.form['Species'])
    return redirect('/staff/animals/'+request.form['name']+'/'+request.form['Species'])


@app.route('/staff/animals', methods=['GET', 'POST'])
def staff_animals_care():
    animal = SearchAnimalForm(request.form)
    if request.method == 'POST':
        return staff_search_animal(animal)
    return render_template('search_animals.html',form=animal)


if __name__ == '__main__':
    app.run(debug=True)