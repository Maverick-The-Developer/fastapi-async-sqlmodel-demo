from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import insert, select, update, delete
from typing import List
from models import Product
from database import get_session, init_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    if engine is not None:
        print("##### Closing database connection #####")
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/products/")
async def create_product(
    product: Product, session: AsyncSession = Depends(get_session)
):
    try:
        insert_data = product.model_dump(exclude_none=True)
        stmt = insert(Product).values(**insert_data)
        # session.add(product)
        result = await session.execute(stmt)
    except Exception as e:
        print(e)
        await session.rollback()
    finally:
        await session.commit()
        print(result.inserted_primary_key)
    return {"new_product_id": result.inserted_primary_key[0], "message": "Product created successfully"}


@app.get("/products/", response_model=List[Product])
async def listup_products(session: AsyncSession = Depends(get_session)):
    stmt = select(Product).order_by(Product.name)
    product_list = await session.execute(stmt)
    return product_list.scalars().all()


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int, product: Product, session: AsyncSession = Depends(get_session)
):
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product_db = result.scalar_one_or_none()
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    # if product.name:
    #     product_db.name = product.name
    # if product.description:
    #     product_db.description = product.description
    # if product.price:
    #     product_db.price = product.price
    # if product.stock:
    #     product_db.stock = product.stock
    update_data = product.model_dump(exclude_unset=True)
    # for key, value in update_data.items():
    #     setattr(product_db, key, value)

    # session.add(product_db)
    stmt = update(Product).where(Product.id == product_id).values(**update_data)
    await session.execute(stmt)
    await session.commit()
    await session.refresh(product_db)
    return product_db


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    stmt = delete(Product).where(Product.id == product_id)
    await session.execute(stmt)
    # await session.delete(product)
    await session.commit()
    return {"message": "Product deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
