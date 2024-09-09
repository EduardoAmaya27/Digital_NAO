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
# creamos el dataframe
df_processed = pd.read_csv(os.path.join(PATH, FILE_NAME))

#columnas que son de tipo fecha deben ser interpretadas como tal en el df
columns_dates = ['order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

df_processed = pd.read_csv(os.path.join(PATH, FILE_NAME),
    parse_dates=columns_dates)

print(df_processed.info())

# creamos el df que sea solo de ordenes entregadas y que tuvieron retrasos moderados y prolongados
filtro = '(order_status == "delivered") & (delay_status != "on_time")'

df_delivered = df_processed.query(filtro)

#creamos la figura
plt.figure(figsize=(10,6))
titulo = 'Fig.1 Órdenes completas que tuvieron retrasos moderados y prolongados'
x_label = 'delay_status'
y_label = 'Frecuencia'

sns.histplot(
    data = df_delivered['delay_status'],
    bins = 100
    )
plt.title(titulo)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.savefig('3_a_histogram_sales_short_long_delays.png')
plt.show()
#