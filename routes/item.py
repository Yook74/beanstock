from datetime import datetime, timedelta

from flask import Blueprint, render_template, jsonify, request, redirect
from werkzeug.exceptions import BadRequest
from sqlalchemy import or_

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

@bluep.get('new')
def new_item_page():
    return render_template('new_item.html',
        item_types=ItemType.query.all()
    )

@bluep.post('new')
def add_new_item():
    item = Item(
        short_name=request.form['newItem'],
        cost=request.form["itemCost"],
        standard_price=request.form["itemPrice"],
        type_id=request.form["itemType"]
    )
    db.session.add(item)
    db.session.commit()

    return redirect(f'{item.id}/adjust')


@bluep.get('<int:id>/adjust')
@by_id(Item)
def adjust_item(item):
    after_date = datetime.now() - timedelta(days=7)
    return render_template('adjust_item.html', item=item,
        active_sale_contexts=SaleContext.query.filter(or_(SaleContext.end_time == None, SaleContext.end_time > after_date))
    )


@bluep.post('<int:id>/quantity')
@by_id(Item)
def set_quantity(item):
    if request.json.get('weight'):
        if request.json.get('weightForOne'):
            item.weight_grams = float(request.json['weightForOne'])

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