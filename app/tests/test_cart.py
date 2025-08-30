from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal

from app.main import app
from app.models.users import User
from app.auth.dependencies import get_current_user

client = TestClient(app)

# Sample user for testing
@pytest.fixture
def sample_user():
    return User(
        id=1,
        username="testuser", 
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_admin=False
    )

def mock_get_user():
    """Mock user for authentication override"""
    return User(
        id=1,
        username="testuser",
        email="test@example.com", 
        first_name="Test",
        last_name="User",
        is_admin=False
    )


class TestCartAuthentication:
    """Test that cart endpoints require authentication"""
    
    def test_get_cart_unauthorized(self):
        """Should return 401 without authentication"""
        response = client.get('/cart/')
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
    
    def test_add_to_cart_unauthorized(self):
        """Should return 401 without authentication"""
        response = client.post('/cart/items/', json={
            "product_id": 1,
            "quantity": 1
        })
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


class TestCartWithAuth:
    """Test cart operations with mocked authentication"""
    
    def setup_method(self):
        """Set up authentication mock before each test"""
        app.dependency_overrides[get_current_user] = mock_get_user
        
    def teardown_method(self):
        """Clean up after each test"""
        app.dependency_overrides.clear()
    
    @patch('app.services.cart_services.add_to_cart_with_quantity')
    def test_add_to_cart_success(self, mock_add_service):
        """Should successfully add item to cart"""
        mock_add_service.return_value = {
            "message": "Item added to cart successfully",
            "success": True
        }
        
        response = client.post('/cart/items/', json={
            "product_id": 1,
            "quantity": 2
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] == True
        assert data["message"] == "Item added to cart successfully"
        mock_add_service.assert_called_once()
    
    @patch('app.services.cart_services.get_cart_summary')
    def test_get_cart_empty(self, mock_get_summary):
        """Should return empty cart"""
        from app.schemas.cart import CartResponse
        
        mock_get_summary.return_value = CartResponse(
            items=[],
            total_items=0,
            total_amount=Decimal("0.00")
        )
        
        response = client.get('/cart/')
        
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total_items"] == 0
        assert float(data["total_amount"]) == 0.0
    
    @patch('app.services.cart_services.update_cart_item_quantity')
    def test_update_cart_item(self, mock_update_service):
        """Should update cart item quantity"""
        mock_update_service.return_value = {
            "message": "Cart item updated successfully",
            "success": True
        }
        
        response = client.put('/cart/items/1/', json={
            "quantity": 3
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["message"] == "Cart item updated successfully"
    
    @patch('app.services.cart_services.remove_from_cart')
    def test_remove_from_cart(self, mock_remove_service):
        """Should remove item from cart"""
        mock_remove_service.return_value = {
            "message": "Item removed from cart successfully",
            "success": True
        }
        
        response = client.delete('/cart/items/1/')
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["message"] == "Item removed from cart successfully"
    
    @patch('app.services.cart_services.clear_cart')
    def test_clear_cart(self, mock_clear_service):
        """Should clear entire cart"""
        mock_clear_service.return_value = {
            "message": "Cart cleared successfully. Removed 2 items",
            "success": True
        }
        
        response = client.delete('/cart/')
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "Removed 2 items" in data["message"]


class TestCartValidation:
    """Test input validation for cart operations"""
    
    def setup_method(self):
        """Set up authentication mock before each test"""
        app.dependency_overrides[get_current_user] = mock_get_user
        
    def teardown_method(self):
        """Clean up after each test"""
        app.dependency_overrides.clear()
    
    def test_invalid_product_id_zero(self):
        """Should reject product_id of 0"""
        response = client.post('/cart/items/', json={
            "product_id": 0,
            "quantity": 1
        })
        assert response.status_code == 422
    
    def test_invalid_quantity_zero(self):
        """Should reject quantity of 0"""
        response = client.post('/cart/items/', json={
            "product_id": 1,
            "quantity": 0
        })
        assert response.status_code == 422
    
    def test_invalid_quantity_too_high(self):
        """Should reject quantity over 100"""
        response = client.post('/cart/items/', json={
            "product_id": 1,
            "quantity": 101
        })
        assert response.status_code == 422
    
    def test_invalid_data_types(self):
        """Should reject invalid data types"""
        response = client.post('/cart/items/', json={
            "product_id": "invalid",
            "quantity": 1
        })
        assert response.status_code == 422


class TestCartErrors:
    """Test error handling in cart operations"""
    
    def setup_method(self):
        """Set up authentication mock before each test"""
        app.dependency_overrides[get_current_user] = mock_get_user
        
    def teardown_method(self):
        """Clean up after each test"""
        app.dependency_overrides.clear()
    
    @patch('app.services.cart_services.add_to_cart_with_quantity')
    def test_product_not_found(self, mock_add_service):
        """Should handle product not found error"""
        mock_add_service.side_effect = HTTPException(
            status_code=404,
            detail="Product not found"
        )
        
        response = client.post('/cart/items/', json={
            "product_id": 999,
            "quantity": 1
        })
        
        assert response.status_code == 404
        assert "Product not found" in response.json()["detail"]
    
    @patch('app.services.cart_services.add_to_cart_with_quantity')
    def test_insufficient_stock(self, mock_add_service):
        """Should handle insufficient stock error"""
        mock_add_service.side_effect = HTTPException(
            status_code=400,
            detail="Insufficient stock. Available: 5"
        )
        
        response = client.post('/cart/items/', json={
            "product_id": 1,
            "quantity": 10
        })
        
        assert response.status_code == 400
        assert "Insufficient stock" in response.json()["detail"]
