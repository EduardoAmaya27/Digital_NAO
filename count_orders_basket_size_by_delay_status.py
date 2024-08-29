# 1. Importamos librerias
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
#
# Datos del archivo a cargar
DATA_PATH = '/content/'
FILE_NAME = 'oilst_processed.csv'

# Cargamos archivo
#Validamos que exista el archivo
print(f'ruta del archivo: {DATA_PATH + FILE_NAME}')
os.path.exists(DATA_PATH + FILE_NAME)

# Creamos dataframe
df_oilst = pd.read_csv(DATA_PATH + FILE_NAME)
df_oilst.head()
df_oilst.info()
# Lista de columnas a interpretar como fecha
columns_dates=[
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

# Lectura del archivo csv
df_oilst = pd.read_csv(
    os.path.join(DATA_PATH, FILE_NAME),
    parse_dates=columns_dates
    )
df_oilst.info()

# Procesamos para obtener lo requerido

# Hacemos uso de crosstab para crear una tabla que nos muestre numero de ordenes por
# cantidad de productos dentro de la orden y el tipo de retraso de la categoria delay_status
pd.crosstab(
    df_oilst['total_products'],
    df_oilst['delay_status'],
    margins=True
    ).sort_values(by='long_delay').tail(10)

# Exportamos la tabla al archivo "count_orders_basket_size_by_delay_status.csv"
df_oilst.to_csv(
    os.path.join(DATA_PATH, 'count_orders_basket_size_by_delay_status.csv'),
    index=False
    )
#

#comprobamos que exista el archivo
os.path.exists(os.path.join(DATA_PATH, 'count_orders_basket_size_by_delay_status.csv'))
#