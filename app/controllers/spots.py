from flask import render_template, redirect, session, flash, request
from app.models.skater import Skater
from app.models.spot import Spot
from app import app

#get all street spots
@app.route('/street')
def street():
    spots = Spot.get_all_streetspots()
    data = {
        "id": id,
    }
    skater = Skater.get_one(data)
    return render_template('street.html', spots=spots, skater=skater)

#get all skate parks
@app.route('/parks')
def parks():
    spots = Spot.get_all_skateparks()
    return render_template('parks.html', spots=spots)

#route to show add spot html page
@app.route('/addspot')
def add_spot_pg():
    data = {
        "id" :id,
    }
    skater = Skater.get_one(data);
    if 'skater_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    return render_template('add_spot.html',skater=skater)

#hidden route to create skate spot
@app.route('/createspot', methods=['POST'])
def create_spot():
    if 'skater_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    newSpot = {
        'skater_id' : session['skater_id'],
        'name' : request.form['name'],
        'spot_aka' : request.form['spot_aka'],
        'descr' : request.form['descr'],
        'address' : request.form['address'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'zip' : request.form['zip'],
        # 'lon' : request.form['lon'],
        # 'lat' : request.form['lat'],
        'type' : request.form['type'],
        'photos' : request.form['photos'],
        'rating' : request.form['rating'],
    }
    Spot.insert_spot(newSpot)
    flash("New spot added; let's get rolling.")
    return redirect('/dashboard')

#edit page
@app.route('/spots/<int:id>/edit')
def edit_spot(id):
    data = {
        'id': id,
    }
    spot = Spot.get_one_spot(data)
<<<<<<< HEAD
    # skater = Spot.get_skater_from_spot(data)
=======

    skdata = {
        "id": id,
    }
    skater = Skater.get_one(skdata)
>>>>>>> 9d4d8ecd47566283d6be89ca599b339b44a54cc7
    if 'skater_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    if spot.skater_id != session['skater_id']:
        flash('You did not create this spot to be able to udpate it.')
        return redirect('/dashboard')
<<<<<<< HEAD
    return render_template('edit_spot.html', spot=spot, skater = spot.skater_id)
=======
    return render_template('edit_spot.html', spot=spot, skater=skater)
>>>>>>> 9d4d8ecd47566283d6be89ca599b339b44a54cc7
    
    
@app.route('/spots/update', methods=['POST'])
def update_spot_in_db():
    data = {
        'skater_id' : session['skater_id'],
        'name' : request.form['name'],
        'spot_aka' : request.form['spot_aka'],
        'descr' : request.form['descr'],
        'address' : request.form['address'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'zip' : request.form['zip'],
        'lon' : request.form['lon'],
        'lat' : request.form['lat'],
        'type' : request.form['type'],
        'photos' : request.form['photos'],
        'rating' : request.form['rating'],
    }
    Spot.update_spot(data)
    return redirect('/dashboard')

#Delete spot
@app.route('/spots/<int:id>/delete')
def delete(id):
    data = {
        "id": id,
    }
    Spot.delete_spot(data)
    return redirect('/dashboard')


@app.route('/spots/<int:id>')
def show_spot(id):
    if 'skater_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    data = {
        'id': id,
    }
    udata = {
        'id' : session['skater_id']
    }
    return render_template('view_spot.html', spot=Spot.get_one_spot(data), skater=Skater.get_one(udata))