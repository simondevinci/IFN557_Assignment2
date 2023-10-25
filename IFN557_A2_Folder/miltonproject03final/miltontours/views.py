from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Order, Item
from datetime import datetime
from .forms import CheckoutForm
from . import db

# ADD DATABASE PART HERE
#I ADDED IN MOST OF THE INFORMATION BUT HAVENT ADD DESCRIPTION, YOU CAN ADD IT HERE. JUST REMEMBER TO ADD THE DESCRIPTION VARIABLE INTO THE CONSTRUCTOR IN THE MODEL.PY
#JUST NEED TO ADD IN DESCRIPTIONS THE 
t1 = Item(image="t_AirPods.jpg",name="AirPods Pro 2", price=300.00, category="Electronics", itemid= 1,
          itemdescription="to", extradetails="")
t2 = Item(image="t_CASIO Calculator.jpg",name="CASIO fx-991ES PLUS", price=59.39, category="Office Supplies", itemid= 2,
          itemdescription="", extradetails="")
t3 = Item(image="t_ScrewDriver.jpg",name="9 PCS Magnetic Screwdriver Set", price=27.49, category="Hardware", itemid= 3,
          itemdescription="", extradetails="")
t4 = Item(image="t_ApplePen.jpg",name="Apple Pen", price=319.00, category="Electronics", itemid= 4,
          itemdescription="", extradetails="")
t5 = Item(image="t_OpenRun.jpg",name="Shokz OpenRun Bone Conductor Headphones", price=219.00, category="Earphones", itemid= 5,
          itemdescription="", extradetails="")
t6 = Item(image="t_LOck.jpg",name="ORIA Combination Lock", price=14.99, category="Office Supplies", itemid= 6,
          itemdescription="", extradetails="")
t7 = Item(image="t_AppleCable.jpg",name="Apple USB-C to Lightning Cable", price=29.00, category="Electronics", itemid= 7,
          itemdescription="", extradetails="")
t8 = Item(image="t_SanDisk.jpg",name="SanDisk 2TB SSD", price=214.99, category="Storage Device", itemid= 8,
          itemdescription="", extradetails="")

# once done to reflect in admin
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
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now(), item = '')
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

    return render_template('categories.html', items = items)

#ADDED A BLUEPRINT FOR THE ITEMDETAILS PAGE # items/1 - for airpods etc. 
@main_bp.route('/items/<int:itemid>')
def itemdetails(itemid):
    item = Item.query.filter(Item.id == itemid)
    return render_template('itemdetails.html', item = item)
