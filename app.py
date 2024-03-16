from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

books = [
    {"id": 1, "title": "Harry Potter", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
    {"id": 3, "title": "Book 3", "author": "Author 3"}
]
next_id = 4  # Variable to keep track of next available ID for new books


@app.route("/")
def hello_world():
    return "<h1>Hello World</h1>"


# Get all books
@app.route("/books", methods=["GET"])
@cross_origin()
def get_all_books():
    return jsonify({"books": books})


# Get a single book by id
@app.route("/books/<int:book_id>", methods=["GET"])
@cross_origin()
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return jsonify({"book": book})
    else:
        abort(404, "Book not found")


# Create a new book
@app.route("/books", methods=["POST"])
@cross_origin()
def create_book():
    global next_id
    data = request.get_json()
    if "title" in data and "author" in data:
        new_book = {"id": next_id, "title": data["title"], "author": data["author"]}
        books.append(new_book)
        next_id += 1
        return jsonify({"message": "Book created successfully", "book": new_book}), 201
    else:
        abort(400, "Incomplete data")


# Update an existing book
@app.route("/books/<int:book_id>", methods=["PUT"])
@cross_origin()
def update_book(book_id):
    data = request.get_json()
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        if "title" in data:
            book["title"] = data["title"]
        if "author" in data:
            book["author"] = data["author"]
        return jsonify({"message": "Book updated successfully", "book": book})
    else:
        abort(404, "Book not found")


# Delete a book
@app.route("/books/<int:book_id>", methods=["DELETE"])
@cross_origin()
def delete_book(book_id):
    global books
    initial_length = len(books)
    books = [book for book in books if book["id"] != book_id]
    if len(books) < initial_length:
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        abort(404, "Book not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)