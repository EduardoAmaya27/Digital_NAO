# importamos librerias para la EDA
import os
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Recursos
DATA_PATH= "/content/"
FILE_CUSTOMERS= 'olist_customers_dataset.xlsx'
FILE_ORDERS= 'olist_orders_dataset.csv'
FILE_GEOLOCATIONS= 'olist_geolocation_dataset.csv'
FILE_ORDER_ITEMS= 'olist_order_items_dataset.csv'
FILE_ORDER_PAYMENTS= 'olist_order_payments_dataset.csv'
FILE_STATES_ABREVIATION= 'states_abbreviations.json'
FILE_REGIONS= 'brasil_regions.csv'
FILE_GEODATA= 'brasil_geodata.json'

# Probamos la existencia de los archivos imprimiendo sus rutas.
print(f"Ruta del archivo: {FILE_GEOLOCATIONS}")
print(os.path.join(DATA_PATH, FILE_GEOLOCATIONS))

# Creamos un df de cada uno de los archivos
df_customers = pd.read_excel(os.path.join(DATA_PATH, FILE_CUSTOMERS))
df_customers.info()
# cambiar el tipo de dato para customer_zip_code_prefix ya que de acuerdo al
# Anexo A es un tipo de dato numerico (texto)
df_customers['customer_zip_code_prefix'] = df_customers['customer_zip_code_prefix'].astype(str)
df_customers.info()
# Revisamos una muestra del df customers
df_customers.sample(10)
# Revisamos las primeras 5 filas del df customers
df_customers.head(5)
# Revisamos las ultimas 5 filas del df customers
df_customers.tail()
# valores unicos para cada una de las columnas
df_customers.nunique()
#Obtenemos un describe del df
df_customers.describe()

#creamos el df de lista de ordenes
df_olist_orders = pd.read_csv(os.path.join(DATA_PATH, FILE_ORDERS))
#Obtenemos info del df
df_olist_orders.info()

# De acuerdo al Anexo A los campos de fecha deben ser de tipo timestamp por lo que debemos convertirlos al formato esperado
# Creamos una lista de columnas de tipo timestamp
date_columns = ['order_purchase_timestamp',
                'order_approved_at',
                'order_delivered_carrier_date',
                'order_delivered_customer_date',
                'order_estimated_delivery_date'
                ]
#Aplicamos el formato
for col in date_columns:
  df_olist_orders[col] = pd.to_datetime(df_olist_orders[col],
                                        infer_datetime_format=True
                                        )
# Validamos que tengamos el nuevo formato
  df_olist_orders.info()
#Observamos el encabezado
df_olist_orders.head()
#Observamos las ultimas filas
df_olist_orders.tail()


# Columnas calculadas
#1.   year (anio en que se realiza el pedido)
#2.   month (mes en que se realiza el pedido)
#3.   quarter (trimestre en que se realiza el pedido)
#4.   year_month (anio y mes en que se realiza el pedido)
#5.   delta_days (dias transcurridos entre la fecha estimada de entrega y la   entrega efectiva del pedido)
#6.   delay_status (indica si no hubo retraso, si se trato de un retraso corto menor o igual a tres dias o uno largo, mayor a 3 dias)

#Iniciamos con las que solo requiere hacer un cast
df_olist_orders['year'] = df_olist_orders['order_purchase_timestamp'].dt.year
df_olist_orders['month'] = df_olist_orders['order_purchase_timestamp'].dt.month
df_olist_orders['quarter'] = df_olist_orders['order_purchase_timestamp'].dt.to_period('Q')
df_olist_orders['year_month'] = df_olist_orders['order_purchase_timestamp'].dt.to_period('M')

#validamos la creacion de las nuevas columnas
df_olist_orders[['order_id','year', 'month', 'quarter', 'year_month']]


#Crear la columna calculada delta_days que se conforma de la diferencia entre
#la columna order_delivered_customer_date y order_estimated_delivery_date
#calculamos en dias
df_olist_orders['delta_days'] = (df_olist_orders['order_delivered_customer_date'] -
                                 df_olist_orders['order_estimated_delivery_date']).dt.total_seconds()/ 60 / 60 / 24

df_olist_orders[['order_delivered_customer_date','order_estimated_delivery_date','delta_days']]

#Exploramos las estadisticas de la nueva columna
df_olist_orders['delta_days'].describe()

#Analizamos el top 5 de los pedidos en el que se entregaron antes de lo estimado
df_olist_orders[df_olist_orders['delta_days'] < 0].sort_values(by='delta_days',  ascending=True).head(5)

#Analizamos el top 5 de los pedidos en el que se entregaron más tarde de lo estimado
df_olist_orders[df_olist_orders['delta_days'] > 0].sort_values(by='delta_days',  ascending=False).head(5)

# Definir la columna delay_status donde un valor negativo en delta_days mayor a 0 dias 
# pero menor a 3 quiere decir que tiene un atraso de entrega dentro de lo aceptable,
# pero si delta_days es mayor a 3, significa que se tiene un atraso significativo
df_olist_orders['delay_status'] = np.where(
    df_olist_orders['delta_days'] > 3, 'long_delay',
    np.where(
        df_olist_orders['delta_days'] <= 0, 'on_time',
        'short_delay'
    )
)

df_olist_orders[['order_id','delta_days','delay_status']]

#Exploramos datos estadisticos de la nueva columna
df_olist_orders['delay_status'].describe()
#Valores distintos
df_olist_orders['delay_status'].value_counts()

#convertimos directamente la columna geolocation_zip_cod_prefix en tipo str
df_geolocations = pd.read_csv(os.path.join(DATA_PATH, FILE_GEOLOCATIONS), dtype={'geolocation_zip_code_prefix': 'str'})

#dado que es un df de codigos postales revisamos una estadistica la columna de codigo postal
df_geolocations['geolocation_zip_code_prefix'].describe()

# Dado que el CP para nuestro analisis debe ser unico podemos procedemos a crear un nuevo df
# en la que vamos a eliminar los registros duplicados del df basados por la columna geolocation_zip_code_prefix
df_unique_geolocations = df_geolocations.drop_duplicates(subset=['geolocation_zip_code_prefix'])
#El nuevo df ya tiene estrictamente valores unicos en la columna de CP
df_unique_geolocations.info()

# 2.4 Exploramos el archivo olist_order_items_dataset.csv
#Comprobamos la existencia del archivo
print(f"Ruta del archivo: {FILE_ORDER_ITEMS}")
print(os.path.join(DATA_PATH, FILE_ORDER_ITEMS))
os.path.exists(os.path.join(DATA_PATH, FILE_ORDER_ITEMS))
#Creamos el df
df_order_items = pd.read_csv(os.path.join(DATA_PATH, FILE_ORDER_ITEMS))

#Obtenemos la información relevante
df_order_items.info()


# El requerimiento solicita cantidad de productos que hay en la orden, por lo que debemos realizar un
# agrupamiento por order_id, realizando un count de la columna order_item_id.
# Adicional se solicita obtener el total del precio de la orden el cual es la sumatoria de la columna price

order_items_agg = df_order_items.groupby('order_id').agg({'order_item_id': 'count', 'price': 'sum'}).reset_index()
#renombramos columnas para dejarlas de acuerdo al requerimiento
order_items_agg.rename(columns={'order_item_id': 'total_products', 'price': 'total_sales'}, inplace=True)

#observamos de forma descendente las ordenes con mayor cantidad de productos
order_items_agg.sort_values(by='total_products', ascending=False)

# Exploramos el archivo olist_order_payments_dataset.csv
#validamos la existencia del archivo
print(f"Ruta del archivo: {FILE_ORDER_PAYMENTS}")
print(os.path.join(DATA_PATH, FILE_ORDER_PAYMENTS))
os.path.exists(os.path.join(DATA_PATH, FILE_ORDER_PAYMENTS))

#creamos el df
df_order_payments = pd.read_csv(os.path.join(DATA_PATH, FILE_ORDER_PAYMENTS))

# Exploramos el archivo states_abreviation.json

# Validamos la existencia del archivo
print(f"Ruta del archivo: {FILE_STATES_ABREVIATION}")
print(os.path.join(DATA_PATH, FILE_STATES_ABREVIATION))
os.path.exists(os.path.join(DATA_PATH, FILE_STATES_ABREVIATION))

#creamos el df
df_states_abreviation = pd.read_json(os.path.join(DATA_PATH, FILE_STATES_ABREVIATION))


# Exploramos el archivo brasil_regions.csv

#validamos que exista el archivo
print(f"Ruta del archivo: {FILE_REGIONS}")
print(os.path.join(DATA_PATH, FILE_REGIONS))
os.path.exists(os.path.join(DATA_PATH, FILE_REGIONS))

#creamos el df
df_regions = pd.read_csv(os.path.join(DATA_PATH, FILE_REGIONS))

# 2.8 Exploramos el archivo brasil_geodata.json
#validamos que exista el archivo
print(f"Ruta del archivo: {FILE_GEODATA}")
print(os.path.join(DATA_PATH, FILE_GEODATA))
os.path.exists(os.path.join(DATA_PATH, FILE_GEODATA))

#creamos el df
df_geodata = pd.read_json(os.path.join(DATA_PATH, FILE_GEODATA))

#Union de archivos para generar entregable

#Creamos un dataframe con la union de clientes y su geolocalizacion
df_customers_geo = pd.merge(df_customers,
                            df_unique_geolocations,
                            left_on='customer_zip_code_prefix',
                            right_on='geolocation_zip_code_prefix',
                            how='left')
df_customers.info()

# Podemos notar que en la union generamos la NaN para diferentes columnas unidas 
# y esto es debido a que en df_customers no especificamos que customer_zip_code_prefix debe ser
# de 5 digits dado que es un CP , por lo que hay que rellenar con cero a la izquierda aquellos 
# que tengan una longitud menor a 5.

# del df df_customers definir que la longitud de la columna customer_zip_code_prefix es de 5 digitos
# y que aquellos que sean menores a 5 rellenar con cero a la izquierda
df_customers['customer_zip_code_prefix'] = df_customers['customer_zip_code_prefix'].str.zfill(5)
df_customers.sample(10)

#Volvemos a crear el dataframe con la union de clientes y su geolocalizacion
df_customers_geo = pd.merge(df_customers,
                            df_unique_geolocations,
                            left_on='customer_zip_code_prefix',
                            right_on='geolocation_zip_code_prefix',
                            how='left')


df_customers_geo_estado = pd.merge(df_customers_geo,
                            df_states_abreviation,
                            left_on='geolocation_state',
                            right_on='abbreviation',
                            how='left')


# Lo siguiente es crear un df con las ordenes y total de articulos y  precios

#Unir df df_orders y items_agg por order_id
df_orders_totals = pd.merge(df_olist_orders,
                            order_items_agg,
                            left_on='order_id',
                            right_on='order_id',
                            how='left')


# Con estos dos df podemos tenemos las columnas solicitadas en el requerimiento por lo que podemos empezar a unirlos

# unimos los df df_orders_totals con df_customers_geo_estado por customer_id
df_results = df_orders_totals.merge(
    df_customers_geo_estado,
    on=['customer_id'],
    how='left'
    )

#Observamos las columnas
df_results.columns

# Exportamos el df al archivo de salida: **"oilst_processed.csv"

#Creamos el archivo
df_results.to_csv(os.path.join(DATA_PATH, 'oilst_processed.csv'), index=False)

#Validamos que se haya generado
print(f"Ruta del archivo: {os.path.join(DATA_PATH, 'oilst_processed.csv')}")
os.path.exists(os.path.join(DATA_PATH, 'oilst_processed.csv'))