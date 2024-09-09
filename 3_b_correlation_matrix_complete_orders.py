# Importamos librerias
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Constantes de nuestro dataset
PATH = '/content/'
FILE_NAME = 'oilst_processed.csv'

# Validamos que existe el archivo
print(f'ruta: {PATH}{FILE_NAME}')
print(os.path.exists(os.path.join(PATH, FILE_NAME)))

#columnas que son de tipo fecha deben ser interpretadas como tal en el df
columns_dates = ['order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

df_processed = pd.read_csv(os.path.join(PATH, FILE_NAME),
                           parse_dates=columns_dates
                          )
df_processed.info()

#creamos un df con ordenes completadas
filtro = 'order_status == "delivered"'
df_orders_delivered = df_processed.query(filtro)
df_orders_delivered.info()

# creamos una lista de columnas numericas
columnas_numericas = df_orders_delivered.select_dtypes(include=[np.number]).columns.tolist()

#generamos la correlacion delta_days con todas las columnas
correlations = df_orders_delivered[columnas_numericas].corr()

#Creamos la figura
plt.figure(figsize=(10, 8)) 

sns.heatmap(correlations, 
            annot=True,
            cmap='coolwarm'
            ).set(
                title='Correlación para las órdenes en las que se concretó su entrega'
            )
plt.savefig('3_b_correlation_matrix_complete_orders.png')
plt.show()