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
#creamos un df con ordenes completadas
filtro = 'order_status == "delivered"'
df_orders_delivered = df_processed.query(filtro)

# Implementa un programa que construya una visualización que permite
# observar la distribucion de la variable delta_days a lo largo de los
# estados de Brasil. Dicha visualización deberá segmentarse o 
# aperturarse de forma que permita revisar la variacion a traves
# diferentes valores del campo delay_status
titulo = 'Distribucion de delta_days por estado y tipo de retraso'
x_label = 'state_name'
y_label = 'delta_days'
segmentacion = 'delay_status'

sns.catplot(data = df_orders_delivered,
            x = x_label,
            y = y_label,
            hue = segmentacion,                             
            ).tick_params(axis = 'x',
                         labelrotation = 90)
            
plt.title(titulo)          
plt.savefig('3_c_delta_day_by_state_and_delay_type.png')
plt.show()
#


