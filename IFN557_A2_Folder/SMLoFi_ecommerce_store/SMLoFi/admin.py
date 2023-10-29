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
from .models import Order, Item, Category
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
#I ADDED IN MOST OF THE INFORMATION BUT HAVENT ADD DESCRIPTION, YOU CAN ADD IT HERE. JUST REMEMBER TO ADD THE DESCRIPTION VARIABLE INTO THE CONSTRUCTOR IN THE MODEL.PY
#JUST NEED TO ADD IN DESCRIPTIONS 

      #adding categories into table
      c1 = Category(name= "Electronics", description="Browse through our options of the latest and greatest home electronics to upgrade your tech devices")
      c2 = Category(name= "Office Supplies", description="Useful tools when specifically made for an IT professional in mind")
      c3 = Category(name= "Hardware", description="Need to fix something? Get our DIY tools that come in handy when you're in a bind")
      c4 = Category(name= "Earphones", description="Our selection of the best in ear headphones around")
      c5 = Category(name= "Storage Device", description="Not enough storage on your device? We got you caovered")

      try:
            db.session.add(c1)
            db.session.add(c2)
            db.session.add(c3)
            db.session.add(c4)
            db.session.add(c5)
            db.session.commit()
            'Added Categories'
      except:
            'There was an issue adding categories in dbseed function'


      # ADD ITEM INTO TABLE
      t1 = Item(itemcategoryid = c1.id, 
          name = 'AirPods Pro 2', 
          description = 'The Apple AirPods Pro (2nd generation) modestly improve upon the first-generation AirPods Pro and feature the same iconic look.', 
          image = 't_AirPods.jpg', 
          price = 300.00, 
          extra_details = 'IP54 dust, sweat and water resistant for AirPods Pro and MagSafe Charging Case.6',
      t2 = Item(itemcategoryid = c2.id, 
          name = 'CASIO fx-991ES PLUS', 
          description = 'Really good form factor. Has all of the functions you need and then some. The case has unit conversions on the inside, which is neat.', 
          image = 't_CASIO Calsulator.jpg', 
          price = 59.39, 
          extra_details = 'Product features: Non Programmable, Non Graphing, Number of Functions : 417',
      t3 = Item(itemcategoryid = c3.id, 
          name = '9 PCS Magnetic Screwdriver Set', 
          description = 'This screwdriver set features non-slip soft grips. Rubber-based ergonomically non-skid and soft-grip handle for improved control and comfort.', 
          image = 't_ScrewDriver.jpg', 
          price = 27.49, 
          extra_details = '4 Phillips + 5 Flat Head Screwdrivers + Storage Case.',
      t4 = Item(itemcategoryid = c1.id, 
          name = 'Apple Pen', 
          description = 'Apple Pencil (2nd generation) delivers pixel-perfect precision and industry-leading low latency, making it great for drawing, sketching, colouring, taking notes, marking up PDFs and more. And its as easy and natural to use as a pencil.', 
          image = 't_ApplePen.jpg', 
          price = 319.00, 
          extra_details = 'Length: 6.53 inches (166 mm), Diameter: 0.35 inch (8.9 mm), Weight: 0.73 ounce (20.7 grams), Connections, Bluetooth, Other Features, Magnetically attaches and pairs',
      t5 = Item(itemcategoryid = c4.id, 
          name = 'Shokz OpenRun Bone Conductor Headphones', 
          description = 'Top selling model of Shokz. Now they have been updated with a quick-charge feature and re-named as OpenRun. A 10-minute quick charge gives you 1.5 hours of listening time so you can get on-the-go fast!', 
          image = 't_OpenRun.jpg', 
          price = 219.00, 
          extra_details = 'IP67 Waterproof (Not for swimming), Lightweight + ComfortableLightweight + Comfortable, 8-Hour Battery Life + Quick Charge, 2-Year Warranty',
      t6 = Item(itemcategoryid = c2.id, 
          name = 'ORIA Combination Lock', 
          description = 'Excellent design with Anti-rust, it is weather proof,light weight, fits through the holes of a lot of suitcases.', 
          image = 't_LOck.jpg', 
          price = 14.99, 
          extra_details = 'Lock Type: Combination Lock Item Dimensions: LxWxH 5.12 x 3.94 x 1.97 inches Material: Steel and Zinc',
      t7 = Item(itemcategoryid = c1.id, 
          name = 'Apple USB-C to Lightning Cable', 
          description ='Connect your device with Lightning connector to your USB-C  Thunderbolt 3 (USB-C)enabled device for syncing and charging, or to your USB-C enabled iPad for charging.', 
          image = 't_AppleCable.jpg', 
          price = 29.00, 
          extra_details = 'Length: 1m',
      t8 = Item(itemcategoryid = c5.id, 
          name = 'SanDisk 2TB SSD', 
          description = 'From the brand trusted by professional photographers worldwide, the SanDisk Extreme PRO Portable SSD provides powerful solid state performance in a rugged, dependable storage solution. Nearly 2x as fast as our previous generation!', 
          image = 't_SanDisk.jpg', 
          price = 214.99, 
          extra_details = 'Capacity: 1TB/ 2TB, Interface: USB 3.2 Gen 2 x2, Connector: USB-C, Compatibility: USB 3.2 Gen 2x2 (20Gb/s), USB 3.0, USB 2.0, Dimensions (L x W x H): 110.26mm x 57.34mm x 10.22mm, Sequential Read Performance: 2000MB/s, Sequential Write Performance: 2000MB/s',

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
            'Added Items'
      except:
            'There was an issue adding a items in dbseed function'

      