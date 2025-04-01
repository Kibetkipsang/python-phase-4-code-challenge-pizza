#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza
import sys

def run_seed():
    with app.app_context():
        try:
            print("\n=== Starting Seed ===")
            
            # Clear existing data
            print("Deleting old data...")
            db.session.query(RestaurantPizza).delete()
            db.session.query(Pizza).delete()
            db.session.query(Restaurant).delete()
            db.session.commit()

            # Create restaurants
            restaurants = [
                Restaurant(name="Karen's Pizza Shack", address='123 Main St'),
                Restaurant(name="Sanjay's Pizza", address='456 Oak Ave'),
                Restaurant(name="Kiki's Pizza", address='789 Pine Rd')
            ]
            db.session.add_all(restaurants)
            db.session.commit()

            # Create pizzas
            pizzas = [
                Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Cheese"),
                Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"),
                Pizza(name="California", ingredients="Dough, Sauce, Ricotta, Red peppers")
            ]
            db.session.add_all(pizzas)
            db.session.commit()

            # Create restaurant_pizzas with validated prices
            menu_items = [
                RestaurantPizza(restaurant=restaurants[0], pizza=pizzas[0], price=12),
                RestaurantPizza(restaurant=restaurants[0], pizza=pizzas[1], price=14),
                RestaurantPizza(restaurant=restaurants[1], pizza=pizzas[0], price=13),
                RestaurantPizza(restaurant=restaurants[2], pizza=pizzas[2], price=15)
            ]
            db.session.add_all(menu_items)
            db.session.commit()

            print("=== Seeding Complete! ===")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"!!! SEEDING FAILED !!!\nError: {str(e)}", file=sys.stderr)
            return False

if __name__ == "__main__":
    if run_seed():
        # Verification
        with app.app_context():
            print(f"Restaurants: {Restaurant.query.count()}")
            print(f"Pizzas: {Pizza.query.count()}")
            print(f"Menu Items: {RestaurantPizza.query.count()}")
    else:
        sys.exit(1)