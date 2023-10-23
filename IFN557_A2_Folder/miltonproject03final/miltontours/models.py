from . import db

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultcity.jpg')
    tours = db.relationship('Tour', backref='City', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}"
orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('tour_id',db.Integer,db.ForeignKey('tours.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'tour_id') )

class Tour(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    
    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}\nPrice: {self.price}\nCity: {self.city_id}\nDate: {self.date}"

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
    tours = db.relationship("Tour", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.first_name}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nDate: {self.date}\nTours: {self.tours}\nTotal Cost: ${self.total_cost}"
    
# THE ASSIGNMENT CLASSES ARE HERE 
# The item_category foreign key refers to the id of the Category class's primary key
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    item_category = db.relationship("Category", secondary=itemcategory, backref="items")
    
    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}\nPrice: {self.price}\nCategory: {Category.name}"
#A REFERENCE TABLE TO COMPARE WHAT ID IS WHAT CATEGORY NAME BETWEEN THE ITEM AND CATEGORY CLASSES
itemdetails = db.Table('itemcategory', 
    db.Column('item_id', db.Integer,db.ForeignKey('items.id'), nullable=False),
    db.Column('category_id',db.Integer,db.ForeignKey('categories.id'),nullable=False),
    db.PrimaryKeyConstraint('item_id', 'category_id') )
    
#NEED THIS CLASS TO REMEMBER ALL THE "TAG" POSSIBLE FOR THE ITEMS BY CATEGORY 
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64),nullable = False)
    

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
    itemnames = db.relationship("Item", secondary=itemdetails, backref="orders")
    
    def __repr__(self):
        return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.firstname}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nItems: {self.itemnames}\nDate: {self.date}\nTotal Cost: ${self.total_cost}"