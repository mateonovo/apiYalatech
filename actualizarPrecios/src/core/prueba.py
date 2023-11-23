import pyodbc

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-512OU1R\\SQLEXPRESS;DATABASE=PRODUCTOS;UID=DESKTOP-512OU1R\mateo;Trusted_Connection=yes;')
cursor = conn.cursor()

# Now you can execute queries using the cursor
cursor.execute("SELECT codigo FROM productos")
rows = cursor.fetchall()

# Iterate through the results and print the data
for row in rows:
    print(f"prod cod: {row.precio}")


def get_product_list():
    cursor.execute("SELECT codigo, nombre, precio FROM productos")
    rows = cursor.fetchall()
    products = []
    for row in rows:
        products.append({
            'barCode': row.codigo,
            'name': row.nombre,
            'commonPrice': float(row.precio)
        })
    return products

# Don't forget to close the cursor and connection when done
cursor.close()
conn.close()