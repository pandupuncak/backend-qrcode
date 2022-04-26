from http.client import responses
from typing import Dict, List

from sqlalchemy.util.langhelpers import NoneType
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from refiller import crud, models, schemas
from database import get_db, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.responses import FileResponse
import io
from starlette.responses import StreamingResponse

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI(title="Refiller")

@app.get("/orders/{id_order}", response_model=schemas.Pesanan, tags=["getters"])
def get_order(id_order: int, db: Session = Depends(get_db)):
    return crud.get_order(db,id_order)

@app.get("/products/{id_product}")
def get_product(id_product:int, db: Session = Depends(get_db), tags=["getters"]):
    return crud.get_product(db,id_product)

@app.get("/products/", response_model = List[schemas.Produk], tags=["getters"])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

# @app.get("/order_items/{id_order}", response_model = List[schemas.ItemPesanan], tags=["getters"])
# def get_order_items(id_order: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.get_order_items(db,id_order)
# def get_order_items()

@app.post("/product",response_model = schemas.Produk, tags=["products"])
def insert(produk: schemas.ProdukBase, db: Session = Depends(get_db)):
    product = crud.add_product(db,produk)
    return product;

@app.patch("/products/", response_model = schemas.Produk, tags=["products"])
def update_volume(produk_id : int, volume : int, db: Session = Depends(get_db)):
    product = crud.update_item_volume(db,produk_id,volume)# tambahin exception kalau salah
    return product

@app.post(
    "/orders/", 
    response_model = schemas.Pesanan,
    responses = {
        200: {
            "content" : {"image/png" : {}},
            "description" : "Return the JSON item or an image"
        }
    }, 
    tags=["order"])
async def order(pesanan : schemas.PesananCreate,db: Session = Depends(get_db)):
    
    if not (pesanan.volume_produk > 0):
        raise HTTPException(status_code=403, detail="No volume input given")

    if (crud.get_product(db,pesanan.id_produk).volume <= 0):
        raise HTTPException(status_code=404, detail = "There's no product left in this machine, please pick another one or cancel your order")
    db_order = crud.create_order(db,pesanan)

    # db_product = crud.update_item_volume(db, pesanan.id_produk,(-pesanan.volume_produk)

    if db_order is None:
        raise HTTPException(status_code=404, detail= "Order details invalid")

    image = crud.generate_qr(db_order.nama_pemesan, db_order.id_produk , db_order.volume_produk, db_order.total_harga)

    
    # db_orderitems = []
    # for item in pesanan.produk:
    #     item_ordered = crud.create_item_order(db, item, db_order.id_pesanan)
    #     if pesanan.total_harga == 0:
    #         crud.add_order_harga(db,db_order.id_pesanan,item_ordered.total_harga_produk)
    #     db_orderitems.append(item_ordered)
    # if (hasattr(pesanan,"id_benefit") and (pesanan.id_benefit != None)):
    #     db_order = crud.apply_benefit(db,db_order.id_pesanan,pesanan.id_benefit) #Update Schemanya
    if image:
        return FileResponse("qr.png", media_type="image/png")
    else:
        return db_order

@app.patch("/orders/", response_model = schemas.Pesanan, tags=["order"])
def update_order(update : schemas.PesananUpdate, db: Session = Depends(get_db)):
    orders = crud.update_order(db,update)# tambahin exception kalau salah
    return orders

@app.patch("/orders/{harga}", response_model = schemas.Pesanan, tags=["order"])
def update_order(id_pesanan: int, update_harga : int, db: Session = Depends(get_db)):
    db_order = crud.add_order_harga(db,id_pesanan, update_harga)
    return db_order

# @app.patch("/orders/status", response_model = dict, tags=["order"])
# def update_order(update : schemas.PesananUpdate, db: Session = Depends(get_db)):
#     orders = crud.update_order(db,update)# tambahin exception kalau salah
#     return orders