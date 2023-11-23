from src.core.producto import Producto
from src.core.database import database as db




def create_product(product_name, product_price, barCode):
    """
    Crea un nuevo producto en la base de datos
    """
    product = Producto(product_name, product_price, barCode)
    db.session.add(product)
    db.session.commit()
    return product
    
    



def get_product_list():
    """
    Obtiene la lista de productos de la base de datos
    """
    product_list = Producto.query.all()
    return product_list