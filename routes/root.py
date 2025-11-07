from flask import Blueprint, render_template

from models import *

bluep = Blueprint('root', __name__, url_prefix='/')


@bluep.get('')
def home():
    types = ItemType.query.all()

    total_value = 0
    for type in types:
        for item in type.items:
            if item.standard_price and item.quantity:
                total_value += item.standard_price * item.quantity

    return render_template('home.html', total_value=total_value, item_types=types)
