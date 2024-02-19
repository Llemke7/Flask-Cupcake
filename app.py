"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connect_db(app)

@app.route('/')
def home():
    return render_template('index.html')

def serialize_cupcake(cupcake):
    """Serialize a cupcake object into a dictionary"""
    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }

@app.route('/api/cupcakes')
def list_cupcakes():
    """Return data about all cupcakes JSON"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcake/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """Return single Cupcake in JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id) 
    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create Cupcake"""
    data = request.json
    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', 'https://tinyurl.com/demo-cupcake') 

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    return jsonify(cupcake=serialized), 201 

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake"""
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()
    serialized_cupcake = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized_cupcake)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")