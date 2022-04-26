from itertools import product
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.sql.expression import delete
from fastapi.responses import FileResponse

import database, generator
import models, schemas
from datetime import datetime, timedelta
from typing import Optional


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session):
    return db.query(models.Product).filter(models.Product.volume > 0).all()

# def get_item_order(db: Session, id_item: int, id_order: int):
#     return db.query(models.item_pesanan).filter((models.item_pesanan.id_pesanan == id_order) and 
#     (models.item_pesanan.id_produk == id_item))

def add_product(db: Session, produk: schemas.Produk):
    db_product = models.Product(nama_product = produk.nama_product, harga = produk.harga, deskripsi = produk.deskripsi, volume = produk.volume, gambar = produk.gambar)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id_pesanan == order_id).first()

# def get_order_items(db: Session, order_id: int, skip: int = 0, limit: int = 100):
#     return db.query(models.item_pesanan).filter(models.item_pesanan.id_pesanan == order_id).offset(skip).limit(limit).all()

def generate_qr(pemesan,produk,qty,harga):
    information = generator.info(pemesan,produk,qty,harga)
    img = information.create_qr()
    img.save('qr.png',format="png")
    return img

def create_order(db: Session, order: schemas.PesananCreate):
    product = get_product(db,order.id_produk)
    db_order = models.Order(id_user = order.id_user, id_produk = order.id_produk, nama_pemesan = order.nama_pemesan, no_telepon = order.no_telepon, 
                        volume_produk = order.volume_produk,total_harga = (order.volume_produk * product.harga), status_pesanan = order.status_pesanan)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# def create_item_order(db: Session, item: schemas.PayloadPesanan, pesanan: int):
#     harga_produk = item.kuantitas * (get_product(db,item.id_produk).harga)
#     db_item = models.item_pesanan(id_pesanan = pesanan, id_produk = item.id_produk, kuantitas= item.kuantitas, 
#     total_harga_produk = harga_produk, notes = item.notes) #update total harga
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)

#     update_item_stock(db,item.id_produk, -1)
    
#     return db_item

def update_item_volume(db: Session, item: int, vol: int):
    db_product = get_product(db,item)
    volume = db_product.volume + vol
    if(volume <= 0):
        volume = 0
    db.query(models.Product).filter(models.Product.id == item).update({"volume" : volume},synchronize_session="fetch")
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def update_order_status(db:Session, id_order: int, status_change: str):
    db_order = get_order(db, id_order)
    db.query(models.Order).filter(models.Order.id_pesanan == id_order).update({models.Order.status_pesanan : status_change}, synchronize_session = "fetch")
    db.commit()
    db.refresh(db_order)


def add_order_harga(db:Session, id_order: int, update_harga: int):
    db_order = get_order(db, id_order)
    harga_total = db_order.total_harga + update_harga
    db.query(models.Order).filter(models.Order.id_pesanan == id_order).update({"total_harga": harga_total}, synchronize_session = "fetch")
    db.commit()
    db.refresh(db_order)

    return db_order

def update_order(db: Session, order: schemas.PesananUpdate):
    db_order = get_order(db, order.id_pesanan)
    db.query(models.Order).filter(models.Order.id_pesanan == order.id_pesanan).update(dict(order))
    db.commit()
    db.refresh(db_order)
    return db_order

