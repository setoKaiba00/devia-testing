from flask import Blueprint, request, jsonify
from models.database import db
from models.order import Order

order_routes = Blueprint("order_routes", __name__)

@order_routes.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200

@order_routes.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify(order.to_dict()), 200
    return jsonify({"error": "Order not found"}), 404

@order_routes.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data.get("customer_id") or not data.get("product_id") or not data.get("quantity"):
        return jsonify({"error": "Customer ID, Product ID, and quantity are required"}), 400

    new_order = Order(customer_id=data["customer_id"], product_id=data["product_id"], quantity=data["quantity"])
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@order_routes.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    order.quantity = data.get("quantity", order.quantity)
    db.session.commit()
    return jsonify(order.to_dict()), 200

@order_routes.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"}), 200