import unittest
from app import create_app
from models.database import db
from models.order import Order

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_order(self):
        response = self.client.post("/api/orders", json={"customer_id": 1, "product_id": 2, "quantity": 3})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", str(response.data))

    def test_get_orders(self):
        self.client.post("/api/orders", json={"customer_id": 1, "product_id": 2, "quantity": 3})
        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, 200)
        self.assertIn("customer_id", str(response.data))

    def test_get_order(self):
        self.client.post("/api/orders", json={"customer_id": 1, "product_id": 2, "quantity": 3})
        response = self.client.get("/api/orders/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("customer_id", str(response.data))

    def test_update_order(self):
        self.client.post("/api/orders", json={"customer_id": 1, "product_id": 2, "quantity": 3})
        response = self.client.put("/api/orders/1", json={"quantity": 4})
        self.assertEqual(response.status_code, 200)
        self.assertIn("quantity", str(response.data))

    def test_delete_order(self):
        self.client.post("/api/orders", json={"customer_id": 1, "product_id": 2, "quantity": 3})
        response = self.client.delete("/api/orders/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Order deleted successfully", str(response.data))

if __name__ == "__main__":
    unittest.main()