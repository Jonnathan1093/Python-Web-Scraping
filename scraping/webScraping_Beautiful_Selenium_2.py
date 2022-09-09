from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

ruta = ChromeDriverManager(path="./chromedriver").install() # Como parametro indicamos la ruta donde queremos que se instale webdriver
# Se instalara en el directorio actual en una carpeta llamada chromedriver
# print(ruta) # Si imprimimos, obtenemo la ruta donde se instalo

# Instanciamos el servicio de chromedriver, y tambien instanciamos en una variable
s = Service(ruta) 
# Instanlamos selenium pasando como argumento service
driver = webdriver.Chrome(service=s) 
# Guardamos en una variable la url a scrapear
url ="https://www.pccomponentes.com/pccom-revolt-one-3060-intel-core-i7-11800h-16gb-1tb-ssd-rtx-3060-156"
# Al igual que request hacemos la peticion 
driver.get(url)
# Puede surgir un problema al abrir el chrome driver, esta ventana se abrira y cerrara automaticamente, como solucion se implementa un input
# input("Esperando que no se cierre webdriver: ")
# Podemos acceder al codigo html de la pagina de la siguiente manera
soup = BeautifulSoup(driver.page_source, "html.parser")
# Procedemos a extraer la informacion como antes

sopa = soup.find("div", class_="articulo").text
print(f"Imprime el nombre del producto: {sopa}")
driver.quit()


