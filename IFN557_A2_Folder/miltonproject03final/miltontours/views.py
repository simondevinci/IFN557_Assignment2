from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import City, Tour, Order, Item, Category
from datetime import datetime
from .forms import CheckoutForm
from . import db

# ADD DATABASE PART HERE


AirPodsPro = Item("AirPods.jpg","AirPods Pro 2", 300.00, "Electronics")
CASIOCalculator = Item("CASIO Calculator.jpg","CASIO fx-991ES PLUS", 59.39, "Office Supplies")
Screwdriver = Item("ScrewDriver.jpg","9 PCS Magnetic Screwdriver Set", 27.49, "Hardware")
ApplePen = Item("ApplePen.jpg","Apple Pen", 319.00, "Electronics")
ShokzOpenRun = Item("OpenRun.jpg","Shokz OpenRun Bone Conductor Headphones", 219.00, "Earphones")
Lock = Item("LOck.jpg","ORIA Combination Lock", 14.99, "Office Supplies")
AppleCable = Item("AppleCable.jpg","Apple USB-C to Lightning Cable", 29.00, "Electronics")
SanDisk = Item("SanDisk.jpg","SanDisk 2TB SSD", 214.99, "Storage Device")


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    #REPLACE THE CITIES PART**********************************************************************************
    items = Item.query.order_by(Item.name).all()
    return render_template('index.html', items = items)


#DISPLAY ITEM CATEGORY IF IT EXIST *****************************************************************************
@main_bp.route('/items/<string:itemcategory>')
def itembycategory(itemcategory):
    items_category = Item.query.filter(Item.item_category==itemcategory)
    #SENDING A ARRAY OF ITEMS WITH THE CATEGORY MATCHING THE SPECIFIED CATEGORY
    return render_template('items.html', category = items_category)

# Referred to as "Basket" to the user
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
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now(), item = Item())
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
        for item in order.item:
            total_price = total_price + item.price
    
    # are we adding an item?
    if item_id is not None and order is not None:
        item = Item.query.get(item_id)
        if item not in order.item:
            try:
                order.item.append(item)
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
@main_bp.route('/items')
def search():

    search = request.args.get('search')

    search = '%{}%'.format(search) # substrings will match

    items = Item.query.filter(Item.description.like(search)).all()

    return render_template('items.html', items = items)


# CREATE A BLUEPRINT FOR THE ITEMDETAILPAGE HERE #######################################################################################