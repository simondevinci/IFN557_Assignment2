from . import db
    
# THE ASSIGNMENT CLASSES ARE HERE 
# The item_category foreign key refers to the id of the Category class's primary key
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    extra_details = db.Column(db.String(300), nullable=False)
    item_category = db.Column(db.String(64), nullable = False)

    def __init__ (self, image, name, price, category, itemid, itemdescription, extradetails):
        self.image = image
        self.name = name
        self.price = price
        self.item_category = category
        self.id = itemid
        self.description = itemdescription
        self.extra_details = extradetails


    #def __repr__(self):
        #return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}\nPrice: {self.price}\nCategory: {self.item_category}"
    

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    shippingdetails = db.Column(db.String(64))
    item = db.Column(db.String(64))

    def __init__ (self, item):
        self.item = item
    
    #def __repr__(self):
        #return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.firstname}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nItems: {self.item}\nDate: {self.date}\nShipping Address: {self.shippingdetails}\nTotal Cost: ${self.total_cost}"
