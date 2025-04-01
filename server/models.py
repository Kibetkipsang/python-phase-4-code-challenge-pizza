from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"
    serialize_rules = ('-restaurant_pizzas.restaurant',)
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    address = db.Column(db.String, nullable=False)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")
    pizzas = association_proxy("restaurant_pizzas", "pizza")

    # add serialization rules
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }
    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"
    serialize_rules = ('-pizza_restaurants.pizza',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # add relationship
    pizza_restaurants = db.relationship("RestaurantPizza", back_populates="pizza")
    # add serialization rules
    def to_dict(self):
        return {
            "id" : self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }
    
    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.pizza_restaurants')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)

    # add relationships
    restaurant = db.relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = db.relationship("Pizza", back_populates="pizza_restaurants")
    # add serialization rules
    def to_dict(self):
        return {
            "id" : self.id,
            "price" : self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id" : self.pizza_id
        }
    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("validation errors") 
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
