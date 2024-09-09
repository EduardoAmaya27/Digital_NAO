# Importamos librerias de trabajo
import os
import json
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
#

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
df_consolidado.info()

# Filtramos solo pedidos entregados y que tengan retraso prolongado
filtro = '(order_status == "delivered") & (delay_status == "long_delay")'
df_delivered_long_delay = df_consolidado.query(filtro)
df_delivered_long_delay.tail()
#

# creamos una agrupación por state_name y geolocation_state
delay_by_state = df_delivered_long_delay.groupby(
    ['state_name', 'geolocation_state']).agg(
        {'order_id': 'count'}
    ).reset_index().\
    rename(columns={'order_id': 'count_orders'}).\
    sort_values(by='count_orders')

# Creamos la figura relacionando properties.UF del json con
# geolocation_state del df agrupado
titulo = 'Mapa con cantidad de ordenes retrasadas por estado.'
labels = 'Cantidad de ordenes'
file_name_image = '3_e_map_long_delays_by_state.html'

fig = px.choropleth(
    data_frame=delay_by_state,
    geojson=geodata,
    featureidkey='properties.UF',    
    locations='geolocation_state',
    color='count_orders',    
    color_continuous_scale="Burgyl",
    scope='south america',
    labels={'count_orders': labels},
    hover_name='state_name',
    width=1600,
    height=800,
    title=titulo
)

# Actualizar diseño de la figura
fig.update_geos(
    showcountries=False,
    showcoastlines=True,
    showland=True,
    fitbounds='locations',
    visible=True
)

fig.update_layout(
    margin=dict(l=20, r=20, t=66, b=20),
    width=800,
    height=800,
)

fig.write_html(file_name_image)

# Mostrar figura
fig.show()

