from fastapi import APIRouter, Depends, HTTPException, Path
from app.auth.dependencies import get_current_user
from typing import Annotated
from app.models.users import User
from app.db.database import SessionDep
from app.services import cart_services
from app.schemas.cart import (
    AddToCartRequest, 
    UpdateCartItemRequest,
    CartResponse,
    CartOperationResponse,
    CartItemOut  # Keep for backward compatibility
)

router = APIRouter(prefix='/cart', tags=['cart'])


@router.post('/items/', status_code=201, response_model=CartOperationResponse)
async def add_to_cart(
    request: AddToCartRequest,
    current_user: Annotated[User, Depends(get_current_user)], 
    db: SessionDep
):
    """Add item to cart with specified quantity"""
    result = cart_services.add_to_cart_with_quantity(
        db, current_user, request.product_id, request.quantity
    )
    return CartOperationResponse(**result)


@router.get('/', response_model=CartResponse)
async def get_cart(
    current_user: Annotated[User, Depends(get_current_user)], 
    db: SessionDep
):
    """Get complete cart summary with totals"""
    return cart_services.get_cart_summary(db, current_user)


@router.put('/items/{product_id}/', response_model=CartOperationResponse)
async def update_cart_item(
    product_id: Annotated[int, Path(gt=0, description="Product ID")],
    request: UpdateCartItemRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: SessionDep
):
    """Update quantity of specific cart item"""
    result = cart_services.update_cart_item_quantity(
        db, current_user, product_id, request.quantity
    )
    return CartOperationResponse(**result)


@router.delete('/items/{product_id}/', response_model=CartOperationResponse)
async def remove_from_cart(
    product_id: Annotated[int, Path(gt=0, description="Product ID")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: SessionDep
):
    """Remove specific item from cart"""
    result = cart_services.remove_from_cart(db, current_user, product_id)
    return CartOperationResponse(**result)


@router.delete('/', response_model=CartOperationResponse)
async def clear_cart(
    current_user: Annotated[User, Depends(get_current_user)],
    db: SessionDep
):
    """Clear all items from cart"""
    result = cart_services.clear_cart(db, current_user)
    return CartOperationResponse(**result)


# Legacy endpoint for backward compatibility
@router.post('/add/', status_code=201, deprecated=True)
async def add_to_cart_legacy(
    request: AddToCartRequest,
    current_user: Annotated[User, Depends(get_current_user)], 
    db: SessionDep
):
    """Legacy endpoint - use POST /cart/items/ instead"""
    try:
        success = cart_services.add_to_cart(db, current_user, request.product_id)
        if success:
            return {"message": "Product added to cart successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to add product to cart")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
