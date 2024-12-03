from dataclasses import dataclass


@dataclass
class Product:
    _id: str
    cat: str
    desc: str
    id: int
    img: str
    price: float
    title: str

