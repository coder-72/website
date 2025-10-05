import flask
import database

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html", posts = database.get_posts())

#run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)