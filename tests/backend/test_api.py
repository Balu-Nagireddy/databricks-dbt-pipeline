"""
Integration tests for the Prism Analytics Analytics API.
Run from the repository root:
    .venv\\Scripts\\pytest tests/backend/test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
from src.backend.app import app

client = TestClient(app, raise_server_exceptions=False)
PREFIX = "/api/v1"


# ──────────────────────────────────────────────────────────────
# Health
# ──────────────────────────────────────────────────────────────
class TestHealth:
    def test_health_returns_ok(self):
        resp = client.get(f"{PREFIX}/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] in ("ok", "degraded")
        assert "version" in body
        assert "database" in body

    def test_version_endpoint(self):
        resp = client.get(f"{PREFIX}/health/version")
        assert resp.status_code == 200
        body = resp.json()
        assert "version" in body
        assert "name" in body

    def test_root_redirect(self):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "docs" in resp.json()


# ──────────────────────────────────────────────────────────────
# Executive
# ──────────────────────────────────────────────────────────────
class TestExecutive:
    def test_kpis_returns_200(self):
        resp = client.get(f"{PREFIX}/executive/kpis")
        assert resp.status_code == 200

    def test_kpis_has_revenue(self):
        body = client.get(f"{PREFIX}/executive/kpis").json()
        assert "total_revenue" in body

    def test_kpis_has_orders(self):
        body = client.get(f"{PREFIX}/executive/kpis").json()
        assert "total_orders" in body

    def test_kpis_has_customers(self):
        body = client.get(f"{PREFIX}/executive/kpis").json()
        assert "total_customers" in body


# ──────────────────────────────────────────────────────────────
# Sales
# ──────────────────────────────────────────────────────────────
class TestSales:
    def test_daily_returns_list(self):
        resp = client.get(f"{PREFIX}/sales/daily")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_daily_has_expected_fields(self):
        rows = client.get(f"{PREFIX}/sales/daily?limit=1").json()
        assert len(rows) > 0
        assert "sale_date" in rows[0]
        assert "total_revenue" in rows[0]
        assert "total_orders" in rows[0]

    def test_daily_pagination(self):
        resp = client.get(f"{PREFIX}/sales/daily?page=1&limit=5")
        assert resp.status_code == 200
        assert len(resp.json()) <= 5

    def test_monthly_returns_list(self):
        resp = client.get(f"{PREFIX}/sales/monthly")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_by_state_returns_list(self):
        resp = client.get(f"{PREFIX}/sales/by-state")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_invalid_limit_returns_422(self):
        resp = client.get(f"{PREFIX}/sales/daily?limit=0")
        assert resp.status_code == 422


# ──────────────────────────────────────────────────────────────
# Customers
# ──────────────────────────────────────────────────────────────
class TestCustomers:
    def test_segments_returns_list(self):
        resp = client.get(f"{PREFIX}/customers/segments")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_segment_filter_vip(self):
        resp = client.get(f"{PREFIX}/customers/segments?segment=VIP")
        assert resp.status_code == 200
        body = resp.json()
        for item in body:
            assert item["customer_segment"] == "VIP"

    def test_top_cities_returns_list(self):
        resp = client.get(f"{PREFIX}/customers/top-cities")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_top_cities_has_city_state(self):
        rows = client.get(f"{PREFIX}/customers/top-cities?limit=1").json()
        assert len(rows) > 0
        assert "customer_city" in rows[0]
        assert "customer_state" in rows[0]

    def test_repeat_stats_returns_data(self):
        resp = client.get(f"{PREFIX}/customers/repeat-stats")
        assert resp.status_code == 200
        assert len(resp.json()) > 0


# ──────────────────────────────────────────────────────────────
# Products
# ──────────────────────────────────────────────────────────────
class TestProducts:
    def test_top_products_returns_list(self):
        resp = client.get(f"{PREFIX}/products/top")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_top_products_has_expected_fields(self):
        rows = client.get(f"{PREFIX}/products/top?limit=1").json()
        assert len(rows) > 0
        assert "product_id" in rows[0]
        assert "total_revenue" in rows[0]
        assert "units_sold" in rows[0]

    def test_category_filter(self):
        resp = client.get(f"{PREFIX}/products/top?category=electronics")
        assert resp.status_code == 200

    def test_categories_returns_list(self):
        resp = client.get(f"{PREFIX}/products/categories")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


# ──────────────────────────────────────────────────────────────
# Finance
# ──────────────────────────────────────────────────────────────
class TestFinance:
    def test_payments_returns_list(self):
        resp = client.get(f"{PREFIX}/finance/payments")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_payments_has_payment_type(self):
        body = client.get(f"{PREFIX}/finance/payments").json()
        assert len(body) > 0
        assert "payment_type" in body[0]
        assert "transaction_count" in body[0]

    def test_installments_returns_list(self):
        resp = client.get(f"{PREFIX}/finance/installments")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


# ──────────────────────────────────────────────────────────────
# Logistics
# ──────────────────────────────────────────────────────────────
class TestLogistics:
    def test_performance_returns_list(self):
        resp = client.get(f"{PREFIX}/logistics/performance")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_performance_has_state(self):
        rows = client.get(f"{PREFIX}/logistics/performance?limit=1").json()
        assert len(rows) > 0
        assert "customer_state" in rows[0]
        assert "avg_delivery_duration_days" in rows[0]

    def test_success_rates_returns_single(self):
        resp = client.get(f"{PREFIX}/logistics/success-rates")
        assert resp.status_code == 200
        body = resp.json()
        assert "success_rate_percent" in body

    def test_seller_shipping_returns_list(self):
        resp = client.get(f"{PREFIX}/logistics/seller-shipping")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_seller_shipping_pagination(self):
        resp = client.get(f"{PREFIX}/logistics/seller-shipping?page=1&limit=10")
        assert resp.status_code == 200
        assert len(resp.json()) <= 10
