from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from send_mail import send_mail
import psycopg2
import re # regular expression
import logging
# import requests # - use from flask import request


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev': # for development
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://<user>:<pw>@localhost/<dbname>" # local database which will hold all the tables
else: # for production
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "<database_uri>" # for production taken from "heroku config --app <appname>"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Form Class/Model with fields
class Form(db.Model): #SQLAlchemy.Model
    id = db.Column(db.Integer, primary_key=True) # id will automatically be included without neeing to be specified in POST 
    name = db.Column(db.String(75), unique=False)
    email = db.Column(db.String(200))
    message = db.Column(db.String(500))

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    
class FormSchema(ma.Schema): #Marshmallow.Schema
    class Meta:
        fields = ('id', 'name', 'email', 'message')

# Init form schema
form_schema = FormSchema() #strict=True
forms_schema = FormSchema(many=True) #strict=True

# Product Class/Model with fields
class Product(db.Model): #SQLAlchemy.Model
    id = db.Column(db.Integer, primary_key=True) # id will automatically be included without neeing to be specified in POST 
    name = db.Column(db.String(200)) # unique=True
    category = db.Column(db.String(200))
    size_variation = db.Column(db.Boolean)
    colour_variation = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    additional_description = db.Column(db.String(6000))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    Image_1 = db.Column(db.String(500))
    Image_2 = db.Column(db.String(500))
    Image_3 = db.Column(db.String(500))
    Image_4 = db.Column(db.String(500))
    Image_5 = db.Column(db.String(500))
    Image_6 = db.Column(db.String(500))
    Size_chart = db.Column(db.String(500))
    Supplier = db.Column(db.String(200))
    active = db.Column(db.Boolean)
    Original_URL = db.Column(db.String(500))

    def __init__(self, name, category, size_variation, colour_variation, description, additional_description, price, qty, Image_1, Image_2, Image_3, Image_4, Image_5, Image_6, Size_chart, Supplier, active, Original_URL):
        self.name = name
        self.category = category
        self.size_variation = size_variation
        self.colour_variation = colour_variation
        self.description = description
        self.additional_description = additional_description
        self.price = price
        self.qty = qty
        self.Image_1 = Image_1
        self.Image_2 = Image_2
        self.Image_3 = Image_3
        self.Image_4 = Image_4
        self.Image_5 = Image_5
        self.Image_6 = Image_6
        self.Size_chart = Size_chart
        self.Supplier = Supplier
        self.active = active
        self.Original_URL = Original_URL

# what we want to show from get requests?
class ProductSchema(ma.Schema): #Marshmallow.Schema
    class Meta:
        fields = ('id', 'name', 'category', 'size_variation', 'colour_variation', 'description', 'additional_description', 'price', 'qty', 'Image_1', 'Image_2', 'Image_3', 'Image_4', 'Image_5', 'Image_6', 'Size_chart', 'Supplier', 'active', 'Original_URL')

# Product schema
product_schema = ProductSchema() #strict=True
products_schema = ProductSchema(many=True) #strict=True


# logging
# create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log.log", 
                    level=logging.DEBUG, 
                    format=LOG_FORMAT) 
logger = logging.getLogger() # logger without a name (root logger)

print(logger.level)

# create a product
# @app.route('/product', methods=['POST'])
# def add_product():
#     logger.info("add_product()")
#     name = request.json['name']
#     logger.debug("added name success")

#     category = request.json['category']
#     size_variation = request.json['size_variation']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']
#     active = request.json['active']

#     new_product = Product(name, category, size_variation, description, price, qty, active)

#     logger.debug("add product to db")
#     db.session.add(new_product)

#     logger.debug("commit product to db")
#     db.session.commit()

#     logger.debug("return json of new product added")
#     return product_schema.jsonify(new_product)

# get all products
@app.route('/product', methods=['GET'])
def get_products():
    logger.info("get_products()")
    all_products = Product.query.all() # gets all the products
    result = products_schema.dump(all_products)
    logger.debug("# return json result") 
    return result # no need for result.data # no need for jsonify(result) this time because being in python

# get all categories (active)
@app.route('/categories', methods=['GET'])
def get_categories():
    all_products = get_products()
    active = [product for product in all_products if product['active'] == True]

    categories = []
    for product in active:
        category = product['category'].split(",")
        categories.extend(category) # similar to append 
    categories = set(categories)
    return categories
# get single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id): 
    product = Product.query.get(id) # gets all the products
    return product_schema.jsonify(product) # no need for result.data

# update a product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#     product = Product.query.get(id)
    
#     # get all fields from request
#     name = request.json['name']
#     category = request.json['category']
#     size_variation = request.json['size_variation']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']
#     active = request.json['active']

#     product.name = name
#     product.category = category
#     product.size_variation = size_variation
#     product.description = description
#     product.price = price
#     product.qty = qty
#     product.active = active

#     db.session.commit()

#     return product_schema.jsonify(product)


# delete single product
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id): 
#     product = Product.query.get(id)
#     db.session.delete(product)
#     db.session.commit()
#     return product_schema.jsonify(product) # no need for result.data

# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home.html')

@app.route('/', methods=['GET'])
def store():
    categories = get_categories()
    products = get_products()
    return render_template('store.html', categories = categories, products = products)

@app.route('/products', methods=['GET'])
def products_page():
    products = get_products()
    display = "none"
    # list comprehension
    active = [product for product in products if product['active'] == True]
    print(len(active)) # how many active products
    categories = get_categories()
    return render_template('products.html', products = active, display = display, categories = categories)

@app.route('/products/sort=price', methods=['GET'])
def sort_price_low_to_high():
    products = get_products()
    active = [product for product in products if product['active'] == True]
    products = sorted(active, key=lambda value: value['price']) 
    display = "initial"

    return render_template('products.html', products = products, display = display)

@app.route('/products/sort=-price', methods=['GET'])
def sort_price_high_to_low():
    products = get_products()
    active = [product for product in products if product['active'] == True]
    products = sorted(active, key=lambda value: value['price'], reverse=True) 
    display = "initial"        
    return render_template('products.html', products = products, display = display)

@app.route('/products/<name>/<id>', methods=['GET'])
def item(name, id):
    product = Product.query.get(id)
    print(product.size_variation)

    categories = get_categories()

    custom_colours = product.colour_variation
    

    # string.replace(old, new, count)
    custom_colours = custom_colours.replace(",", "|")

    print(custom_colours)

    return render_template('item.html', product = product, image_url = product.Image_1, Image_2 = product.Image_2, product_name = product.name, price = product.price, description = product.description, size_variation = product.size_variation, id = product.id, categories = categories, custom_colours = custom_colours)

@app.route('/collections', methods=['GET'])
def collections():
    products = get_products()
    logger.debug("# get_products() success test") 
    active = [product for product in products if product['active'] == True]
    categories = get_categories()
    return render_template('collections.html', products = active, categories = categories)

@app.route('/collections/<category>', methods=['GET'])
def specific_collection(category):
    products = get_products()
    active = [product for product in products if product['active'] == True]

    product_with_category = []
    for product in active: 
        if category in product['category']:
            product_with_category.append(product)

    categories = get_categories()

    return render_template("collection.html", category = category, categories = categories, product_with_category = product_with_category)

    

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    products = get_products()
    display = "none"
    # list comprehension
    active = [product for product in products if product['active'] == True]
    print(len(active)) # how many active products
    categories = get_categories()

    logger.info("submit()")
    if request.method == "POST":
        fullname = request.form["fullname"].strip()
        email = request.form["email"].strip()
        message = request.form["message"].strip()
    
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # for email validation    
        if fullname == "" and email == "" and message == "":
            return render_template('store.html', categories = categories, products = products, msg="Message not sent!", message="Please fill all the required fields")
        elif fullname == "":
            return render_template('store.html', categories = categories, products = products, msg="Message not sent!", message="Please fill in your name")
        elif email == "":
            return render_template('store.html', categories = categories, products = products, msg="Message not sent!", message="Please fill in your email")
        elif re.search(regex,email) == None: # re.search returns None if email does not match the regex requirements
            logger.warning(f"# email {email} was not valid ")
            return render_template('store.html', categories = categories, products = products, msg="Message not sent!", message="Please fill in a valid email")
        elif message == "":
            return render_template('store.html', categories = categories, products = products, msg="Message not sent!", message="Please fill in your message")
        else:
            # send to database
            new_form = Form(fullname, email, message)
            db.session.add(new_form)
            db.session.commit()

            # send to email
            send_mail(fullname, email, message)
            
            # if every field filled, render success.html  
            logger.debug("# form successfully filled") 
            return render_template('store.html', categories = categories, products = products, msg="Success", message_success ="Your message was sent!")

if __name__ == "__main__":
    app.run(debug=False, port=5000) # Running a Flask app in debug mode may allow an attacker to run arbitrary code through the Werkzeug debugger.