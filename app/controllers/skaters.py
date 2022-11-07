from flask import render_template, redirect, session, flash, request
from app.models.skater import Skater
from app.models.spot import Spot
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
        return redirect('/loginpg')
    newSkater = {
        'username' : request.form['username'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        #hash password
        'password' : bcrypt.generate_password_hash(request.form['password']),
        # 'bio' : request.form['bio'],
        # 'stance' : request.form['stance'],
        # 'avatar' : request.form['avatar'],
    }
    id = Skater.insert(newSkater)
    if not id:
        flash('Something went wrong.')
        return redirect('/loginpg')
    session['skater_id'] = id
    # flash('You are logged in.')
    return redirect('/dashboard')

#hidden route from login form
@app.route('/login', methods=['POST'])
def login():
    data = {
        'username' : request.form['username']
    }
    skater = Skater.get_username(data)
    if not skater:
        flash('That username is not in our database. Please register.')
        return redirect('/loginpg')
    if not bcrypt.check_password_hash(skater.password, request.form['password']):
        flash('Wrong password.')
        return redirect('/loginpg')
    session['skater_id'] = skater.id
    # flash('You are logged in.')
    return redirect('/dashboard')

#edit user page
@app.route('/profile/<int:id>/edit')
def edit_user(id):
    data = {
        "id" : id,
    }
    skater = Skater.get_one(data)
    return render_template('edit_user.html', skater=skater)

#Update user in db from form
@app.route('/profile/<int:id>/update', methods=['POST'])
def update_db(id):
    data = {
        'id' : id,
        'username' : request.form['username'],
        'password' : request.form['password'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'bio' : request.form['bio'],
        'stance' : request.form['stance'],
        'avatar' : request.form['avatar'],
    }
    Skater.update(data)
    return redirect(f'/dashboard')


# Add favorite
@app.route('/spot/<int:id>/fav')
def add_fav(id):
    data = {
        "skater_id": session['skater_id'],
        "spot_id": id
    }
    Skater.add_skater_fav(data)
    return redirect('/dashboard')

@app.route('/community')
def community():
    return render_template('community.html')


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
    allSpots = Spot.get_all_spots()
    return render_template('dashboard.html', skaterList = results, skater=Skater.get_one(data), fav=Skater.get_favs(data), spots = allSpots)


#logout hidden method, redirect back to index login page.
@app.route('/logout')
def logout():
    session.clear()
    # flash('You are now logged out.')
    return redirect('/')

