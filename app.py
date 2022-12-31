from flask import Flask, request
import numpy as np
import pandas as pd
from flask import Flask, request, redirect, url_for, session, json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["SECRET_KEY"] = "the quick brown fox jumps over the lazy   dog"

app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(
    app,
    # resources={
    #     r"/api/*": {
    #         "origins": "*",
    #     }
    # },
)
import sqlite3 as sql
from flask_restx import Api, Resource

api = Api(app)

conn = sql.connect("database.db")


conn.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR(50) NOT NULL,password VARCHAR(50) NOT NULL,email VARCHAR(50) NOT NULL)"
)


app = Flask(__name__)


@app.route("/")
def main():
    return "OKAY"


def get_large_url(text):
    replacement = text.split("/")[-2].replace("s", "l")
    replacement = text.split("/")[-2].replace("s", "l")
    url = text.split("/")
    url[-2] = replacement
    return "/".join(url)


con = sql.connect("database.db")
cur = con.cursor()
books = pd.read_sql("SELECT * FROM books", con)
books["large_image_url"] = books["small_image_url"].apply(lambda x: get_large_url(x))

books["original_title"] = books["original_title"].str.title()
con.close()
import random


@api.route("/api/books/featured")
class Random(Resource):
    def get(self):
        data = request.get_json()
        n = data["n"]
        try:
            idx = random.sample(range(0, books.shape[0]), k=n)

            featured = books.loc[
                idx,
                [
                    "book_id",
                    "title",
                    "original_title",
                    "authors",
                    "original_publication_year",
                    "average_rating",
                    "large_image_url",
                    "image_url",
                ],
            ].to_dict(orient="records")
            # response = app.response_class(
            #     response=json.dumps(featured), status=200, mimetype="application/json"
            # )
            return {featured}, 200
        except:
            return {"Internal Server Error"}, 500
            # response = app.response_class(
            #     response=json.dumps("Interal Server Error"),
            #     status=500,
            #     mimetype="application/json",
            # )


# @app.route("/api/books/search", methods=["GET", "POST"])
# def find():

#     con = sql.connect("database.db")

#     data = request.get_json()
#     param = data["query"]
#     n = data["n"]

#     search = pd.read_sql(
#         f'''SELECT * from books where original_title like "%{param}%"''', con
#     )
#     search["large_image_url"] = search["small_image_url"].apply(
#         lambda x: get_large_url(x)
#     )
#     search["original_title"] = search["original_title"].str.title()
#     search = search.reset_index()
#     results = (
#         search.head(n)
#         .loc[
#             :,
#             [
#                 "book_id",
#                 "title",
#                 "original_title",
#                 "authors",
#                 "original_publication_year",
#                 "average_rating",
#                 "large_image_url",
#                 "image_url",
#             ],
#         ]
#         .to_dict(orient="records")
#     )
#     if len(results) > 0:
#         response = app.response_class(
#             response=json.dumps(results), status=200, mimetype="application/json"
#         )
#         con.close()
#         return response
#     else:
#         response = app.response_class(
#             response=json.dumps("Not found"), status=404, mimetype="application/json"
#         )
#         con.close()
#         return response


# with open("recommendation_results.json", "r") as j:
#     contents = json.loads(j.read())

# import functools
# import operator


# @app.route("/api/books/recommend", methods=["GET", "POST"])
# def recommend():
#     data = request.get_json()
#     id = data["id"]
#     try:
#         r = contents.get(str(books[books["book_id"] == id].index.tolist()[0]))[:5]
#         index = functools.reduce(operator.iconcat, r, [])[1::2]
#         index = [int(x) for x in index]
#         recommendations = books.loc[
#             index,
#             [
#                 "book_id",
#                 "title",
#                 "original_title",
#                 "authors",
#                 "original_publication_year",
#                 "average_rating",
#                 "large_image_url",
#                 "image_url",
#             ],
#         ].to_dict(orient="records")
#         response = app.response_class(
#             response=json.dumps(recommendations),
#             status=200,
#             mimetype="application/json",
#         )
#         return response
#     except:
#         response = app.response_class(
#             response=json.dumps("Not Found"), status=404, mimetype="application/json"
#         )
#         return response


# @app.route("/api//books/details", methods=["GET", "POST"])
# def get_by_id():
#     data = request.get_json()
#     book_id = data["id"]

#     book = books[books["goodreads_book_id"] == book_id][
#         [
#             "book_id",
#             "title",
#             "original_title",
#             "authors",
#             "original_publication_year",
#             "average_rating",
#             "large_image_url",
#             "image_url",
#         ]
#     ].to_dict(orient="records")
#     if len(book) > 0:

#         response = app.response_class(
#             response=json.dumps(book), status=200, mimetype="application/json"
#         )
#         return response
#     else:
#         response = app.response_class(
#             response=json.dumps("Not Found"), status=404, mimetype="application/json"
#         )
#         return response


# @app.route("/api/books/top", methods=["GET", "POST"])
# def top_rated():
#     data = request.get_json()
#     n = data["n"]
#     try:
#         top_books = (
#             books.sort_values(by="average_rating", ascending=False)
#             .head(50)
#             .reset_index()
#         )
#         idx = random.sample(range(0, top_books.shape[0]), k=n)
#         top = top_books.loc[
#             idx,
#             [
#                 "book_id",
#                 "title",
#                 "original_title",
#                 "authors",
#                 "original_publication_year",
#                 "average_rating",
#                 "large_image_url",
#                 "image_url",
#             ],
#         ].to_dict(orient="records")

#         response = app.response_class(
#             response=json.dumps(top), status=200, mimetype="application/json"
#         )
#         return response
#     except:
#         response = app.response_class(
#             response=json.dumps("Internal Server Error"),
#             status=500,
#             mimetype="application/json",
#         )
#         return response


# @app.route("/api/user/login", methods=["GET", "POST"])
# def login():
#     msg = ""
#     data = request.get_json()

#     username = data["username"]
#     password = data["password"]
#     with sql.connect("database.db") as con:
#         cur = con.cursor()
#         cur.execute(
#             "SELECT * FROM users WHERE username =? AND password = ?",
#             (
#                 username,
#                 password,
#             ),
#         )
#         account = cur.fetchone()
#         # print(account)
#     if account:
#         # session['loggedin'] = True
#         # session['id'] = account['id']
#         # session['username'] = account['username']
#         msg = "Logged in successfully !"
#         response = app.response_class(
#             response=json.dumps(msg), status=200, mimetype="application/json"
#         )
#         return response
#     else:
#         msg = "Incorrect username / password !"
#         response = app.response_class(
#             response=json.dumps(msg), status=401, mimetype="application/json"
#         )
#         return response


# @app.route("/api/user/logout", methods=["GET", "POST"])
# def logout():
#     session.pop("loggedin", None)
#     session.pop("id", None)
#     session.pop("username", None)
#     return redirect(url_for("login"))


# @app.route("/api/user/register", methods=["GET", "POST"])
# def register():
#     msg = ""
#     data = request.get_json()

#     username = data["username"]
#     password = data["password"]
#     email = data["email"]
#     with sql.connect("database.db") as con:

#         cur = con.cursor()

#         cur.execute("SELECT * FROM users WHERE username = ?", (username,))
#         account = cur.fetchone()
#         # print(account)

#         if account:
#             msg = "Account already exists !"
#             response = app.response_class(
#                 response=json.dumps(msg), status=403, mimetype="application/json"
#             )
#             return response

#         else:
#             with sql.connect("database.db") as con:
#                 cur = con.cursor()
#                 cur.execute(
#                     "INSERT INTO users (username,password,email) VALUES (?,?,?)",
#                     (username, password, email),
#                 )

#                 con.commit()
#             msg = "You have successfully registered !"
#             response = app.response_class(
#                 response=json.dumps(msg), status=200, mimetype="application/json"
#             )
#             return response


if __name__ == "__main__":
    app.run(debug=False)
