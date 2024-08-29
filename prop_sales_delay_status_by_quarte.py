# Importamos librerias de trabajo
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
#

# Lectura de datos
# Trabajaremos con el archivo consolidado creado en el primer requerimiento del Sprint 1.

#Carpeta donde se encuentran los recursos
DATA_PATH = '/content/'
FILE_OLIST_PROCESSED = 'oilst_processed.csv'

# Validamos que exista el archivo
print(f'ruta de archivo: {DATA_PATH}{FILE_OLIST_PROCESSED}')
os.path.exists(f'{DATA_PATH}{FILE_OLIST_PROCESSED}')

# Crearemos un un dataframe del archivo consolidado.
df_oilst = pd.read_csv(f'{DATA_PATH}{FILE_OLIST_PROCESSED}')

#Lista de columnas que son de tipo fecha
colums_date = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

# Lectura del archivo csv
df_oilst = pd.read_csv(
    os.path.join(DATA_PATH, FILE_OLIST_PROCESSED),
    parse_dates=colums_date
    )



# creamos un df de puros pedidos entregados
df_delivered = df_oilst.query('order_status == "delivered"')

# Agrupamos por estatus la cantidad de pedidos entregados.
df_delivered.groupby(['delay_status'])['delay_status'].count()

# Creamos una tabla pivote donde las filas seran los estatus de entrega,
# las columnas los trimestres y los valores serán el total de ventas por el trimestre.

df_delivered.pivot_table(
    index='delay_status',
    columns = 'quarter',
    values= 'total_sales',
    aggfunc= 'sum',
    fill_value=0
    )

# Ahora obtenemos la proporcion (%) que representa cada estatus.

#Creamos tabla pivote para obtener el porcentaje de cada trimestre por estatus.
df_pivot = df_delivered.pivot_table(
    index='delay_status',
    columns = 'quarter',
    values= 'total_sales',
    aggfunc= 'sum',
    fill_value=0
    ).apply	(lambda x: x / float(x.sum()), axis=0).round(2)
df_pivot

# Mulitiplicamos por 100 para obtener el porcentaje
df_pivot = df_pivot * 100
#

# Exportamos la tabla a archivo "prop_sales_delay_status_by_quarte.csv"
#Exportamos tabla a archivo
df_pivot.to_csv('prop_sales_delay_status_by_quarte.csv')
#validamos que se haya creado el archivo.
os.path.exists('prop_sales_delay_status_by_quarte.csv')