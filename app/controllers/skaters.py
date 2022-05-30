from flask import render_template, redirect, session, flash, request
from app.models.skater import Skater
# from app.models.recipe import Recipe
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

#page for login/register
@app.route('/loginpg')
def loginpg():
    return render_template('login_reg.html')

#hidden route for registration form
@app.route('/register', methods=['POST'])
def register():
    isValid = Skater.validate_registration(request.form)
    if not isValid:
        return redirect('/')
    newSkater = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        #hash password
        'password' : bcrypt.generate_password_hash(request.form['password']),
    }
    id = Skater.insert(newSkater)
    if not id:
        flash('Something went wrong.')
        return redirect('/')
    session['skater_id'] = id
    # flash('You are logged in.')
    return redirect('/dashboard')

#hidden route from login form
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    skater = Skater.get_email(data)
    if not skater:
        flash('That email is not in our database. Please register.')
        return redirect('/')
    if not bcrypt.check_password_hash(skater.password, request.form['password']):
        flash('Wrong password.')
        return redirect('/')
    session['skater_id'] = skater.id
    # flash('You are logged in.')
    return redirect('/dashboard')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/street')
def street():
    return render_template('street.html')

@app.route('/parks')
def parks():
    return render_template('parks.html')

@app.route('/map')
def mapview():
    return render_template('map.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')



#view page after login successfully
@app.route('/dashboard')
def dashboard():
    if 'skater_id' not in session:
        flash('You must be logged in to view this page. Routing back home.')
        return redirect('/login')
    data = {
        'id' : session['skater_id']
    }
    results = Skater.get_all()
    return render_template('dashboard.html', skaterList = results, skater=Skater.get_one(data))

#logout hidden method, redirect back to index login page.
@app.route('/logout')
def logout():
    session.clear()
    # flash('You are now logged out.')
    return redirect('/')

