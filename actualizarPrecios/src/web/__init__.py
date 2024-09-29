from flask import Flask, render_template, request, jsonify
import json
import requests
import hashlib
from datetime import datetime
from flask import current_app as app
import pytz
from src.web.config import config
import pyodbc
from src.core import database
import logging

logging.basicConfig(level=logging.INFO)


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-512OU1R\\SQLEXPRESS;DATABASE=PRODUCTOS;UID=DESKTOP-512OU1R\mateo;Trusted_Connection=yes;')
    
    def generate_very_text(key):
        china_tz = pytz.timezone('Asia/Shanghai')
        current_time_china = datetime.now(china_tz)
        current_date_only = current_time_china.strftime('%Y-%m-%d')
        text_to_encrypt = key + current_date_only
        md5_hash = hashlib.md5(text_to_encrypt.encode()).hexdigest()
        return md5_hash.lower()

    def get_product_list():
        url = "http://sg.yalabi.net/open/getGoodsList"
        very_text = generate_very_text(key)
        headers = {
            "veryText": very_text,
            "merchantCode": merchant_code,
            "content-type": "application/json"
        }
        data = {"pageSize": 1000
             }
    
        response = requests.post(url, json=data, headers=headers)
    
        if response.status_code == 200 and response.json().get("success"):
            product_list = response.json().get("data").get("list")
            return product_list
        else:
            error_msg = response.json().get("errorMsg")
            print(f"Error al obtener la lista de productos: {error_msg}")
            return []
    
   
    def get_product_list_bd():
        cursor = conn.cursor()
        with cursor:
            cursor.execute("SELECT codigo,precioIva FROM tblArticulos")
            products = []
            for row in cursor.fetchall():
                products.append({
                    'barCode': row.codigo,
                    'commonPrice': float(row.precioIva)
                }) 
        return products
    
    
    def cambiarPrecio(barCode, product_price):
        merchant_code = ""
        key = ""
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
        print(data)
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
            print(response.json())
            if response.json().get("success"):
                logging.info("Precio actualizado con éxito en el producto: %s", barCode)
            else:
                error_msg = response.json().get("errorMsg")
                logging.error("Error al actualizar el precio: %s", error_msg)
        except requests.exceptions.RequestException as e:
            logging.error("Error en la solicitud: %s", e)
        except json.decoder.JSONDecodeError as e:
            logging.error("Error al decodificar JSON: %s", e)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")
    

 
    @app.route("/update", methods=["POST"])
    def update_prices():
        product_list = get_product_list()
        #print(product_list)
        actualizados = []
        cursor = conn.cursor()
        with cursor:
            bd = get_product_list_bd()
        #print(bd)
        for product in product_list:
            barCode = product['barCode']
            product_price = product['commonPrice']
            product_name = product['name']
            for bd_product in bd:
                 if bd_product['barCode'] == barCode and bd_product['commonPrice'] != product_price:
                     #print(f"Coincidencia encontrada para {barCode}. Precio en bd: {bd_product['commonPrice']}, Precio del producto: {product_price}")
                     product = {
                             'barCode': barCode,
                             'name': product_name,
                             'price': float(bd_product['commonPrice'])
                            }    
                     actualizados.append(product)          
                     cambiarPrecio(barCode, product["price"])                                
        return jsonify({"message": "Precios actualizados y leídos con exitoooooo","actualizados":  actualizados})
    
    
    
    
    merchant_code = ""
    key = ""
    very_text = generate_very_text(key)  
    return app
