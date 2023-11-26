from flask import Flask, render_template, request, redirect, url_for
from leapcell import Leapcell
import os
import markdown
import datetime


app = Flask(__name__)

api = Leapcell(
    os.environ.get("LEAPCELL_API_KEY"),
)

author = os.environ.get("AUTHOR", "Leapcell User")
avatar = os.environ.get("AVATAR", "https://leapcell.io/logo.png")
resource = os.environ.get("TABLE_RESOURCE")
table_id = os.environ.get("TABLE_ID")

table = api.table(repository=resource, table_id=table_id, name_type="name")


@app.route("/")
def index():
    records = table.select().query()
    params = {
        "author": author,
        "avatar": avatar,
        "posts": records,
        "timestamp_format": lambda timestamp: datetime.datetime.fromtimestamp(
            timestamp
        ).strftime("%B %d, %Y %H:%M:%S"),
    }

    return render_template("index.html", **params)


@app.route("/category/<category>")
def category(category):
    records = table.select().where(table["category"].contain(category)).query()
    params = {
        "author": author,
        "avatar": avatar,
        "posts": records,
        "category": category,
        "timestamp_format": lambda timestamp: datetime.datetime.fromtimestamp(
            timestamp
        ).strftime("%B %d, %Y %H:%M:%S"),
    }

    return render_template("index.html", **params)

@app.route("/search")
def search():
    query = request.args.get("query", "")
    records = table.search(query=query)
    params = {
        "author": author,
        "avatar": avatar,
        "posts": records,
        "query": query,
        "timestamp_format": lambda timestamp: datetime.datetime.fromtimestamp(
            timestamp
        ).strftime("%B %d, %Y %H:%M:%S"),
    }

    return render_template("index.html", **params)


@app.route("/post/<post_id>")
def post(post_id):
    record = table.get_by_id(post_id)
    markdown_html = markdown.markdown(record["content"])
    params = {
        "author": author,
        "avatar": avatar,
        "post": record,
        "markdown_html": markdown_html,
        "timestamp_format": lambda timestamp: datetime.datetime.fromtimestamp(
            timestamp
        ).strftime("%B %d, %Y %H:%M:%S"),
    }

    return render_template("post.html", **params)


if __name__ == "__main__":
    app.run(debug=True)
