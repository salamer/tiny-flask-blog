from flask import Flask, render_template, request, redirect, url_for
from leapcell import Leapcell
import os
import markdown


app = Flask(__name__)

api = Leapcell(
    os.environ.get("LEAPCELL_API_KEY"),
)
table = api.table("salamer/flask-blog", "tbl1723292788542648320", name_type="name")
author = os.environ.get("AUTHOR", "Jedi")
avatar = os.environ.get("AVATAR", "https://leapcell.io/logo.png")


@app.route("/")
def index():
    records = table.select().query()
    params = {
        "author": author,
        "avatar": avatar,
        "posts": records,
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
    }

    return render_template("post.html", **params)


if __name__ == "__main__":
    app.run(debug=True)