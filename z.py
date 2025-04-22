from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Setup the database URI (this example uses SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ayoub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    def __repr__(self):
        return f"Author('{self.id}', '{self.name}')"
with app.app_context():
    db.create_all()       
@app.route('/users',methods=['GET'])
def getAllUsers():
    allUsers = users.query.all()
    usersList = [{'id': user.id, 'name': user.name} for user in allUsers]  
    return jsonify(usersList)  


@app.route('/user/<int:id>', methods=['GET'])
def getOneUser(id):
    user = users.query.get(id)  # غادي يرجع المستخدم ولا يعطي 404 إلا ما لقاوش
    userData = {'id': user.id, 'name': user.name}
    return jsonify(userData)

@app.route('/user', methods=['POST'])
def add():
    data = request.get_json()
    newUser = users(name=data['name'])
    db.session.add(newUser)
    db.session.commit()
    return jsonify({'message': 'Author created successfully'}), 201

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    user = users.query.get(id)  # غادي يرجع المستخدم ولا يعطي 404 إلا ما لقاوش
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Author created successfully'}), 201

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    user = users.query.get(id)  # غادي يرجع المستخدم ولا يعطي 404 إلا ما لقاوش
    data = request.get_json()
    user.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Author created successfully'}), 201    
              
if __name__ == '__main__':
    app.run(debug=True)