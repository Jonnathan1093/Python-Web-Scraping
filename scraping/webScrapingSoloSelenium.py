# para instalar automáticamente chromedriver
from webdriver_manager.chrome import ChromeDriverManager
# driver de selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# para modificar las opciones de webdriver en chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # Importamos esta para usar selenium, sirve para definir el tipo de busqueda del elemento

# Inicia Chrome con los parametris indicados y devuelve el driver
def iniciar_chrome():
    # Instalamos la version de chromedriver correspondiente, nos deveulve la ruta completa del ejecutable
    # El log level nos permite definir la cantidad de informacion que queremos que se muestre en el terminal
    # log_level=0  no mostraria nada o salida limpia 
    # ruta = ChromeDriverManager(path="./chromedriver", log_level=0).install()
    ruta = ChromeDriverManager(path="./chromedriver").install()
    # Opciones de chrome
    # Instanciamos las clase options    
    options = Options() # Creamos un objeto llamado options
    
    # Para definir el User agent en selenium lo hacemos de la siguiente manera
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
    
    options.add_argument(f" user-agent={user_agent}") # Define un user agent
    options.add_argument("--headless") # para ejecutar chromedriver, pero sin abrir la ventana
    # Estos son excluyentes es decir si funciona el uno no funciona el otro 
    # options.add_argument("--window-size=1000,1000") # Configurar dimension ventana alto y ancho
    options.add_argument("--start-maximized") # para maximizar la ventana 
    options.add_argument("--disable-web-security") # desabilita la politica del mismo origen o Same Origin Policy
    options.add_argument("--disable-extensions") # No cargue las extensiones de chrome
    options.add_argument("--disable-notifications") # Bloquear las notificaciones
    options.add_argument("--ignore-certificate-errors") # Ignora el aviso "Su conexion no es privada"
    options.add_argument("--no-sandbox") # deshabilita el modo sandbox
    options.add_argument("--log-level=3") # para que chromedriver no muestre nada en la terminal
    options.add_argument("--allow-running-insecure-content") # desactiva el aviso de " contenido no seguro"
    options.add_argument("--no-default-browser-check") # Evita el aviso de que Chrome no es el navegador por defecto
    options.add_argument("--no-first-run") # evita la ejecución de ciertas tareas que se realizan la primera vez que se ejecutan en chrome
    options.add_argument("--no-proxy-server") # para no usar proxy , sino conexiones directas
    # ESTE ARGUMENTO ES EL MAS IMPORTANTE PARA QUE NO NOS DETECTE COMO BOT
    options.add_argument("--disable-blink-features=AutomationControlled") # evita que selenium
    
    # PARÁMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt = [ # Definimos una lista
        'enable-automation', # para que no muestre la notificación " Un software automatizado de pruebas esta controlando Chro,e
        'ignore-certificate-errors', # para ignorar errores de certificados ( a veces están caducados)
        'enable-logging' # para que no se muestre en la terminal " DevTools listening on ... "
        ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    
    # PARÁMETROS QUE DEFINEN PREFERENCIAS EN CHROMEDRIVER
    prefs = { # Definimos un diccionario
        "profile.default_content_setting_values.notifications" : 2 ,# notificaciones : 0 = preguntar | 1 = permitir | 2=  no permitir
        " intl.accept_languages " : [ " es - ES " , " es " ] , # para definir el idioma del navegador
        " credentials_enable_service " : False # para evitar que Chrome nos pregunte si queremos guardar la contraseña al loguearnos
     }
    options.add_experimental_option("prefs", prefs)
       
    # Instanciamos el servicio de chromedriver
    s = Service(ruta)
    # instanciamos webdriver de selenium con chrome
    driver = webdriver.Chrome(service=s, options=options) #añadimos el argumento Options
    # devolvemos el driver
    return driver
# MAIN
if __name__ == "__main__":
    driver = iniciar_chrome()
    # input("Preciona enter para salir") # Eliminamos esta linea y definimos la url de la peticion
    url ="https://www.pccomponentes.com/alurin-go-intel-pentium-n4200-8gb-128gb-ssd-nos-141"
    driver.get(url)
    nombre_producto = driver.find_element(By.CSS_SELECTOR, "div.articulo").text # Pasamos 2 argumentos para difinir que tipo vamos hacer, segundo el selector css
    precio_antes = driver.find_element(By.CSS_SELECTOR, "del.original-price-nodiscount").text
    # precio_actual = driver.find_element(By.CSS_SELECTOR, "div#precio-main").text # Tendra el mismo resultado que con ID
    precio_actual = driver.find_element(By.ID, "precio-main").text
    
    # NOTA: "find_element" seria el equivalente a "find" en beatifulsoup
    # NOTA: "find_all" seria el equivalente a "find_elements"
    
    # MEDIANTE ESTAS VARIANTES Y CICLO PODREMOS OBTENER LOS DATOS EN CASO EXISTA UNA CATEGORIA
    variantes = driver.find_elements(By.CSS_SELECTOR, "div.variant") # En esta variable se guardara una lista con los elementos
    vars = {} # Con esto definimos el diccionario para find_elements´
    
    for variante in variantes:
        tipo = variante.find_element(By.CSS_SELECTOR, "div.variant__title").text.split(":")[0]    
        vars[tipo] = []# Inicializo la lista que contendra una lista vacia  
        opciones = variante.find_elements(By.CSS_SELECTOR, "a")
        for opcion in opciones: # Recorremos la lista
            vars[tipo].append(opcion.text)
    # FIN
    
    url_imagen = driver.find_element(By.CSS_SELECTOR, "img.img-fluid").get_attribute("src")
    
    print(f"Nombre del producto: {nombre_producto}")
    print(f"Nombre del producto: {precio_antes}")
    print(f"Nombre del producto: {precio_actual}")
    print(f"Variantes..........: {vars}")
    print(f"Url de la imagen...: {url_imagen}")
    driver.quit()
 
    
    