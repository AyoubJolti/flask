from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Setup the database URI (this example uses SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the models

# Parent table: Author
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship with Book (one-to-many)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"Author('{self.id}', '{self.name}')"

# Child table: Book (with a foreign key)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.id}', '{self.title}', '{self.author_id}')"

# Create the tables in the database
with app.app_context():
    db.create_all()

# Routes for CRUD operations

# Create Author
@app.route('/author', methods=['POST'])
def create_author():
    data = request.get_json()
    new_author = Author(name=data['name'])
    db.session.add(new_author)
    db.session.commit()
    return jsonify({'message': 'Author created successfully'}), 201

# Read Authors
@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    authors_list = [{'id': author.id, 'name': author.name} for author in authors]
    return jsonify(authors_list)

# Create Book
@app.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author_id=data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

# Read Books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{'id': book.id, 'title': book.title, 'author_id': book.author_id} for book in books]
    return jsonify(books_list)

# Update Author
@app.route('/author/<int:id>', methods=['PUT'])
def update_author(id):
    data = request.get_json()
    author = Author.query.get_or_404(id)
    author.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Author updated successfully'})

# Delete Author
@app.route('/author/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'message': 'Author deleted successfully'})

# Update Book
@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.title = data['title']
    book.author_id = data['author_id']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

# Delete Book
@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
