import requests
import json
import hashlib
from datetime import date,datetime
import pytz

def generate_very_text(key):
    china_tz = pytz.timezone('Asia/Shanghai')
    current_time_china = datetime.now(china_tz)
    current_date_only = current_time_china.strftime('%Y-%m-%d')
    text_to_encrypt = key + current_date_only
    md5_hash = hashlib.md5(text_to_encrypt.encode()).hexdigest()
    return md5_hash.lower()

def read_products_from_txt(filename):
    products = []
    with open(filename, 'r') as file:
        for line in file:
            product_data = line.strip().split(',')
            if len(product_data) == 3:
                barCode, product_name, product_price = product_data
                product_price = float(product_price)
                list= get_product_list(merchant_code, key, barCode)
                producto = match_product_by_bar_code(list,barCode)            
                if producto['barCode']== barCode:
                     if product_price != producto['commonPrice']:
                        cambiarPrecio(barCode,product_price)
                     else:    
                         print("El precio no se ha modificado")    
                product = {
                    'barCode': barCode,
                    'name': product_name,
                    'price': float(product_price)
                }
       
                products.append(product)
                print(f"Producto leído: {product}")
    return products

def get_product_list(merchant_code, key,barCode):
    url = "http://sg.yalabi.net/open/getGoodsList"
    very_text = generate_very_text(key)
    headers = {
        "veryText": very_text,
        "merchantCode": merchant_code,
        "content-type": "application/json"
    }
    data = { 'barCode' : barCode
         }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200 and response.json().get("success"):
        product_list = response.json().get("data").get("list")
        return product_list
    else:
        error_msg = response.json().get("errorMsg")
        print(f"Error al obtener la lista de productos: {error_msg}")
        return []


def match_product_by_bar_code(product_list, bar_code):
    matching_product = None
    for product in product_list:
        if product['barCode'] == bar_code:
             matching_product = product
             break
    return matching_product

def cambiarPrecio(barCode, product_price):
    url = "http://sg.yalabi.net/open/goodsEditPrice"
    very_text = generate_very_text(key)
    producto_a_actualizar = {
       
        "merchantGoodsId": barCode,
        "normalPrice": product_price,
    }
    data = [producto_a_actualizar]
    headers = {
        "veryText": very_text,
        "merchantCode": merchant_code,
        "content-type": "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200 and response.json().get("success"):
        print("Precio actualizado con éxito. en el producto:" ,{barCode})
    else:
        error_msg = response.json().get("errorMsg")
        print(f"Error al actualizar el precio: {error_msg}")

    
merchant_code = ""
key = ""
very_text = generate_very_text(key)
database_filename = 'database.txt'
read_products_from_txt(database_filename)
