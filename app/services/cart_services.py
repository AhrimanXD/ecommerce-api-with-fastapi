from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.cart import Cart, CartItem
from app.models.products import Product
from app.models.users import User
from app.schemas.cart import CartResponse, CartItemResponse
from fastapi import HTTPException
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def create_cart(session:Session, user) -> Cart:
  cart = Cart(user_id = user.id)
  session.add(cart)
  session.commit()
  session.refresh(cart)
  return cart

def create_cartitem(session:Session, product_id, cart_id):
  cart_item = CartItem(product_id=product_id, cart_id=cart_id, quantity = 1)
  session.add(cart_item)
  session.commit()



def add_to_cart(session: Session, current_user: User, product_id: int):
  try:
    cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
      cart = create_cart(session, current_user)
    cartitem = session.query(CartItem).filter(CartItem.product_id == product_id, CartItem.cart_id == cart.id).first()
    if cartitem:
      update_quantity(cartitem, session)
      logger.info(f"Successfully increased the quantity of product {product_id} in the cart of user {current_user.id}")
      return True
    if validate_product_id(session, product_id):
      create_cartitem(session, product_id=product_id,cart_id=cart.id)
      logger.info(f"Successfully added product {product_id} to cart for user {current_user.id}")
      return True
  except Exception as e:
    logger.error(f"Error adding item to cart: {e}")
    session.rollback()
    raise e
  return False

  
def validate_product_id(session: Session, product_id: int):
  return session.get(Product, product_id)

def update_quantity(cartitem, session):
  cartitem.quantity += 1
  session.commit()
  session.refresh(cartitem)

def get_cart(session: Session, current_user: User):
    cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return None
    
    # Single query with join
    results = session.query(CartItem, Product)\
        .join(Product, CartItem.product_id == Product.id)\
        .filter(CartItem.cart_id == cart.id)\
        .all()
    
    response = []
    for cart_item, product in results:
        sub_total = product.price * cart_item.quantity
        response.append({
            "name": product.name,
            "price": product.price,
            "quantity": cart_item.quantity,
            "sub_total": sub_total
        })
    
    return response

# Enhanced cart service methods

def add_to_cart_with_quantity(session: Session, current_user: User, product_id: int, quantity: int = 1) -> dict:
    """Add product to cart with specified quantity"""
    try:
        # Validate product exists and is available
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if not product.is_available:
            raise HTTPException(status_code=400, detail="Product is not available")
        
        # Check stock availability
        if quantity > product.stock:
            raise HTTPException(status_code=400, detail=f"Insufficient stock. Available: {product.stock}")
        
        # Get or create user's cart
        cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            cart = create_cart(session, current_user)
        
        # Check if item already exists in cart
        existing_item = session.query(CartItem).filter(
            CartItem.product_id == product_id, 
            CartItem.cart_id == cart.id
        ).first()
        
        if existing_item:
            # Update quantity but check stock
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                raise HTTPException(status_code=400, detail=f"Cannot add {quantity} items. Would exceed stock limit")
            
            existing_item.quantity = new_quantity
            session.commit()
            logger.info(f"Updated cart item quantity for product {product_id} to {new_quantity}")
        else:
            # Create new cart item
            cart_item = CartItem(product_id=product_id, cart_id=cart.id, quantity=quantity)
            session.add(cart_item)
            session.commit()
            logger.info(f"Added new item to cart: product {product_id}, quantity {quantity}")
        
        return {"message": "Item added to cart successfully", "success": True}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding item to cart: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to add item to cart")


def update_cart_item_quantity(session: Session, current_user: User, product_id: int, new_quantity: int) -> dict:
    """Update quantity of specific cart item"""
    try:
        # Validate product and stock
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if new_quantity > product.stock:
            raise HTTPException(status_code=400, detail=f"Insufficient stock. Available: {product.stock}")
        
        # Find cart item
        cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        cart_item = session.query(CartItem).filter(
            CartItem.product_id == product_id,
            CartItem.cart_id == cart.id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Item not found in cart")
        
        cart_item.quantity = new_quantity
        session.commit()
        
        logger.info(f"Updated cart item {product_id} quantity to {new_quantity}")
        return {"message": "Cart item updated successfully", "success": True}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating cart item: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update cart item")


def remove_from_cart(session: Session, current_user: User, product_id: int) -> dict:
    """Remove specific item from cart"""
    try:
        cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        cart_item = session.query(CartItem).filter(
            CartItem.product_id == product_id,
            CartItem.cart_id == cart.id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Item not found in cart")
        
        session.delete(cart_item)
        session.commit()
        
        logger.info(f"Removed product {product_id} from cart")
        return {"message": "Item removed from cart successfully", "success": True}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing item from cart: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to remove item from cart")


def clear_cart(session: Session, current_user: User) -> dict:
    """Remove all items from user's cart"""
    try:
        cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        # Delete all cart items
        deleted_count = session.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        session.commit()
        
        logger.info(f"Cleared cart for user {current_user.id}, removed {deleted_count} items")
        return {"message": f"Cart cleared successfully. Removed {deleted_count} items", "success": True}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing cart: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear cart")


def get_cart_summary(session: Session, current_user: User) -> CartResponse:
    """Get detailed cart summary with totals"""
    try:
        cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            return CartResponse(items=[], total_items=0, total_amount=Decimal('0.00'))
        
        # Query cart items with product details
        results = session.query(CartItem, Product)\
            .join(Product, CartItem.product_id == Product.id)\
            .filter(CartItem.cart_id == cart.id)\
            .all()
        
        cart_items = []
        total_amount = Decimal('0.00')
        total_items = 0
        
        for cart_item, product in results:
            subtotal = Decimal(str(product.price)) * cart_item.quantity
            
            cart_items.append(CartItemResponse(
                product_id=product.id,
                product_name=product.name,
                product_price=Decimal(str(product.price)),
                quantity=cart_item.quantity,
                subtotal=subtotal
            ))
            
            total_amount += subtotal
            total_items += cart_item.quantity
        
        return CartResponse(
            items=cart_items,
            total_items=total_items,
            total_amount=total_amount
        )
    
    except Exception as e:
        logger.error(f"Error getting cart summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cart summary")
