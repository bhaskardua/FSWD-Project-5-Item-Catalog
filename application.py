from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items, User
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('postgresql:///catalogwithusers')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        print credentials
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print result
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    print gplus_id
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != '228111374547-5rql4id9f8jjlp2tu3dotdai4npraum9.apps.googleusercontent.com':
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    print "Answer:// "
    print answer

    data = answer.json()
    print "Data:// "
    print data

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    print login_session
    # print login_session['username']
    # print login_session['picture']
    # print login_session['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # print login_session['credentials']
    # print type(login_session['credentials'])
    # print json.loads(login_session['credentials'])
    # login_session['access_token'] = json.loads(login_session['credentials'])['access_token']
    print login_session
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        # del login_session['credentials']
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You are now logged out!")
        response = make_response(render_template('logout.html', message='Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    else:

        login_session.clear()
        response = make_response(render_template('logout.html', message='Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'text/html'
        return response


# Add JSON API endpoint here
@app.route('/catalog.json')
def catalogJSON():
    categoryList = []
    categories = session.query(Category).all()
    for category in categories:
        items = session.query(Items).filter_by(category_id=category.id).all()
        itemList = [item.serialize for item in items]
        categoryList.append({
            'id': category.id,
            'name': category.name,
            'Items': itemList
            })
    return jsonify(Category=categoryList)


@app.route('/catalog/JSON/categories')
def catalogListJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[category.name for category in categories])


@app.route('/catalog/JSON/<category_name>/')
def categoryItemListJSON(category_name):
    categoryList = []
    category_id = session.query(Category).filter_by(name=category_name).one().id
    items = session.query(Items).filter_by(category_id=category_id).all()
    itemList = [item.serialize for item in items]
    categoryList.append({
        'id': category_id,
        'name': category_name,
        'Items': itemList
        })
    return jsonify(Category=categoryList)


@app.route('/catalog/JSON/<category_name>/<item_name>/')
def itemDetailsJSON(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return jsonify(item.serialize)


@app.route('/')
@app.route('/catalog/')
def catalog():
    categories = session.query(Category).all()
    return render_template('main.html', categories=categories)


# ROUTING
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/items/')
def categoryItems(category_name):
    category_id = int(session.query(Category).filter_by(name=category_name).one().id)
    items = session.query(Items).filter_by(category_id=category_id).all()
    print category_name, category_id, items
    if 'username' not in login_session:
        return render_template('public_category_items.html',
                               category_name=category_name, items=items)
    else:
        return render_template('category_items.html',
                               category_name=category_name, items=items)


@app.route('/catalog/<category_name>/<item_name>/')
def itemDetails(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    creator = getUserInfo(item.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('public_item_details.html', item_name=item_name,
                               item_description=item.description)
    else:
        return render_template('item_details.html', item_name=item_name,
                               item_description=item.description)


@app.route('/catalog/add/', methods=['GET', 'POST'])
def itemAdd():
    print "login session: "
    print login_session
    print "\n"
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        user_id = login_session['user_id']
        description = request.form['description']
        category_id = int(request.form['category'])
        category_name = session.query(Category).filter_by(id=category_id).one().name
        newItem = Items(name=name,
                        description=description,
                        category_id=category_id,
                        user_id=user_id)
        session.add(newItem)
        session.commit()
        flash("new item added!")
        print name, description, category_id
        return redirect(url_for('itemDetails',
                                category_name=category_name,
                                item_name=name))
    categories = session.query(Category).all()
    return render_template("item_add.html", categories=categories)


@app.route('/catalog/<item_name>/edit/', methods=['GET', 'POST'])
def itemEdit(item_name):
    editedItem = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this restaurant. Please create your own restaurant in order to delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = int(request.form['category'])
        session.add(editedItem)
        session.commit()
        flash("Item has been edited")
        return redirect(url_for('catalog'))
    return render_template("item_edit.html", item=editedItem,
                           categories=categories)


@app.route('/catalog/<item_name>/delete/', methods=['GET', 'POST'])
def itemDelete(item_name):
    itemToDelete = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this restaurant. Please create your own restaurant in order to delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('catalog'))
    return render_template("item_delete.html", item=itemToDelete,
                           categories=categories)


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
