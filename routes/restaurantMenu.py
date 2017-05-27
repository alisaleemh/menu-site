from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

restaurantMenu = Blueprint('restaurantMenu', __name__,
                        template_folder='templates')
@restaurantMenu.route('/')
@restaurantMenu.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)
