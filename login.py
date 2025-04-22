from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # for hashing passwords

# Initialize the Flask application
app = Flask(__name__)

# Setup the database URI (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model (Table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

# Create the database tables
with app.app_context():
    db.create_all()

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Fetch username and password from the request body
    username = data.get('username')
    password = data.get('password')
    
    # Fetch the user from the database
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        # User is found and password is correct
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    else:
        # Incorrect credentials
        return jsonify({'message': 'Invalid username or password'}), 401

# Route to register a new user (for demo purposes)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    
    # Create new user and add to the database
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
