from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from session_manager import SessionManager
from routes import restaurantMenu

app = Flask(__name__)

db = SessionManager()


# List of All Restaurants
@app.route('/')
@app.route('/restaurant')
@app.route('/restaurant/all')
def allRestaurants():
    restaurants = db.session.query(Restaurant).all()
    return render_template('allRestaurant.html', restaurants=restaurants)


# Adds a New Restaurant Entry
@app.route('/resturant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        if request.form['name']:
            newItem = Restaurant(name=request.form['name'])
            db.session.add(newItem)
            db.session.commit()
            flash("new restaurant menu successfully created")
            return redirect(url_for('allRestaurants'))
        else:
            render_template('newRestaurant.html')


# Edits a Restaurant Entry
# Input: restaurant_id
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        editItem = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
        editItem.name = request.form['name']
        db.session.commit()
        flash("restaurant %s successfully edited" % editItem.name)
        return redirect(url_for('allRestaurants'))
    else:
        render_template('editRestaurant.html')


# Delete a Restaurant
# Input: restaurant_id
@app.route('/restaurant/<int:restaurant_id>')
def deleteRestaurant(restaurant_id):
    deleteItem = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        db.session.delete(deleteItem)
        db.session.commit()
        flash("restaurant %s successfully deleted" % deleteItem.name)
        return redirect (url_for('allRestaurants'))
    else:
        return render_template('deleteRestaurant')


# Menu of a Specific Restaurant
# Input: restaurant_id
@app.route('/restaurant/<int:restaurant_id>/')
def showRestaurantMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# New Menu Item in a Specific Restaurant
# Input: restaurant_id
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        db.session.add(newItem)
        db.session.commit()
        flash("new item successfully added")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Edit a Menu Item in a Specific Restaurant
# Input: restaurant_id, menu_id
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        editItem = db.session.query(MenuItem).filter_by(id=menu_id).one()
        editItem.name = request.form['name']
        db.session.commit()
        flash("menu item successfully edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id)


# Delete a Menu Item in a Specific Restaurant
# Input: restaurant_id, menu_id
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        db.session.delete(deleteItem)
        db.session.commit()
        flash("menu item successfully deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=deleteItem)

# Return a JSON object of the Menu in a Specific Restaurant
# Input: restaurant_id
@app.route('/restaurant/<int:restaurant_id>/menu/json/')
def restaurantMenuJson(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])



if __name__ == '__main__':
    app.secret_key = "tatta"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
