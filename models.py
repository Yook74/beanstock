from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ItemType(db.Model):
    """sticker, print. standee, etc."""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


class Item(db.Model):
    """A type of stocked macguffin. For example, a particular print design"""
    id = db.Column(db.Integer(), primary_key=True)
    type_id = db.Column(db.Integer(), db.ForeignKey('item_type.id'))
    short_name = db.Column(db.String(128), nullable=False, unique=True)
    cost = db.Column(db.Numeric(precision=8, scale=2))
    standard_price = db.Column(db.Numeric(precision=8, scale=2))
    weight_grams = db.Column(db.Float())
    quantity = db.Column(db.Integer())

    type = db.relationship('ItemType', backref='items')


class Sale(db.Model):
    """One of these happens when exactly one of an item is sold"""
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'))
    context_id = db.Column(db.Integer(), db.ForeignKey('sale_context.id'))
    timestamp = db.Column(db.DateTime)
    price = db.Column(db.Numeric(precision=8, scale=2))

    item = db.relationship('Item', backref='sales')
    context = db.relationship('SaleContext', backref='sales')


class SaleContext(db.Model):
    """A particular year of a con, or Etsy, or Iron Lion"""
    id = db.Column(db.Integer(), primary_key=True)
    con_id = db.Column(db.Integer(), db.ForeignKey('con.id'), nullable=True)
    name = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.Text())
    end_time = db.Column(db.DateTime)

    con = db.relationship('Con', backref='contexts')


class Con(db.Model):
    """A recurring event where things are sold"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
