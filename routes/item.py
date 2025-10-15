from flask import Blueprint, render_template, jsonify

from routes import by_id
from models import *

bluep = Blueprint('item', __name__, url_prefix='/item')


@bluep.get('<int:id>')
@by_id(Item)
def one_item(item):
    return jsonify({
        'short_name': item.short_name,
        'cost': item.cost
    })
