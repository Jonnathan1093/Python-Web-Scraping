import requests
from bs4 import BeautifulSoup
import re
# COLORES
azul = "\33 [1;36m"  # texto azul claro
gris = "\33 [0;37m "  # texto gris
blanco = "\33 [1; 37m "  # texto blanco


def datos_Game(url):
    #    " " " Devuelve información de un producto en la tienda Game"

    # inicializamos el diccionario de salida
    d = {}
    # cabeceras de la petición HTTP
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
    }
    # realizamos la petición
    print(f'{azul} Realizando la petición:  {blanco}{url}{gris}')
    req = requests.get(url, headers=headers, timeout=10)
    print(f'{azul} Código de respuesta... :  {blanco}{req.status_code}{req.reason}{gris}')
    # si la petición no fue correcta , devolvemos error
    if req.status_code != 200:
        return {"ERROR": f"{req.reason}", "status_code ": f"{req.status_code}"}
    # url del producto
    d["url"] = req.url
    # id del producto
    d["id"] = d["url"].split("/")[-1]
    # creamos el objeto bs4 a partir del código HTML
    soup = BeautifulSoup(req.text, "html.parser")
    # with open ("requests.html", encoding="utf-8")as f:
    # f.write (req.text)
    # nombre del producto
    d["nombre_producto"] = soup.find("h2", class_="product-title").text.strip()
    # url imagen
    d["url_imagen"] = soup.find("img", id="product-cover").attrs.get("src")
    # plataformas
    objs_plat = soup.find("dd").find_all("a")
    d["plataformas"] = []
    for item in objs_plat:
        d["plataformas"].append(item.text.strip())
        # valoración
    try:
        # string del atributo que contiene el número de puntuación ( entre 0 y 5 )
        c_point = soup.find("a", class_="reviews-points-m").attrs.get("class")[-1]
        # extraemos el número que representa la puntuación del string del atributo
        puntos = re.search(r'points-(\d)', c_point).group(1)
        # convertimos el string en un entero
        d["valoracion"] = int(puntos)
    except:
        d["valoracion"] = None
        # precios
    obj_precio = soup.find("div", class_="buy--price")# objeto que contiene el precio anterior y el actual
        # precio anterior :
    try:
        d["precio_antes"] = float(obj_precio.find("small").text.replace("€", " ").replace(",", "."))
    except:
        d["precio_antes"] = None
        # precio actual:
    try:
        # obtenemos el string con el valor entero del precio actual
        p_int = obj_precio.find("span").text.strip().split("\n")[0].strip()
        # obtenemos el string con el valor decimal del precio actual
        p_dec = obj_precio.find("span", class_="decimal").text.replace("'", ".")
        # concatenamos el string con el valor entero y el decimal y lo convertimos a float
        d["precio_ahora"] = float(p_int + p_dec)
    except:
        d["precio_ahora"] = None
        # devolvemos el diccionario con los datos obtenidos
        # breakpoint()
    return d

#MAIN ##
if __name__ == "__main__":
    url = "https://www.game.es/ACCESORIOS/AURICULARES/PC-GAMING/GAME-HX500-RGB-71-PRO-GAMING-HEADSET-PC-PS4-AURICULARES-AURICULARES-GAMING/169628"
    url = "https://www.game.es/169628"
    #    url = "https://www.game.es/193393"
    datos = datos_Game(url)
    for clave, valor in datos.items():
        print(f'{azul}{clave.upper()}: {blanco}{valor}{gris}')
    exit(0)
