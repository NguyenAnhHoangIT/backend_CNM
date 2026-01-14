from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import get_db
from app.db.base import engine
from app.models import Base
from app.routers.product_router import router as product_router
from app.routers.user_router import router as user_router_router
from app.routers.cart_router import router as cart_router
from app.routers.role_router import router as role_router
from app.routers.category_router import router as category_router
from app.routers.invoice_router import router as invoice_router
from app.routers.voucher_router import router as voucher_router
from app.routers.upload_router import router as upload_router
from app.routers.chat_router import router as chat_router

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shop",
    description="shop",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)  
app.include_router(user_router_router)
app.include_router(cart_router)
app.include_router(role_router)
app.include_router(category_router)
app.include_router(invoice_router)
app.include_router(voucher_router)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/home")
async def root():
    return {"message": "Hello shop"}
