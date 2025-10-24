from flask import Blueprint, render_template

from models import *

bluep = Blueprint('root', __name__, url_prefix='/')


@bluep.get('')
def home():
    items = Item.query.all()

    total_value = 0
    for item in items:
        total_value += item.standard_price * item.quantity

    return render_template('home.html', total_value=total_value, items=items)
