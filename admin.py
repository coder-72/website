from datetime import datetime

def items_to_list(items):
    html = ""
    for i in items:
        title = i["title"]
        date = datetime.fromtimestamp(int(i["date"])).strftime("%m/%d/%Y")
        id = i["id"]
        description = i["description"]
        html += f"""
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{id}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{id}" aria-expanded="true" aria-controls="collapse{id}">
                  {title}
                </button>
              </h2>
              <div id="collapse{id}" class="accordion-collapse collapse" aria-labelledby="heading{id}" data-bs-parent="#accordion">
                <div class="accordion-body">
                  <strong>Description:</strong> {description}<br>
                  <small class="text-muted">{date}</small>
                  <div class="my-2">
                    <form method="POST" action="{{ url_for('delete_item') }}" class="d-inline">
                        <input type="hidden" name="id" value="{{ item.id }}">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                    <a href="item/{id}" class="btn btn-primary mx-1">View</a>
                  </div>
                </div>
              </div>
            </div>
            
            """
    return html
