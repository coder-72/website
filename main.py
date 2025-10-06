import flask
import admin
import database
from werkzeug.exceptions import HTTPException
app = flask.Flask(__name__)


@app.route('/')
def index():
    html = database.items_to_cards(database.get_new(lim=3))
    return flask.render_template("index.html", products = html)

@app.route('/item/<int:item_id>')
def item(item_id:int):
    html = database.item_to_page(database.item(item_id))
    return flask.render_template("item.html", product=html)

@app.route('/shop/<string:name>')
def shop(name:str):
    if name.lower() == "new":
        return flask.render_template("shop.html", items=database.items_to_cards(database.get_new()), title="New Arrivals", subtitle="See the latest pieces here!", background_url="/assets/images/download.png")
    html = ""
    title = ""
    description = ""
    image = ""
    t = ""
    match name:
        case "other":
            title = "other"
            description = "jewelry"
            image = "assets/download.png"
            t="other"
        case "necklaces":
            title = "necklace"
            description = "necklace"
            image = "assets/download.png"
            t = "necklace"
        case "bracelets":
            title = "bracelet"
            description = "bracelet"
            image = "assets/download.png"
            t = "bracelet"
        case _:
            title = "other"
            description = "other"
            image = "assets/download.png"
            t = "other"
    items = database.get_items(title)
    html += database.items_to_cards(items)
    return flask.render_template("shop.html", items=html, title=title, subtitle=description, background_url=flask.url_for("static", filename=image))

@app.route('/shop')
def shop_all():
    items = database.items_to_cards(database.get_all())
    return flask.render_template("shop.html", items=items, title="shop", description="shop")


@app.errorhandler(Exception)
def error_handler(error):


    # check if http error if not makes it an internal server error code (500)
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return flask.render_template('error.html', error=error, code=error_code, ), error_code

@app.route('/about')
def about():
    return flask.render_template("about.html")

@app.route('/admin/delete', methods=['POST'])
def delete_item():
    id = flask.request.form.get("id")
    database.delete(id)
    return flask.redirect(flask.url_for("dashboard"))

@app.route('/admin/add', methods=['GET', 'POST'])
def add_item():
    if flask.request.method == "GET":
        return flask.render_template("add.html")
    else:
        form = flask.request.form
        title = form.get("title")
        description = form.get("description")
        image = flask.request.files.get("image").read()
        t = form.get("type")
        price = form.get("price")
        priority = form.get("priority")
        related = str([form.get("related1"), form.get("related2"), form.get("related3"), form.get("related4")])
        database.add_item(title, description, float(price) ,str(related), float(priority),  image, str(t))
        return flask.redirect(flask.url_for("dashboard"))


@app.route('/admin')
def dashboard():
    html = admin.items_to_list(database.get_all())
    return flask.render_template("admin dashboard.html", html=html)

@app.route('/contact')
def contact():
    return flask.render_template("contact.html")

#run app
if __name__ == "__main__":
    app.run(host='0.0.0.0')