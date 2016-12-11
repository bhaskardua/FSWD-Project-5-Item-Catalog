from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
def catalog():
    return "Catalog"


# ROUTING
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/items/')
def categoryItems(category_name):
    return "List of items in " + category_name.upper() + " category"


@app.route('/catalog/<category_name>/<item_name>/')
def itemDetails(category_name, item_name):
    return ("Details of item " + item_name.upper() +
            " in category " + category_name.upper())


@app.route('/catalog/<item_name>/')
def itemAdd():
    return "Page to Add new item"


@app.route('/catalog/<item_name>/edit/')
def itemEdit(item_name):
    return "Page to Edit item " + item_name.upper()


@app.route('/catalog/<item_name>/delete/')
def itemDelete(item_name):
        return "Delete item " + item_name.upper()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
