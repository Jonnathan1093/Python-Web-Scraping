# para instalar automáticamente chromedriver
from webdriver_manager.chrome import ChromeDriverManager
# driver de selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# beautifulsoup
from bs4 import BeautifulSoup

# instalamos la versión de chromedriver correspondiente . Nos devuelve la ruta completa del ejecutable
ruta_chromedriver = ChromeDriverManager(path='./chromedriver').install()
# instanciamos el servicio de chromedriver
s = Service(ruta_chromedriver)
# instanciamos webdriver de selenium con chrome
driver=webdriver.Chrome(service=s)
# url de la petición
url="https://www.pccomponentes.com/alurin-go-intel-pentium-n4200-8gb-128gb-ssd-nos-141"
# abrimos la página
driver.get(url)
# preparamos la sopa
soup=BeautifulSoup(driver.page_source, "html.parser")
# extraemos los datos
# nombre del producto
nombre_producto=soup.find("div", class_="articulo").text
    # precio anterior
precio_antes = soup.find("del", class_="original-price-nodiscount").text
    #  precio actual
precio_ahora = soup.find(id="precio-main").text
    #  url de la imagen del producto
url_imagen = " https: " + soup.find("img", class_="pc-com-zoom").attrs.get("src")
# categoría
categoria = soup.find("div", class_="navegacion-secundaria__migas-de-pan").find_all("a", class_="GTM-breadcumb")[-1].text
# [-1] tomamos el ultimo valor
# ID del producto
id_producto = soup.find(id="codigo-articulo-pc").text
# mostramos los datos obtenidos
print (" NOMBRE PRODUCTO: ", nombre_producto)
print (" ID ............: ", id_producto)
print (" CATEGORIA......: ", categoria)
print (" IMAGEN.........: ", url_imagen)
print (" PRECIO ANTES...: ", precio_antes )
print (" PRECIO AHORA...: ", precio_ahora )
#cerramos Chrome
driver.quit()