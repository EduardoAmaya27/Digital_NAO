# Importamos librerias de trabajo
import os
import json
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Creamos constantes para el manejo de archivos de trabajo
DATA_PATH = '/content/'
FILE_PROCESSED = 'oilst_processed.csv'
FILE_GEODATA = 'brasil_geodata.json'

# Validamos que existan la ruta y los archivos
print(f'Ruta archivo proecesado: {os.path.join(DATA_PATH,FILE_PROCESSED)}')
print(f'Ruta archivo geodata: {os.path.join(DATA_PATH,FILE_GEODATA)}')

print(os.path.exists(os.path.join(DATA_PATH,FILE_PROCESSED)))
print(os.path.exists(os.path.join(DATA_PATH,FILE_GEODATA)))
#

# Cargamos el json regions.json
with open(os.path.join(DATA_PATH, FILE_GEODATA), 'r') as f:
    geodata = json.load(f)

# Creamos df de datos consolidados
columns_dates = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

df_consolidado = pd.read_csv(
    os.path.join(DATA_PATH, FILE_PROCESSED),
    parse_dates = columns_dates
    )

# Filtramos solo pedidos entregados y que tengan retraso prolongado
filtro = '(order_status == "delivered") & (delay_status == "long_delay")'
df_delivered_long_delay = df_consolidado.query(filtro)
df_delivered_long_delay.tail()
#

# creamos una agrupación por state_name y geolocation_state sumando las ventas
monetary_value_long_delays_by_state = df_delivered_long_delay.groupby(
    ['state_name', 'geolocation_state']).agg(
        {'total_sales': 'sum'}
    ).reset_index().\
    rename(columns={'total_sales': 'sales'}).\
    sort_values(by='sales')

