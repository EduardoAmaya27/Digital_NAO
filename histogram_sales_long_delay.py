
# Importamos Librerias


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 2. Validamos que exista el archivo

PATH = '/content/'
FILE_NAME = 'oilst_processed.csv'

print(f'Validamos que exista la ruta {PATH}{FILE_NAME}')
os.path.exists(f'{PATH}{FILE_NAME}')

#Creamos el df

df_oilst = pd.read_csv(f'{PATH}{FILE_NAME}')
df_oilst.head()

df_oilst.info()

#Creamos lista de columnas que deben ser tipo fecha
columns_dates=[
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

# Creacion del df con el parseo de las fechas
df_oilst = pd.read_csv(
    os.path.join(PATH, FILE_NAME),
    parse_dates=columns_dates
    )

#Obtenemos info del df
df_oilst.info()
#

#Obtenemos info del df
df_oilst.sample(5)
#

#Primero debemos generar un df de puras ordenes terminadas.
df_delivered = df_oilst.query("order_status  == 'delivered' ")
df_delivered
#
#La regla empirica debil para encontrar el 88.88% de datos alrededor del promedio es el intervalo definido por la media y tres veces la desviacion estandar.
# titulo y etiquetas
titulo = 'Histograma de frequencias de delta_days'
x_label = 'Diferencia tiempo estimado - tiempo real entrega'
y_label = 'Frecuencia'
# Variable para guardar la grafica
FILE_GRAFICA = 'histogram_sales_long_delay.png'
# creamos el subplot
fig, ax = plt.subplots(figsize=(10, 5))
# numero de intervalos para conteos
n_bins = 100
# creacion del objeto historgama
n, bins, patches = ax.hist(
    df_delivered['delta_days'],
    n_bins
    )
#Establecemos titulo y ejes "x" y "y"
ax.set_title(titulo )
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
# Obtenemos la media
media = df_delivered['delta_days'].mean()
# Obtenemos 3 veces la desviacion estandar
x3_desviacion = 3 * df_delivered['delta_days'].std()
# Linea para la media la cual identificaremos de color rojo
plt.axvline(
    media,
    color='r',
    linestyle='dashed',
    linewidth=3)
# Linea para la media + 3 veces la desviacion estandar la cual identificaremos color amarillo
plt.axvline(
    media + x3_desviacion,
    color='y',
    linestyle='dashed',
    linewidth=2)
# Linea para la media - 3 veces la desviacion estandar la cual identificaremos color amarillo
plt.axvline(
    media - x3_desviacion,
    color='y',
    linestyle='dashed',
    linewidth=2)
# limites de la figura
min_ylim, max_ylim = plt.ylim()
# Etiquetas
plt.text(
   media *1.1,
    max_ylim*0.9,
    'Promedio: {:.2f}'.format(media)
    )

print(f'min_ylim {min_ylim}')
print(f'max_ylim {max_ylim}')
print(f'media {media}')
print(f'x3_desviacion {x3_desviacion}')
plt.savefig(f'{PATH}{FILE_GRAFICA}', bbox_inches='tight')
plt.show()