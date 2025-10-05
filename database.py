import sqlite3
from datetime import datetime, timezone
import base64


DB_PATH = "database.db"


def placeholder():
    with open('static/assets/placeholder.png', 'rb') as file:
        return file.read()


placeholder = placeholder()

def add_post(title, description, t:int = 1, priority:int = 0,  image = placeholder)->None:
    now = datetime.now(timezone.utc)
    unix_timestamp = int(now.timestamp())

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()



    # insert post info into sql table (posts)
    cursor.execute("INSERT INTO posts (title,description, image, type, date, priority) VALUES (?, ?, ?, ?, ?, ?);",
                   (title, description, image, t, unix_timestamp, priority))

    # commit data before closing connection
    conn.commit()
    cursor.close()
    conn.close()

def get_posts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # execute sql and get results
    cursor.execute("SELECT title, description, image, type FROM posts ORDER BY Priority DESC, date DESC;")
    posts = cursor.fetchall()

    # close cursor and connection
    cursor.close()
    conn.close()

    html = ""
    for post in posts:
        title = post["title"]
        description = post["description"]
        image = base64.b64encode(post["image"]).decode("utf-8")
        if post['type'] == 1:
            html += f"""
        <div class="row gx-0 mb-4 mb-lg-5 align-items-center">
                <div class="col-xl-8 col-lg-7"><img class="img-fluid mb-3 mb-lg-0" src="data:image/jpeg;base64,{image}" alt="..." /></div>
                <div class="col-xl-4 col-lg-5">
                    <div class="featured-text text-center text-lg-left">
                            <h4>{title}</h4>
                            <p class="text-black-50 mb-0">{description}</p>
                    </div>
                </div>
        </div>
        """
        elif post['type'] == 2:
            html += f"""
                <div class="row gx-0 mb-4 mb-lg-5 align-items-center">
                    <div class="col-xl-4 col-lg-5">
                        <div class="featured-text text-center text-lg-left">
                            <h4>{title}</h4>
                            <p class="text-black-50 mb-0">{description}</p>
                        </div>
                    </div>
                    <div class="col-xl-8 col-lg-7"><img class="img-fluid mb-3 mb-lg-0" src="data:image/jpeg;base64,{image}" alt="..." /></div>
                </div>
                """
        elif post['type'] == 3:
            html += f"""
             <div class="row gx-0 mb-5 mb-lg-0 justify-content-center">
                    <div class="col-lg-6"><img class="img-fluid" src="data:image/jpeg;base64,{image}" alt="..." /></div>
                    <div class="col-lg-6">
                        <div class="bg-black text-center h-100 project">
                            <div class="d-flex h-100">
                                <div class="project-text w-100 my-auto text-center text-lg-left">
                                    <h4 class="text-white">{title}</h4>
                                    <p class="mb-0 text-white-50">{description}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            """
        elif post['type'] == 4:
            html += f"""
            <div class="row gx-0 justify-content-center">
                    <div class="col-lg-6"><img class="img-fluid" src="data:image/jpeg;base64,{image}" alt="..." /></div>
                    <div class="col-lg-6 order-lg-first">
                        <div class="bg-black text-center h-100 project">
                            <div class="d-flex h-100">
                                <div class="project-text w-100 my-auto text-center text-lg-right">
                                    <h4 class="text-white">{title}</h4>
                                    <p class="mb-0 text-white-50">{description}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            """
        else:
            pass
    return html

