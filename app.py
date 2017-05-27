from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from session_manager import SessionManager

app = Flask(__name__)

db = SessionManager()


# Task 1: Create route for newMenuItem function here

@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        db.session.add(newItem)
        db.session.commit()
        flash("new item successfully added")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        editItem = db.session.query(MenuItem).filter_by(id=menu_id).one()
        editItem.name = request.form['name']
        db.session.commit()
        flash("menu item successfully edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        db.session.delete(deleteItem)
        db.session.commit()
        flash("menu item successfully deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=deleteItem)


@app.route('/restaurant/<int:restaurant_id>/menu/json/')
def restaurantMenuJson(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = "tatta"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)