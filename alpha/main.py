from fastapi import FastAPI
from .routers import user, product, purchase

app = FastAPI()

app.include_router(user.router)
app.include_router(product.router)
app.include_router(purchase.router)