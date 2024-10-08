
import requests
import json
import hashlib
from datetime import date
from datetime import datetime, date
import pytz
import time

def generate_very_text(key):
    china_tz = pytz.timezone('Asia/Shanghai')
    current_time_china = datetime.now(china_tz)
    current_date_only = current_time_china.strftime('%Y-%m-%d')
    text_to_encrypt = key + current_date_only
    md5_hash = hashlib.md5(text_to_encrypt.encode()).hexdigest()
    return md5_hash.lower()

# Código del comerciante y clave


# Generar el valor de veryText
very_text = generate_very_text(key)

# URL del endpoint para cambiar el precio
url = "http://sg.yalabi.net/open/goodsEditPrice"


# Datos del producto a actualizar
producto_a_actualizar = {
    "merchantGoodsId": "bu",  # Reemplaza con el ID del producto a actualizar
    "normalPrice": 690 # Reemplaza con el nuevo precio que deseas establecer
}

# Generar el valor de veryText
very_text = generate_very_text(key)

# Crear la solicitud con los parámetros requeridos
data = [producto_a_actualizar]
headers = {
    "veryText": very_text,
    "merchantCode": merchant_code,
    "content-type": "application/json"
}
# Realizar la solicitud POST a la API de YalaTech
response = requests.post(url, data=json.dumps(data), headers=headers)

# Procesar la respuesta
if response.status_code == 200 and response.json().get("success"):
        print("Precio actualizado con éxito.")
else:
    error_msg = response.json().get("errorMsg")
    print(f"Error al actualizar el precio: {error_msg}")
