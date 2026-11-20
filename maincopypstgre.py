"""
from fastapi import FastAPI,Response,status, HTTPException
from pydantic import BaseModel,EmailStr
from typing import Optional
from fastapi.params import Body
from random import randrange

import psycopg2
from psycopg2.extras import RealDictConnection
app = FastAPI()
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="admin123",
        cursor_factory=RealDictConnection
    )
class User(BaseModel):
    name:str
    email:EmailStr
class Product(BaseModel):
    name:str
    price:float
class Purchase(BaseModel):
    user_id:int
    product_id:int
    quantity: int

@app.get("/")
async def root():
    return {"message": "ecommerece API running"}

@app.get("/user")
def get_posts():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("select * from users")
            return {"data":cursor.fetchall}
@app.post("/users",status_code=201)
def create_user(user:User):
    with get_connection as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users(name,email)
                values(%s,%s)
                RETURNING *
            """,
            
            (user.name,user.email)
            )
            return{"data":cursor.fetchone()}
@app.get('/user/{id}')
def get_user(id:int):
    with get_connection as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM  users WHERE id = %s",
                (id,)
            )
            user= cursor.fetchone()
        if not user:
            raise HTTPException(404,"USER not found")
        return{"data":user}
    
@app.delete("/delete/{id:int}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    with get_connection as conn:
        with conn.cursor() as cursor:
            cursor.execeute("""DELETE FROM users WHERE ID =%s""",(id,))
            deleted=cursor.rowcount
            if deleted==0:
                raise HTTPException(status.HTTP_404_NOT_FOUND,"User not Found")
@app.get("/products")
def get_products():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            return {"data": cursor.fetchall()}
@app.post("/products", status_code=201)
def create_product(product: Product):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" INSERT INTO products(name,price)
                                VALUES(%s,%s)
                                RETURNING *
                                """,
                                (Product.name,product.price)
                            )
            return {"data":cursor.fetchone()}
@app.get("/products/{id}")
def get_product(id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM products WHERE id = %s",
                (id,)
            )
            product = cursor.fetchone()

    if not product:
        raise HTTPException(404, "Product not found")

    return {"data": product}
@app.delete("/products/{id}", status_code=204)
def delete_product(id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM products WHERE id = %s",
                (id,)
            )
            deleted = cursor.rowcount

    if deleted == 0:
        raise HTTPException(404, "Product not found")
@app.get("/purchases")
def get_purchases():
    with get_connection() as conn:   
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    purchases.id,
                    users.name AS username,
                    products.name AS product,
                    products.price,
                    purchases.quantity,
                    products.price * purchases.quantity AS total
                FROM purchases
                JOIN users ON purchases.user_id = users.id
                JOIN products ON purchases.product_id = products.id
                """
            )
            return {"data": cursor.fetchall()}
@app.post("/purchases", status_code=201)
def create_purchase(purchase: Purchase):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO purchases (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (
                    purchase.user_id,
                    purchase.product_id,
                    purchase.quantity
                )
            )
            return {"data": cursor.fetchone()}
@app.delete("/purchases/{id}", status_code=204)
def delete_purchase(id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM purchases WHERE id = %s",
                (id,)
            )
            deleted = cursor.rowcount

    if deleted == 0:
        raise HTTPException(404, "Purchase not found")
"""