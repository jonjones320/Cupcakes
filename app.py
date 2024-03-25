"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)


@app.route('/')
def home():
    cupcakes = Cupcake.query.all()

    return render_template("index.html", cupcakes=cupcakes)


@app.route('/api/cupcakes')
def list_cupcakes():
    """Get data about all cupcakes. Respond with JSON like:
    `{cupcakes:[{id,flavor,size,rating,image},...]}`. 
    The values should come from each cupcake instance."""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def view_cupcake(id):
    """Get data about a single cupcake. Respond with JSON like:
    `{cupcake:{id,flavor,size,rating,image}}`. 
    This should raise a 404 if the cupcake cannot be found."""

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request. 
    Respond with JSON like:`{cupcake:{id,flavor,size,rating,image}}`"""

    new_cupcake = Cupcake(
        flavor=request.json["flavor"], 
        size=request.json["size"], 
        rating=request.json["rating"], 
        image=request.json["image"]
        )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Change a single cupcake and respond with JSON"""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor), 
    cupcake.size = request.json.get ("size", cupcake.size), 
    cupcake.rating=request.json.get("rating", cupcake.rating), 
    cupcake.image=request.json.get("image", cupcake.image)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/[cupcake-id]', methods=['DELETE'])
def delete_cupcake(id):
    """Deletes a specific innocent cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="deleted")