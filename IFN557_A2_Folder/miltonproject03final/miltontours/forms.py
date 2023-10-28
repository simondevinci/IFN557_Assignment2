from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# form used in basket
#CAN USE AS IT IS ****************************************************************************************************
class CheckoutForm(FlaskForm):
    firstname = StringField("Your first name", validators=[InputRequired()])
    surname = StringField("Your surname", validators=[InputRequired()])
    email = StringField("Your email", validators=[InputRequired(), email()])
    phone = StringField("Your phone number", validators=[InputRequired()])
    shippingaddress = StringField("Your shipping address", validators=[InputRequired()])
    submit = SubmitField("Confirm Information and Checkout")


# comment to check update reflected#