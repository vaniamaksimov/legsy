from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from legsy.core import Base


class Size(Base):
    name: Mapped[str] = mapped_column(String(length=255), unique=True)

    goods: Mapped[list['GoodSize']] = relationship(back_populates='size')

    def __init__(self, name: str, goods: list['GoodSize'] = []):
        self.name = name
        self.goods = goods

    def __str__(self) -> str:
        return self.name


class GoodSize(Base):
    quantity: Mapped[int] = mapped_column(Integer)

    good: Mapped['Good'] = relationship(
        back_populates='sizes',
    )
    size: Mapped[Size] = relationship(
        back_populates='goods',
        lazy='joined'
    )

    good_id: Mapped[int] = mapped_column(
        ForeignKey('good.id', name='fk_goodsize_good_id')
    )
    size_id: Mapped[int] = mapped_column(
        ForeignKey('size.id', name='fk_goodsize_size_id'),
        nullable=False,
    )

    name: AssociationProxy[Size] = association_proxy('size', 'name')

    __table_args__ = (
        UniqueConstraint('good_id', 'size_id', name='unique_good_size'),
    )

    def __init__(self, quantity: int, good: 'Good', size: 'Size'):
        self.quantity = quantity
        self.good = good
        self.size = size

    def __str__(self) -> str:
        return f'Количество товара {self.good}'\
               f'размера {self.size}: {self.quantity}'


class GoodColor(Base):
    good: Mapped['Good'] = relationship(
        back_populates='colors'
    )
    color: Mapped['Color'] = relationship(
        back_populates='goods',
        lazy='joined',
    )

    good_id: Mapped[int] = mapped_column(
        ForeignKey('good.id', name='fk_goodcolor_good_id')
    )
    color_id: Mapped[int] = mapped_column(
        ForeignKey('color.id', name='fk_goodcolor_color_id'),
        nullable=False,
    )

    name: AssociationProxy['Color'] = association_proxy('color', 'name')

    __table_args__ = (
        UniqueConstraint('good_id', 'color_id', name='unique_good_color'),
    )

    def __init__(self, good: 'Good', color: 'Color'):
        self.good = good
        self.color = color

    def __str__(self) -> str:
        return f'Цвет товара {self.good}: {self.color}'


class Color(Base):
    name: Mapped[str] = mapped_column(String(length=255), unique=True)
    goods: Mapped[list[GoodColor]] = relationship(
        back_populates='color',
    )

    def __init__(self, name: str, goods: list['Good'] = []):
        self.name = name
        self.goods = goods

    def __str__(self) -> str:
        return self.name


class Brand(Base):
    name: Mapped[str] = mapped_column(String(length=255))
    brand_id: Mapped[int] = mapped_column(Integer, unique=True)
    site_brand_id: Mapped[int] = mapped_column(Integer)

    goods: Mapped[list['Good']] = relationship(
        back_populates='brand'
    )

    def __init__(self,
                 name: str,
                 brand_id: int,
                 site_brand_id: int,
                 goods: list['Good'] = []):
        self.name = name
        self.brand_id = brand_id
        self.site_brand_id = site_brand_id
        self.goods = goods

    def __str__(self) -> str:
        return self.name


class Good(Base):
    nm_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String(length=255))
    supplier_id: Mapped[int] = mapped_column(Integer)
    sale: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    sale_price: Mapped[int] = mapped_column(Integer)
    rating: Mapped[int] = mapped_column(Integer)
    feedbacks: Mapped[int] = mapped_column(Integer)

    brand: Mapped[Brand] = relationship(
        back_populates='goods',
        lazy='joined',
    )
    sizes: Mapped[list[GoodSize]] = relationship(
        back_populates='good',
        lazy='selectin',
        cascade='all, delete',
    )
    colors: Mapped[list[GoodColor]] = relationship(
        back_populates='good',
        lazy='selectin',
        cascade='all, delete'
    )

    brand_id: Mapped[int] = mapped_column(
        ForeignKey('brand.id', name='fk_good_brand',),
        nullable=False,
    )

    def __init__(self,
                 nm_id: int,
                 name: str,
                 supplier_id: int,
                 sale: int,
                 price: int,
                 sale_price: int,
                 rating: int,
                 feedbacks: int,
                 brand: Brand = None,
                 colors: list[Color] = [],
                 sizes: list[GoodSize] = []):
        self.nm_id = nm_id
        self.name = name
        self.supplier_id = supplier_id
        self.sale = sale
        self.price = price
        self.sale_price = sale_price
        self.rating = rating
        self.feedbacks = feedbacks
        self.colors = colors
        self.sizes = sizes
        self.brand = brand

    def __str__(self) -> str:
        return self.name
