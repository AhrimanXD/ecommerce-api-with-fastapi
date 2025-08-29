from fastapi.testclient import TestClient
import pytest

from app.main import app


client = TestClient(app)

class TestCartRoutes:
  def test_cart_unauthorized(self):
    response = client.get('/cart/')
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

class TestProductRoutes:

  @pytest.mark.parametrize(
      "product_id, status_code",
      [
        (1, 200),
        (2, 200),
        ('hello', 422),
        (50, 404)
      ]
  )
  def test_get_product(self, product_id, status_code):
    response = client.get(f'/products/{product_id}')
    assert response.status_code == status_code