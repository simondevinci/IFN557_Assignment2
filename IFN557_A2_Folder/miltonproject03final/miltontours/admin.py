'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import Order, Item
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
    #ADDING ITEM DATA
    t1 = Item(image="t_AirPods.jpg",name="AirPods Pro 2", price=300.00, category="Electronics", itemid= 1)
    t2 = Item(image="t_CASIO Calculator.jpg",name="CASIO fx-991ES PLUS", price=59.39, category="Office Supplies", itemid= 2)
    t3 = Item(image="t_ScrewDriver.jpg",name="9 PCS Magnetic Screwdriver Set", price=27.49, category="Hardware", itemid= 3)
    t4 = Item(image="t_ApplePen.jpg",name="Apple Pen", price=319.00, category="Electronics", itemid= 4)
    t5 = Item(image="t_OpenRun.jpg",name="Shokz OpenRun Bone Conductor Headphones", price=219.00, category="Earphones", itemid= 5)
    t6 = Item(image="t_LOck.jpg",name="ORIA Combination Lock", price=14.99, category="Office Supplies", itemid= 6)
    t7 = Item(image="t_AppleCable.jpg",name="Apple USB-C to Lightning Cable", price=29.00, category="Electronics", itemid= 7)
    t8 = Item(image="t_SanDisk.jpg",name="SanDisk 2TB SSD", price=214.99, category="Storage Device", itemid= 8)

    try:
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)
        db.session.add(t4)
        db.session.add(t5)
        db.session.add(t6)
        db.session.add(t7)
        db.session.add(t8)
        db.session.commit()
    except:
        return 'There was an issue adding a tour in dbseed function'

    return 'DATA LOADED'