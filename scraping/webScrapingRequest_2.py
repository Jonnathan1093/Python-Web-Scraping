import requests
from bs4 import BeautifulSoup
import re

url = "https://shopbermeohnos.com/product/kits-de-pesas-weider-hop-210lbs-olimpica" #Url de la pagina o producto
headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63"} #User agent o cabecera de peticion mediante un diccionario
res = requests.get(url, headers=headers) # Hacemos la peticion del request para no confundirse en headers el el argumento el el siguiente es la variable donde esta el diccionario - headers=headers

# print (res)

soup = BeautifulSoup(res.text,"html.parser") # Necesitamos 2 argumentos el codigo html y parser que es el metodo que va usar para crear el arbol de objetos

# print(soup.title.text) # Si queremos que nos devuelva solo el texto usamos text

sopa = soup.find("h1", class_="product_title entry-title").text.strip()
# Si agregamos el atributo text nos devolvera solo el string, y si usamos strip() nos permite limpiar el codigo en caso hay saltos de linea etc, lstrip() para los de la izquierda, y rstrip() para los de la derecha
print(sopa)

sopa1 = soup.find("p", class_="price").find("bdi").text.replace("$", "").replace(".", ",")
# Remplazamos ciertos argumentos
print(sopa1)

sopa2 = float(soup.find("ins").text.replace("$", ""))
print(sopa2)

sopa3 = float(soup.find("p", class_="price").text.replace("$", "").split()[0].strip())
# Split nos permite convertir un string en una lista o mas entendible obtener ambos valores en este caso
# De esta manera se muestra ambos precos 630 y 604, al poner [0] o [1] escogemos el precio a mostrar
print(f"precio anterior {sopa3}")

sopatotal = sopa3 - sopa2
print(f"El precio es de {sopatotal:.2f}") # Imprimir un float con dos decimales

# elementos = soup.find(class_="woocommerce-product-details__short-description").find_all("li")[0]
elementos = soup.find("div",class_="woocommerce-product-details__short-description").find_all("li")
# print(elementos)
# Para añadir 
plataformas = []

for elemento in elementos:
    plataformas.append(elemento.text.strip())
print(plataformas)

imagen = soup.find("img", {"class":"wp-post-image"}).attrs.get("src")
# Con un diccionario puedo obtner el mismo resulatado que de manera normal
# El attr es un atributo, en lo que nos devuelve un diccionario, es decir la clave es el atributo y como valor de la clave una lista con todos los valores en caso tenga mas de un valor
print(imagen)

