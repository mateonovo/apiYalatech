import pyodbc



conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-512OU1R\SQLEXPRESS;DATABASE=PRODUCTOS;UID=DESKTOP-512OU1R\mateo;')
cursor = conn.cursor()


print('connection successful')
cursor.execute('SELECT * FROM productos')