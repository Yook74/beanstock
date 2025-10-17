from flask import Blueprint, render_template, jsonify, request
from werkzeug.exceptions import BadRequest
from datetime import datetime

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


@bluep.get('<int:id>/adjust')
@by_id(Item)
def adjust_item(item):
    return render_template(
        'adjust_item.html',
        item=item,
        active_sale_contexts=SaleContext.query.filter(SaleContext.end_time == None) # TODO or ended recently
    )


@bluep.post('<int:id>/quantity')
@by_id(Item)
def set_quantity(item):
    new_quantity = 0
    if request.json.get('weight'):
        # TODO what if not weight_in_grams
        new_quantity = round(float(request.json.get('weight')) / item.weight_grams)
    elif request.json.get('quantity'):
        new_quantity = int(request.json.get('quantity'))
    else:
        raise BadRequest('Need weight or quantity')

    if request.json.get('context'):
        context_id = int(request.json.get('context'))
        if new_quantity > item.quantity:
            raise BadRequest('How sell thing and qty go up?????')

        for _ in range(item.quantity - new_quantity):
            # TODO price
            db.session.add(Sale(item=item, context_id=context_id, timestamp=datetime.now()))

    item.quantity = new_quantity
    db.session.commit()

    return 'updated'