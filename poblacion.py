# 4.	Censo de Población y Vivienda 2010:
# a.	Periodicidad: Cada 10 años
# b.	Liga: https://www.inegi.org.mx/programas/ccpv/2010/default.html#Tabulados


# EJEMPLO CON LA POBLACIÓN

# IdIndicador
# El primer paso que se debe realizar para obtener información de la API es seleccionar el indicador e identificar su clave. Esto lo puede realizar consultando el "Constructor de consultas".

# Idioma
# La información está disponible en español [es] e inglés [en].

# Área geográfica
# Puede ser nacional [00], por entidad federativa [99] o por municipio [999], dependiendo de cada indicador.

# Dato más reciente o Serie histórica
# Puede consultarse solo el dato más reciente [true] o la serie histórica completa [false].

# Fuente de datos
# Corresponde a la fuente de diseminación [BISE] o [BIE] de donde se obtendrán los datos consultados.

# Versión
# Con él se identificará la edición [2.0] del servicio de provisión de datos.

# Token
# Para utilizar la API es necesario mandarle un token válido, el cual puede obtener al registrarse aquí.

# Formato
# Se ofrece la información en 3 tipos de formatos: JSON [json], JSONP [jsonp] o XML [xml].


#Llamado al API
# Poblacion de hombres y mujeres en la misma página (NO FUNCIONA BIEN, DESCARGA LOS MISMO DATOS PARA PARA HOMBRES EL DE LAS MUJERES)
# url = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000002,1002000003/es/0700/false/BISE/2.0/'+token_INEGI+'?type=json'


# Librerias

import pandas as pd
import numpy as np
import requests
import json
import time

start_time=time.time() # Inicio del tiempo 


token_INEGI="" # AQUI DEBE IR EL TOKEN PROPORCIONADO POR EL INEGI se obtiene en: http://www3.inegi.org.mx//sistemas/api/indicadores/v1/tokenVerify.aspx

# Areas geograficas (estados)
Area_geo=['01','02','03','04','05','06','07','08','09'] + list(range(10,33)) 
# Genera un DataFrame auxiliar para ir llenandolo de la informacion
df1=pd.DataFrame([], columns=['Ano', 'Total', 'Hombre', 'Mujer'])

# Saca los datos usando la API del INEGI para cada entidad
for n in Area_geo:

  print("Entidad: ", n)
  # Poblacion hombres
  url_h = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000002/es/'+str(n)+'/false/BISE/2.0/'+token_INEGI+'?type=json'
  response_1= requests.get(url_h)
  # Poblacion mujeres
  url_m = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000003/es/'+str(n)+'/false/BISE/2.0/'+token_INEGI+'?type=json'
  response_2= requests.get(url_m)
  
    
  # Si respondio bien el servidor continua
  if (response_1.status_code==200) and (response_2.status_code==200):
    
      # transforma los datos a json
      content_1= json.loads(response_1.content)
      content_2= json.loads(response_2.content)
      # extrae los anos y los datos
      Tiempo=content_1['Series'][0]['OBSERVATIONS']
      Anos=[obs['TIME_PERIOD'] for obs in Tiempo]
      # Serie hombres
      Series_1=content_1['Series'][0]['OBSERVATIONS']
      Serie_1=[float(obs['OBS_VALUE']) for obs in Series_1]
      # Serie mujeres
      Series_2=content_2['Series'][0]['OBSERVATIONS']
      Serie_2=[float(obs['OBS_VALUE']) for obs in Series_2]
                      
       # Diccionario para crear el data frame    
      df_1 = {'Ano': Anos,
              'Total': np.array(Serie_1)+np.array(Serie_2),
              'Hombre': Serie_1,
              'Mujer': Serie_2,
              }
      # Crea el data frame
      df = pd.DataFrame(df_1)
      # concatena los datos
      df1 = pd.concat([df1,df], axis=0)
      
# Nombre de las entidades para agregarlas al data frame ya que los datos
# extraidos no traen los nombres
entidades=['Aguascalientes',
 'Baja California',
 'Baja California Sur',
 'Campeche',
 'Coahuila de Zaragoza',
 'Colima',
 'Chiapas',
 'Chihuahua',
 'Distrito Federal',
 'Durango',
 'Guanajuato',
 'Guerrero',
 'Hidalgo',
 'Jalisco',
 'México',
 'Michoacán de Ocampo',
 'Morelos',
 'Nayarit',
 'Nuevo León',
 'Oaxaca',
 'Puebla',
 'Querétaro',
 'Quintana Roo',
 'San Luis Potosí',
 'Sinaloa',
 'Sonora',
 'Tabasco',
 'Tamaulipas',
 'Tlaxcala',
 'Veracruz de Ignacio de la Llave',
 'Yucatán',
 'Zacatecas']
      
      
# Crea los DataFrames para cada ano y los guarda en csv

df_1995 = df1[df1["Ano"]=="1995"]
df_1995.insert (1, "Entidad", entidades)
df_1995.to_csv("Poblacion_1995.csv", index=False, encoding="latin_1")


df_2000 = df1[df1["Ano"]=="2000"]
df_2000.insert (1, "Entidad", entidades)
df_2000.to_csv("Poblacion_2000.csv", index=False, encoding="latin_1")


df_2005 = df1[df1["Ano"]=="2005"]
df_2005.insert (1, "Entidad", entidades)
df_2005.to_csv("Poblacion_2005.csv", index=False, encoding="latin_1")


df_2010 = df1[df1["Ano"]=="2010"]
df_2010.insert (1, "Entidad", entidades)
df_2010.to_csv("Poblacion_2010.csv", index=False, encoding="latin_1")

    
      
# Fin del tiempo 
end_time=time.time()

time_in_minutes = float(end_time-start_time)/60
print("Tiempo transcurrido en minutos: ", time_in_minutes)


df_2010 