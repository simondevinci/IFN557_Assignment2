from . import db

# THE ASSIGNMENT CLASSES ARE HERE 
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    extra_details = db.Column(db.String(300), nullable=False)
    item_category = db.Column(db.String(64), nullable = False)
    item_category_id = db.Column(db.Integer, nullable = False)

    itemcategoryid = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}\nPrice: {self.price}\nCategory: {self.itemcategoryid}"
    
orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('item_id',db.Integer,db.ForeignKey('items.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'item_id') )

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    total_cost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    shippingdetails = db.Column(db.String(64))
    items = db.relationship("Item", secondary = orderdetails, backref = "orders")
    
    def __repr__(self):
        return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.firstname}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nItems: {self.items}\nDate: {self.date}\nShipping Address: {self.shippingdetails}\nTotal Cost: ${self.total_cost}"
    
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    items = db.relationship('Item', backref='Category', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}"
