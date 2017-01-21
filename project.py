from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Product, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import bleach

app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    if 'username' in login_session:
        flash("You are already logged in")
        return redirect(url_for('showCategories'))
    else:
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in xrange(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)


# Log in with google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Check for forgery
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # update code to credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the'
                                            'authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
           'access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Abort if error
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'applicatopn/json'
    gplus_id = credentials.id_token['sub']

    # Abort if access token is not for intended user
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't"
                                            " match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Abort if access token is not for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not"
                                            " match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                            ' connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store token for later use
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info and store in login_session
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    login_session['provider'] = 'google'
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # Check if user exists, create new one if not
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'\
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Log out from google
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('credentials')
    if access_token is None:
        response = make_response(json.dumps('Current user '
                                            'not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        response = make_response(json.dumps('Failed to revoke token'
                                            ' for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Login with facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Check for forgery
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Request user token
    access_token = request.data
    app_id = json.loads(open('fb_client_secrets.json',
                             'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json',
                                 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb'\
          '_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s'\
        % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get info from facebook API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    token = result.split("&")[0]
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Save user info to login_session
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    # Store token in login_session in order to allow proper logout
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token
    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height'\
          '=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data['data']['url']

    # Check if user exists, if not create new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'\
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Log out from facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s'\
        % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# General disconnect method
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


# JSON APIs to view Categories information
@app.route('/JSON/')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[category.serialize for category in categories])


# JSON APIs to view single Categories Products information
@app.route('/<string:category_name>/JSON')
def categoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Product).filter_by(category_id=category.id).all()
    return jsonify(categoryProducts=[item.serialize for item in items])


# JSON APIs to view single Product information
@app.route('/<string:category_name>/<string:product_name>/JSON/')
def productJSON(category_name, product_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Product).filter_by(category_id=category.id)\
        .filter_by(name=product_name).one()
    return jsonify(Product=[item.serialize])


# Show all categories
@app.route('/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    # Return depending on logged in user or not
    if 'username' not in login_session:
        return render_template('main.html', categories=categories)
    else:
        return render_template('main_user.html', categories=categories)


# show selected category
@app.route('/<string:category_name>/')
def showCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    creator = getUserInfo(category.user_id)
    items = session.query(Product).filter_by(category_id=category.id).all()
    # Return depending on category is created by current user or not
    if 'username' not in login_session or login_session['user_id']\
            != category.user_id:
        return render_template('category.html', category=category,
                               creator=creator, items=items)
    else:
        return render_template('category_user.html', category=category,
                               creator=creator, items=items)


# Create a new category
@app.route('/new_category/', methods=['GET', 'POST'])
def newCategory():
    # Check if logged in to create new category
    if 'username' not in login_session:
        flash("You need to be logged in to add a Category. Please log in")
        return redirect('/login')

    # Check if category exists, if not create new
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=request
                                                     .form['name']).all()
        if category:
            flash('%s already exists!' % request.form['name'])
            return redirect(url_for('newCategory'))
        else:
            newCategory = Category(name=bleach.clean(request.form['name']),
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            flash('New Category: %s added successfully!' % newCategory.name)
            session.commit()
            return redirect(url_for('showCategory',
                            category_name=newCategory.name))
    else:
        return render_template('new_category.html')


# Edit a category
@app.route('/<string:category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
    editedCat = session.query(Category).filter_by(name=category_name).one()
    # Check if logged in
    if 'username' not in login_session:
        flash("You need to be logged in to edit a Category. Please log in")
        return redirect('/login')

    # Check category belongs to current user
    if editedCat.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
               "to edit this Category.'); window.history.back();}</script>"\
               "<body onload='myFunction()''>"

    # Make sure new name doesnt already exist
    if request.method == 'POST':
        if request.form['name']:
            category = session.query(Category).filter_by(name=request
                                                         .form['name']).all()
            if category:
                flash('%s already exists!' % request.form['name'])
                return redirect(url_for('editCategory',
                                        category_name=category_name))
            else:
                editedCat.name = bleach.clean(request.form['name'])
                flash('Category Successfully Edited %s' % editedCat.name)
                return redirect(url_for('showCategory',
                                        category_name=editedCat.name))
    else:
        return render_template('edit_category.html', category=editedCat)


# Delete a category
@app.route('/<string:category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    # Check user is logged in
    if 'username' not in login_session:
        flash("You need to be logged in to delete a Category. Please log in")
        return redirect('/login')

    categoryToDelete = session.query(Category).filter_by(name=category_name)\
        .one()
    items = session.query(Product).filter_by(category_id=categoryToDelete.id)
    # Check category belongs to user
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
               " to delete this Category.'); window.history.back();}</script>"\
               "<body onload='myFunction()''>"

    if request.method == 'POST':
        for item in items:
            session.delete(item)
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('delete_category.html',
                               category=categoryToDelete)


# Show a categories product
@app.route('/<string:category_name>/<string:product_name>/')
def showProduct(category_name, product_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Product).filter_by(category_id=category.id)\
        .filter_by(name=product_name).one()
    creator = getUserInfo(category.user_id)

    # Load correct page if products category belongs to user
    if 'username' not in login_session or item.user_id\
            != login_session['user_id']:
        return render_template('product.html', item=item, category=category,
                               creator=creator)
    else:
        return render_template('product_user.html', item=item,
                               category=category, creator=creator)


# Create a new product
@app.route('/<string:category_name>/new/', methods=['GET', 'POST'])
def newProduct(category_name):
    # Check user is logged in
    if 'username' not in login_session and login_session['user_id'] !=\
            category.user_id:
        flash("You need to be logged in to add a Product. Please log in")
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).one()
    # Check category belongs to current user
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
               " to add a product to this Category.'); window.history.back()"\
               ";}</script><body onload='myFunction()''>"

    # Add new product to category
    if request.method == 'POST':
        item = Product(name=bleach.clean(request.form['name']),
                       description=bleach.clean(request.form['description']),
                       price=bleach.clean(request.form['price']),
                       picture=bleach.clean(request.form['picture']),
                       category_id=category.id,
                       user_id=login_session['user_id'])
        session.add(item)
        session.commit()
        flash('New Product: %s Successfully Created' % (item.name))
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('new_product.html', category_name=category_name)


# Edit a product
@app.route('/<string:category_name>/<string:product_name>/edit',
           methods=['GET', 'POST'])
def editProduct(category_name, product_name):
    # Check user is logged in
    if 'username' not in login_session:
        flash("You need to be logged in to edit a Product. Please log in")
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).one()
    editedItem = session.query(Product).filter_by(category_id=category.id)\
        .filter_by(name=product_name).one()
    # Check product belongs to user
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
               "to edit this Product.'); window.history.back();}</script>"\
               "<body onload='myFunction()''>"

    # Edit product
    if request.method == 'POST':
        products = session.query(Product).filter_by(category_id=category.id)\
            .filter_by(name=request.form['name']).all()
        # Check if product with new name exists in category already
        if products and request.form['name'] != editedItem.name:
            flash("%s already exists!" % request.form['name'])
            return redirect(url_for('editProduct', category_name=category_name,
                                    product_name=product_name))

        # Otherwise add new info to product
        if request.form['name']:
            editedItem.name = bleach.clean(request.form['name'])
        if request.form['description']:
            editedItem.description = bleach.clean(request.form['description'])
        if request.form['price']:
            editedItem.price = bleach.clean(request.form['price'])
        if request.form['picture']:
            editedItem.picture = bleach.clean(request.form['picture'])
        session.add(editedItem)
        session.commit()
        flash('Product: %s Successfully Edited' % (editedItem.name))
        return redirect(url_for('showProduct', product_name=editedItem.name,
                                category_name=category_name))
    else:
        return render_template('edit_product.html',
                               category_name=category_name, item=editedItem)


# Delete a menu item
@app.route('/<string:category_name>/<string:product_name>/delete',
           methods=['GET', 'POST'])
def deleteProduct(category_name, product_name):
    # Check user is logged in
    if 'username' not in login_session:
        flash("You need to be logged in to delete a Product. Please log in")
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(Product).filter_by(category_id=category.id)\
        .filter_by(name=product_name).one()
    # Check product belongs to user
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
               " to delete this Product.'); window.history.back();}</script>"\
               "<body onload='myFunction()''>"

    # Delete product from database
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Product: %s Successfully Deleted' % product_name)
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('delete_product.html', item=itemToDelete,
                               category=category)


# Get user ID if exists
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Get users info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# create a new user in database
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
