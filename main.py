import flask
import database
from werkzeug.exceptions import HTTPException
app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/item/<int:item_id>')
def item(item_id:int):
    return flask.render_template("item.html")

@app.route('/shop/<string:name>')
def shop(name:str):
    items = database.get_items(name)
    return flask.render_template("shop.html", items=items)

@app.route('/shop')
def shop(name:str):
    items = database.get_items()
    return flask.render_template("shop.html", items=items)

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


#run app
if __name__ == "__main__":
    app.run(host='0.0.0.0')