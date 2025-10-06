import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
import base64


DB_PATH = "database.db"
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_B3mrRSV1PFgk@ep-cool-waterfall-abaavfkt-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")


def add_item(title:str, description:str,price:float ,related:str, priority:int,  image, t:str = "other")->None:
    now = datetime.now(timezone.utc)
    unix_timestamp = int(now.timestamp())

    cursor = conn.cursor(cursor_factory=RealDictCursor)





    # insert post info into sql table (posts)
    cursor.execute("INSERT INTO items (title, description, price, related, priority, image, date, type) VALUES (?, ?, ?, ?, ?, ?, ?,?)",(title, description, price, related, priority, image, unix_timestamp, t.lower()))

    # commit data before closing connection
    conn.commit()
    cursor.close()

def get_items(t):

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # execute sql and get results
    cursor.execute("SELECT * FROM items WHERE type = ? ORDER BY priority DESC, date DESC;", [t.lower()])
    items = cursor.fetchall()

    # close cursor and connection
    cursor.close()


    return items

def get_all():

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # execute sql and get results
    cursor.execute("SELECT * FROM items ORDER BY priority DESC, date DESC;")
    items = cursor.fetchall()

    # close cursor and connection
    cursor.close()

    return items

def item(id:int):

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # execute sql and get results
    cursor.execute("SELECT * FROM items Where id = ?;", [id])
    info =  cursor.fetchone()

    # close cursor and connection
    cursor.close()
    return info

def item_to_card(i):
    id = i["id"]
    title = i["title"]
    description = i["description"]
    price = i["price"]
    related = i["related"]
    image = i["image"]
    date = datetime.fromtimestamp(int(i["date"])).strftime("%m/%d/%Y")
    html = f"""
                <div class="col mb-5">
                                <div class="card h-100">
                                    <!-- Product image-->
                                    <img class="card-img-top" src="{{ url_for(('static'), filename='assets/download.png')}}" alt="..." />
                                    <!-- Product details-->
                                    <div class="card-body p-4">
                                        <div class="text-center">
                                            <!-- Product name-->
                                            <h5 class="fw-bolder">{title}</h5>
                                            <!-- Product reviews-->
                                            <!-- Product price-->
                                            £{price:.2f}
                                        </div>
                                    </div>
                                    <!-- Product actions-->
                                    <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                        <div class="text-center"><a class="btn btn-outline-dark mt-auto" href="/item/{id}">View item</a></div>
                                    </div>
                                </div>
                            </div>
                """
    return html

def item_to_page(i):
    id = i["id"]
    title = i["title"]
    description = i["description"]
    price = i["price"]
    related = i["related"]
    image = i["image"]
    date = datetime.fromtimestamp(int(i["date"])).strftime("%m/%d/%Y")
    r_html = ""
    for r in related:
        r_html += item_to_card(item(id))


    html = f"""
        <section class="py-5">
            <div class="container px-4 px-lg-5 my-5">
                <div class="row gx-4 gx-lg-5 align-items-center">
                    <div class="col-md-6"><img class="card-img-top mb-5 mb-md-0" src="https://dummyimage.com/600x700/dee2e6/6c757d.jpg" alt="..." /></div>
                    <div class="col-md-6">
                        <div class="small mb-1">ID: {id}</div>
                        <h1 class="display-5 fw-bolder">{title}</h1>
                        <div class="fs-5 mb-5">
                            <span>£{price:.2f}</span>
                        </div>
                        <p class="lead">{description}</p>
                        <div class="d-flex">
                            <input class="form-control text-center me-3" id="inputQuantity" type="num" value="1" style="max-width: 3rem" />
                            <button class="btn btn-outline-dark flex-shrink-0" type="button">
                                <i class="bi-cart-fill me-1"></i>
                                Add to cart
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="py-5 bg-light">
            <div class="container px-4 px-lg-5 mt-5">
                <h2 class="fw-bolder mb-4">Related products</h2>
                <div class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
                    {r_html}
                </div>
            </div>
        </section>
"""
    return html

def get_bits():
    with open("static/assets/download.png", "rb") as f:
        return f.read()

def items_to_cards(items):
    html = ""
    for i in items:
        html += item_to_card(i)
    return html

def get_new(lim=5):

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # execute sql and get results
    cursor.execute("SELECT * FROM items ORDER BY date DESC LIMIT ?", [lim])
    items = cursor.fetchall()

    # close cursor and connection
    cursor.close()

    return items

add_item("test title", "test description description would go here", 10.001, "1,2,3,4", 1, get_bits(), )
