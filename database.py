import sqlite3
from datetime import datetime, timezone
import base64


DB_PATH = "database.db"


def add_item(title:str, description:str,price:float ,related:str, priority:int,  image, t:str = "other")->None:
    now = datetime.now(timezone.utc)
    unix_timestamp = int(now.timestamp())

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()




    # insert post info into sql table (posts)
    cursor.execute("INSERT INTO items (title, description, price, related, priority, image, date, type) VALUES (?, ?, ?, ?, ?, ?, ?,?)",(title, description, price, related, priority, image, unix_timestamp, t.lower()))

    # commit data before closing connection
    conn.commit()
    cursor.close()
    conn.close()

def get_items(t):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # execute sql and get results
    cursor.execute("SELECT * FROM items WHERE type = ? ORDER BY priority DESC, date DESC;", [t.lower()])
    items = cursor.fetchall()

    # close cursor and connection
    cursor.close()
    conn.close()

    html = ""
    for item in items:
        id = item["id"]
        title = item["title"]
        description = item["description"]
        price = item["price"]
        image = item["image"]
        date = datetime.fromtimestamp(int(item["date"])).strftime("%m/%d/%Y")
        #TODO: fix image
        html += f"""
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
                                    <div class="d-flex justify-content-center small text-warning mb-2">
                                        <div class="bi-star-fill"></div>
                                        <div class="bi-star-fill"></div>
                                        <div class="bi-star-fill"></div>
                                        <div class="bi-star-fill"></div>
                                        <div class="bi-star-fill"></div>
                                    </div>
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

def get_bits():
    with open("static/assets/download.png", "rb") as f:
        return f.read()

#add_item("test title", "test description desctription would go here", 10.001, "1,2,3,4", 1, get_bits(), )
