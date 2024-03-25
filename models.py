"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database and set app context"""
    db.app = app
    db.init_app(app)
    app_ctx = app.app_context()
    app_ctx.push()
    db.create_all()


class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False, default="https://tinyurl.com/demo-cupcake")

    def serialize(self):
        """Serializes our cupcakes into a dict, which can be JSONified"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
    
    def __repr__(self):
        return f"<Cupcake {self.id} flavor={self.flavor} size={self.size} rating={self.rating} image={self.image}>"