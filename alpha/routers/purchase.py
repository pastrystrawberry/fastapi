
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schema
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.get("/")
def get_purchases(current_user: models.User = Depends(get_current_user),db: Session = Depends(get_db)):
    purchases = (

        db.query(
            models.Purchase,
            models.User.name.label("username"),
            models.Product.name.label("product"),
            models.Product.price
        )
        .join(
            models.User,
            models.Purchase.user_id == models.User.id
        )
        .join(
            models.Product,
            models.Purchase.product_id == models.Product.id
        )
        .filter(models.Purchase.user_id==current_user.id)
        .all()
    )

    results = []

    for purchase, username, product, price in purchases:
        results.append({
            "id": purchase.id,
            "username": username,
            "product": product,
            "price": price,
            "quantity": purchase.quantity,
            "total": price * purchase.quantity
        })

    return {"data": results}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_purchase(
    purchase: schema.PurchaseCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(
        models.Product.id == purchase.product_id
    ).first()
    if not product:
        raise HTTPException(404,"Product not found")
    if purchase.quantity<=0:
        raise HTTPException(400,"Quantity must be greater than zero")
    
    new_purchase = models.Purchase(
        user_id=current_user.id,
        product_id=purchase.product_id,
        quantity=purchase.quantity
    )

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return {"data": new_purchase}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(id: int,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(
        models.Purchase.id == id,
        models.Purchase.user_id == current_user.id
    ).first()

    if not purchase:
        raise HTTPException(404, "Purchase not found")

    db.delete(purchase)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
