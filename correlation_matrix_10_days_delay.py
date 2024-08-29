# Importamos librerias
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
#

# Declaramos variables estaticas de ruta y nombre archivo
DATA_PATH = '/content/'
DATA_FILE = 'oilst_processed.csv'

# Validamos que existe el archivo
print(os.path.exists(DATA_PATH + DATA_FILE))
# Creamos df
df_processed = pd.read_csv(DATA_PATH + DATA_FILE)
df_processed.head()
#Obtenemos info del df
df_processed.info()

#Creamos lista de columnas que deben ser tipo fecha
columns_dates=[
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

# Creacion del df con el parseo de las fechas
df_processed = pd.read_csv(
    os.path.join(DATA_PATH, DATA_FILE),
    parse_dates=columns_dates
    )
df_processed.info()

#Requerimiento
#calcule la matriz de correlacion entre las variables total_sales,
#total_products, delta_days y distance_distribution_center para
#ordenes completadas que cuya fecha de entrega sobrepasa los 10 dias
#de la fecha estimada para la entrega. El resultado de este script
#debera ser una figura denominada correlation_matrix_10_days_delay.png

# Primero creamos el df con solo pedidos completados y que la fecha de
# entrega sobrepasa 10 dias.
df_completed = df_processed.query('(order_status == "delivered") and (delta_days >10)')
df_completed.head()

# Obtenemos info del nuevo df
df_completed.info()

#Lista de columnas a validar si tienen correlacion
columns_corr = [
    'total_sales',
    'total_products',
    'delta_days',
    'distance_distribution_center'
    ]
#
#Usamos el metodo .corr de pandas
matriz = df_completed[columns_corr].corr().round(4)
matriz
#

#creamos una figura para plasmar la correlacion
plt.figure(figsize=(10,10))
sns.heatmap(matriz, annot=True)
plt.savefig('correlation_matrix_10_days_delay.png')
plt.show()
#