
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schema
from ..dependencies import get_current_user
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_products(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    products = db.query(models.Product).all()
    return {"data": products}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product: schema.ProductCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_product = models.Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"data": new_product}


@router.get("/{id}")
def get_product(id: int,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == id
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    return {"data": product}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == id
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.post("/{id}/reaction")
def react_to_product(
    id: int,
    reaction: schema.ProductReactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(
        models.Product.id == id
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    existing_reaction = db.query(models.ProductReaction).filter(
        models.ProductReaction.user_id == current_user.id,
        models.ProductReaction.product_id == id
    ).first()

    if existing_reaction:
        existing_reaction.reaction = reaction.reaction
    else:
        new_reaction = models.ProductReaction(
            user_id=current_user.id,
            product_id=id,
            reaction=reaction.reaction
        )
        db.add(new_reaction)

    db.commit()

    return {"message": f"Product {reaction.reaction}d successfully"}
@router.delete("/{id}/reaction", status_code=status.HTTP_204_NO_CONTENT)
def remove_product_reaction(
    id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reaction = db.query(models.ProductReaction).filter(
        models.ProductReaction.user_id == current_user.id,
        models.ProductReaction.product_id == id
    ).first()

    if not reaction:
        raise HTTPException(404, "Reaction not found")

    db.delete(reaction)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)