from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# set the DB connection
engine = create_engine(
    'sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
dbsession = sessionmaker(bind = engine)
session = dbsession()

# @app.route = static and dynamic pass = used to bind a function to a URL
@app.route('/')
@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurantslist.html', restaurant_list=restaurants)

# last '/' important to handle presence/absence of '/' in the URL
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def restaurantNew():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['newRestaurantName'])
        session.add(newRestaurant)
        session.commit()
        flash("Success! New restaurant added!")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def restaurantDelete(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Success! Restaurant deleted!")
        return redirect(url_for('restaurantList'))
    else:
        # for a GET request
        return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant_name=restaurant.name)

@app.route('/restaurants/<int:restaurant_id>/menu/', methods=['GET', 'POST'])
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=menuitems)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['newMenuItemName'], restaurant_id=restaurant_id)
        session.add(newMenuItem)
        session.commit()
        flash("Success! New menu item added!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # for a GET request
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['editMenuItemName']:
            menuitem.name = request.form['editMenuItemName']
        session.add(menuitem)
        session.commit()
        flash("Success! Menu item edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # for a GET request
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, itemName=menuitem.name, menu_id=menu_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        flash("Success! Menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # for a GET request
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, itemName=menuitem.name, menu_id=menu_id)

#Make an API endpoint for GET request
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[menuitem.serialize for menuitem in menuitems])

#Make an API endpoint for GET request
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=menuitem.serialize)

# run only if the script is run from Python interpreter. Not if it is imported.
if __name__ == '__main__':
    # server will reload everytime it sees a code change, also provides a
    # debugger in the browser
    app.debug = True
    # message flashing
    # used by Flask to create sessions for users
    app.secret_key = 'a-real-super-secret-key'
    app.run(host = '0.0.0.0', port = 5000)
