import requests
import hashlib
from datetime import datetime
import pytz

# Función para generar el valor de veryText mediante MD5
def generate_very_text(key):
    china_tz = pytz.timezone('Asia/Shanghai')
    current_time_china = datetime.now(china_tz)
    current_date_only = current_time_china.strftime('%Y-%m-%d')
    text_to_encrypt = key + current_date_only
    md5_hash = hashlib.md5(text_to_encrypt.encode()).hexdigest()
    return md5_hash.lower()

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

# Datos del comerciante
merchant_code = "MC2574"
key = "c147DC65C0f9c0A"
bar_code = "bu"
# Obtener la lista de productos
product_list = get_product_list(merchant_code, key,bar_code)

print(f"Se encontraron {len(product_list)} productos.")
for product in product_list:
    print(f"BarCode: {product['barCode']}")
    print(f"Nombre: {product['name']}")
    print(f"Precio común: {product['commonPrice']}")
    print("-----")
