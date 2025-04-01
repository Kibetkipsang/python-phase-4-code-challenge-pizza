#!/usr/bin/env python3
from flask import jsonify, json
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Pizza Restaurants</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        return jsonify([r.to_dict() for r in restaurants]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/restaurants/<int:id>", methods=['GET'])
def get_restaurant_by_id(id):
    try:
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "restaurant_pizzas": []
        }
        
        for rp in restaurant.restaurant_pizzas:
            restaurant_data["restaurant_pizzas"].append({
                "id": rp.id,
                "price": rp.price,
                "pizza": {
                    "id": rp.pizza.id,
                    "name": rp.pizza.name,
                    "ingredients": rp.pizza.ingredients
                }
            })
            
        return jsonify(restaurant_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restaurants/<int:id>", methods=['DELETE'])
def delete_restaurants(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    db.session.delete(restaurant)
    db.session.commit()
    
    return "", 204

@app.route("/pizzas", methods=['GET'])
def get_pizzas():
    try:
        pizzas = Pizza.query.all()
        return jsonify([{
            "id": p.id,
            "name": p.name,
            "ingredients": p.ingredients
        } for p in pizzas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    
    if not request.is_json:
        print("ERROR: Request is not JSON")
        return jsonify({"errors": ["validation errors"]}), 400
    
    try:
        data = request.get_json()
        
        def get_field(data, possible_names):
            for name in possible_names:
                if name in data:
                    return data[name]
            return None
        
        price = get_field(data, ['price', 'Price'])
        pizza_id = get_field(data, ['pizza_id', 'pizzaId', 'PizzaId'])
        restaurant_id = get_field(data, ['restaurant_id', 'restaurantId', 'RestaurantId'])
        
       
        if None in (price, pizza_id, restaurant_id):
            missing = []
            if price is None: missing.append("price")
            if pizza_id is None: missing.append("pizza_id")
            if restaurant_id is None: missing.append("restaurant_id")
            return jsonify({"errors": ["validation errors"]}), 400
        
        
        try:
            price = int(price)
            pizza_id = int(pizza_id)
            restaurant_id = int(restaurant_id)
        except (ValueError, TypeError):
            return jsonify({"errors": ["validation errors"]}), 400
        
  
        if not 1 <= price <= 30:
            return jsonify({"errors": ["validation errors"]}), 400
            
      
        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)
        if not restaurant or not pizza:
            return jsonify({"errors": ["validation errors"]}), 400
        
      
        rp = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(rp)
        db.session.commit()
        
        return jsonify({
            "id": rp.id,
            "price": rp.price,
            "pizza": {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            },
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400