# Importamos librerias de trabajo
import os
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Consantes de archivo
DATA_PATH = '/content/'
FILE_PROCESSED = 'oilst_processed.csv'

# Validamos que exista el archivo
os.path.exists(os.path.join(DATA_PATH, FILE_PROCESSED))

# Creamos df de datos consolidados
columns_dates = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

df_procesado = pd.read_csv(
    os.path.join(DATA_PATH, FILE_PROCESSED),
    parse_dates=columns_dates
    )

# Creamos el df de ordenes terminadas
filtro = 'order_status == "delivered"'
df_delivered = df_procesado.query(filtro)
df_delivered.head()

# agrupamos por mes y anio  los pedidos con entrega prolongada
filtro_prolongado = 'delay_status == "long_delay"'
agrupado_prolongado = df_delivered.query(filtro_prolongado).\
    groupby(['year_month'])['order_id'].count().\
    reset_index().\
    rename(columns={'order_id': 'orders'})

# Cambiamos year_month a texto
agrupado_prolongado['period'] = agrupado_prolongado['year_month'].astype(str)

# graficamos la cantidad de ordenes con retraso prolongado por mes y 
# guardamos la imagen.
name_file_image = '3_d_evolution_delayed_orders_by_region.html'
x_label = 'Periodo'
y_label = 'Cantidad de pedidos'
title = 'Cantidad de pedidos con retraso prolongado por mes'

fig = px.bar(
    agrupado_prolongado,
    x='period',
    y='orders')

fig.update_layout(
    xaxis_title=x_label,
    yaxis_title=y_label,
    title=title
)
fig.write_html(name_file_image)
fig.show()
#