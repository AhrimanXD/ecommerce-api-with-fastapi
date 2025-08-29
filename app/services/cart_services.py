from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.products import Product
from app.models.users import User
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

  