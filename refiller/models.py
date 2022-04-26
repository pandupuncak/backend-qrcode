from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, String, Date, Text,Integer
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.ext.declarative import declarative_base
from refiller.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "pelanggan"

    id = Column(BigInteger, primary_key=True, index=True,autoincrement=True)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(255))
    password = Column(String(255))
    no_telp = Column(String(20))
    status = Column(String(10), nullable=True)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

class Order(Base):
    __tablename__ = "pesanan"

    id_user = Column(BigInteger, ForeignKey("pelanggan.id"))
    id_produk = Column(Integer, ForeignKey("product.id"))
    nama_pemesan = Column(String(255))
    no_telepon= Column(String(20), nullable=True)
    volume_produk = Column(Integer)
    total_harga = Column(Integer)
    status_pesanan = Column(String(255))
    id = Column(Integer, primary_key=True,autoincrement=True )

    #products = relationship("item_pesanan", back_populates="orders")

class Product(Base):
    __tablename__ = "product"

    nama_product = Column(String(255))
    harga = Column(Integer)
    deskripsi = Column(String(255))
    volume = Column(Integer)
    gambar = Column(String(255))
    id = Column(Integer, primary_key=True,autoincrement=True)


# class item_pesanan(Base):
#     __tablename__ = "product_orders"
    
#     id_pesanan = Column(BigInteger, ForeignKey("pesanan.id_pesanan"), primary_key=True)
#     id_produk = Column(BigInteger, ForeignKey("product.product_id"), primary_key=True)
#     kuantitas = Column(Integer)
#     total_harga_produk = Column(Integer)
#     notes = Column(Text, nullable=True)

#     orders = relationship("Order", back_populates="products")
