import string
from dataclasses import dataclass


@dataclass
class Product:
    _id: string
    cat: string
    desc: string
    id: int
    img: string
    price: float
    title: string

