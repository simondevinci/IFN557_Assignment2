from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Order, Item, Category
from datetime import datetime
from .forms import CheckoutForm
from . import db

#adding categories into table
c1 = Category(name= "Electronics", description="")
c2 = Category(name= "Office Supplies", description="")
c3 = Category(name= "Hardware", description="")
c4 = Category(name= "Earphones", description="")
c5 = Category(name= "Storage Device", description="")

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
          description = '', 
          image = 't_AirPods.jpg', 
          price = 300.00, 
          extra_details = '')
t2 = Item(itemcategoryid = c2.id, 
          name = 'CASIO fx-991ES PLUS', 
          description = '', 
          image = 't_CASIO Calsulator.jpg', 
          price = 59.39, 
          extra_details = '')
t3 = Item(itemcategoryid = c3.id, 
          name = '9 PCS Magnetic Screwdriver Set', 
          description = '', 
          image = 't_ScrewDriver.jpg', 
          price = 27.49, 
          extra_details = '')
t4 = Item(itemcategoryid = c1.id, 
          name = 'Apple Pen', 
          description = '', 
          image = 't_ApplePen.jpg', 
          price = 319.00, 
          extra_details = '')
t5 = Item(itemcategoryid = c4.id, 
          name = 'Shokz OpenRun Bone Conductor Headphones', 
          description = '', 
          image = 't_OpenRun.jpg', 
          price = 219.00, 
          extra_details = '')
t6 = Item(itemcategoryid = c2.id, 
          name = 'ORIA Combination Lock', 
          description = '', 
          image = 't_LOck.jpg', 
          price = 14.99, 
          extra_details = '')
t7 = Item(itemcategoryid = c1.id, 
          name = 'Apple USB-C to Lightning Cable', 
          description = '', 
          image = 't_AppleCable.jpg', 
          price = 29.00, 
          extra_details = '')
t8 = Item(itemcategoryid = c5.id, 
          name = 'SanDisk 2TB SSD', 
          description = '', 
          image = 't_SanDisk.jpg', 
          price = 214.99, 
          extra_details = '')

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

# once done to reflect in admin
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    #REPLACE THE CITIES PART**********************************************************************************
    items = Item.query.order_by(Item.name).all()
    return render_template('index.html', items = items)


#DISPLAY ITEM CATEGORY IF IT EXIST *****************************************************************************
@main_bp.route('/itembycategory/<int:category_id>')
def itembycategory(category_id):
    items_category = Item.query.filter(Item.item_category_id==category_id)
    #SENDING A ARRAY OF ITEMS WITH THE CATEGORY MATCHING THE SPECIFIED CATEGORY
    return render_template('categories.html', items = items_category)


# Referred to as "Cart" to the user
@main_bp.route('/order', methods=['POST','GET'])
def order():
    item_id = request.values.get('item_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', total_cost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    total_price = 0
    if order is not None:
        for item in order.items:
            total_price = total_price + item.price
    
    # are we adding an item?
    if item_id is not None and order is not None:
        item = Item.query.get(item_id)
        if item not in order.items:
            try:
                order.items.append(item)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, total_price=total_price)

#************************************************************************************************************
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        item_to_delete = Item.query.get(id)
        try:
            order.item.remove(item_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket 
#CAN USE THIS AS IT IS ***************************************************************************************************
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            order.shippingdetails = form.shippingaddress.data
            totalcost = 0
            for items in order.item:
                totalcost = totalcost + items.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our awesome team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)

#SHOWCASE ITEMS BY CATEGORY ****************************************************************************************************
@main_bp.route('/search')
def search():

    search = request.args.get('search')

    search = '%{}%'.format(search) # substrings will match

    items = Item.query.filter(Item.description.like(search)).all()

    return render_template('categories.html', items = items)

#ADDED A BLUEPRINT FOR THE ITEMDETAILS PAGE # items/1 - for airpods etc. 
@main_bp.route('/itemdetails/<int:itemid>')
def itemdetails(itemid):
    item = Item.query.filter(Item.id == itemid)
    return render_template('itemdetails.html', item = item)
