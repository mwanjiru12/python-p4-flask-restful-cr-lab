#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'price': float(self.price)
        }

class PlantsResource(Resource):
    def get(self):
        plants = Plant.query.all()
        return make_response(jsonify([plant.to_dict() for plant in plants]), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

class PlantByIDResource(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return make_response(jsonify(plant.to_dict()), 200)

api.add_resource(PlantsResource, '/plants')
api.add_resource(PlantByIDResource, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
