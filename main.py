import flask
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
    items = database.get_items(name)
    html += database.items_to_cards(items)
    match name:
        case "other":
            title = "other"
            description = "jewelry"
            image = "assets/download.png"
        case "necklaces":
            title = "necklace"
            description = "necklace"
            image = "assets/download.png"
        case "bracelets":
            title = "bracelet"
            description = "bracelet"
            image = "assets/download.png"
        case _:
            title = "other"
            description = "other"
            image = "assets/download.png"
    return flask.render_template("shop.html", items=html, title=title, subtitle=description, background_url=image)

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

#run app
if __name__ == "__main__":
    app.run(host='0.0.0.0')