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

    #category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    #category = relationship('Category', back_populates='items')

    def __init__ (self, image, name, price, category, itemid, itemdescription, extradetails, categoryid):
        self.image = image
        self.name = name
        self.price = price
        self.item_category = category
        self.id = itemid
        self.description = itemdescription
        self.extra_details = extradetails
        self.item_category_id = categoryid

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}\nPrice: {self.price}\nCategory: {self.item_category}"
    

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

    #item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    #item = relationship('Item')
    
    def __init__ (self, status, firstname, surname, email, phone, totalcost, date, item):
        self.status = status
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.phone = phone
        self.total_cost = totalcost
        self.date = date
        self.item = item
    
    def __repr__(self):
        return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.firstname}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nItems: {self.item}\nDate: {self.date}\nShipping Address: {self.shippingdetails}\nTotal Cost: ${self.total_cost}"
    
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    #items = relationship('Item', back_populates='category')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}"
