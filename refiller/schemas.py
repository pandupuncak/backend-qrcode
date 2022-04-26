from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel

class ProdukBase(BaseModel):
    nama_product: str
    harga: int
    deskripsi: str
    volume: int
    gambar: str

class Produk(ProdukBase):
    id : int
    class Config:
        orm_mode = True

# class ItemPesananBase(BaseModel):
#     id_produk : int
#     id_pesanan: int
#     kuantitas: int
#     notes: Optional[str]

# class ItemPesanan(ItemPesananBase):
#     total_harga_produk: int
#     class Config:
#         orm_mode = True

class PesananBase(BaseModel):
    id_user: int
    nama_pemesan: str
    no_telepon: int
    total_harga: int = 0
    status_pesanan : str = "Accepted"


# class PayloadPesanan(BaseModel):
#     id_produk: int
#     kuantitas: int
#     notes: Optional[str]
    

class PesananCreate(PesananBase):
    id_produk : int
    volume_produk: int
    #produk : List[PayloadPesanan]

class PesananUpdate(PesananBase):
    id_pesanan: int

class Pesanan(PesananBase):
    id: int
    class Config:
        orm_mode = True

class Item(BaseModel):
    pemesan : str
    option : str
    qty : int
    price : int