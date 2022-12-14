from cgi import print_arguments
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from config_instagram import * # Importamos la configuracion de instagram
# Estas 3 librerias nos permite solucionar el tiempo de un elemento, consiste en definir un tiempo de expera maximo, y si esta disponoble antes lo genera 
from selenium.webdriver.support.ui import WebDriverWait # para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as EC # para condiciones en selenium
from selenium.common.exceptions import TimeoutException # exepcion de timeout en selenium
from selenium.webdriver.common.keys import Keys # para pulsar teclas especiales
import os
import sys
import time
import pickle # para cargar / guardar las cookies
import wget # para descargar archivos

# Inicia Chrome con los parametris indicados y devuelve el driver
def iniciar_chrome():
    # Instalamos la version de chromedriver correspondiente, nos deveulve la ruta completa del ejecutable
    # El log level nos permite definir la cantidad de informacion que queremos que se muestre en el terminal
    # ruta = ChromeDriverManager(path="./chromedriver", log_level=0).install()
    ruta = ChromeDriverManager(path="./chromedriver").install()
    # Opciones de chrome
    
    options = Options()  # Instanciamos las clase options  # Creamos un objeto llamado options
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"     # Para definir el User agent en selenium lo hacemos de la siguiente manera

    options.add_argument(f" user-agent={user_agent}") # Define un user agent
   # options.add_argument("--headless") # para ejecutar chromedriver, pero sin abrir la ventana
    # Estos son excluyentes es decir si funciona el uno no funciona el otro 
    options.add_argument("--window-size=970,1080") # Configurar dimension ventana alto y ancho
    # options.add_argument("--start-maximized") # para maximizar la ventana 
    options.add_argument("--disable-web-security") # desabilita la politica del mismo origen o Same Origin Policy
    options.add_argument("--disable-extensions") # No cargue las extensiones de chrome
    options.add_argument("--disable-notifications") # Bloquear las notificaciones
    options.add_argument("--ignore-certificate-errors") # Ignora el aviso "Su conexion no es privada"
    options.add_argument("--no-sandbox") # deshabilita el modo sandbox
    options.add_argument("--log-level=3") # para que chromedriver no muestre nada en la terminal
    options.add_argument("--allow-running-insecure-content") # desactiva el aviso de " contenido no seguro"
    options.add_argument("--no-default-browser-check") # Evita el aviso de que Chrome no es el navegador por defecto
    options.add_argument("--no-first-run") # evita la ejecuci??n de ciertas tareas que se realizan la primera vez que se ejecutan en chrome
    options.add_argument("--no-proxy-server") # para no usar proxy , sino conexiones directas
    # ESTE ARGUMENTO ES EL MAS IMPORTANTE PARA QUE NO NOS DETECTE COMO BOT
    options.add_argument("--disable-blink-features=AutomationControlled") # evita que selenium
    
    # PAR??METROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt = [ # Definimos una lista
        'enable-automation', # para que no muestre la notificaci??n " Un software automatizado de pruebas esta controlando Chro,e
        'ignore-certificate-errors', # para ignorar errores de certificados ( a veces est??n caducados)
        'enable-logging' # para que no se muestre en la terminal " DevTools listening on ... "
        ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    
    # PAR??METROS QUE DEFINEN PREFERENCIAS EN CHROMEDRIVER
    prefs = { # Definimos un diccionario
        "profile.default_content_setting_values.notifications" : 2 ,# notificaciones : 0 = preguntar | 1 = permitir | 2=  no permitir
        " intl.accept_languages " : [ " es - ES " , " es " ] , # para definir el idioma del navegador
        " credentials_enable_service " : False # para evitar que Chrome nos pregunte si queremos guardar la contrase??a al loguearnos
     }
    options.add_experimental_option("prefs", prefs)
       
    
    s = Service(ruta) # Instanciamos el servicio de chromedriver
    driver = webdriver.Chrome(service=s, options=options) # instanciamos webdriver de selenium con chrome #a??adimos el argumento Options
    driver.set_window_position(0,0) #posicionamos la ventana en la coordenada 0,0
    return driver # devolvemos el driver
    
def cursor_arriba(n=1):
    # Sube el cursor n vecees 
    print(f" \033[{n}A", end="")
    
def raya():
    # escribe tantos guiones como ancha sea la terminal
    print("-"*os.get_terminal_size().columns) 
    
def login_instagram ( ) :
    # Realiza login en Instagram , si es posible por cookies y sino desde cero " " "
    
    # comprobamos si existe el archico de cookies
    print("Login en Instagran por COOKIES")
    if os.path.isfile("instagram.cookies"):
    # Leemos las cookies del archivo
        cookies = pickle.load(open("instagram.cookies", "rb"))
        # Cargamos robots.txt del dominio instagram
        driver.get("https://www.instagram.com/robots.txt")
        # recorremos el objeto cookies y las a??adimos al driver
        for cookie in cookies:
            driver.add_cookie(cookie) 
        # Comprobamos si el login por cookies funciona
        driver.get("https://www.instagram.com/")
        try:
            elemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article[role='presentation']"))) 
            print("Login desde COOKIES: Correcto")
            return "Ok"
        except TimeoutException:
            print("Error: El feed de noticias no se ha cargado")
            return "Error"
    else: # Si no existe el archivo de las cookies
        print("Alerta: El archivo de cookies no existe")
    
    # input("Pausa...") # Ponemos este input para hacer una pausa y comprobar si funciona o no las cookies   
        
    # abrimos la p??gina de Instagram
    print('Login en INSTAGRAM desde CERO')
    driver.get(" https://www.instagram.com/")
    
    # elemento = driver.find_element(By.XPATH,  "/html/body/script[1]/text()") # Lo utilizamos en caso de que salga la ventana de cookies
    # elemento.click() # Permite hacer click en el elemento en caso tengamos una ventana de cookies
    # Puede ocurrir una exepcion, debido a que vamos muy rapido, justo al momento de entrar en la ventana esta automanticamente 
    # realiza la opcion de click que se hizo antes, para solucionar ello podemos hacer una peque??a pausa, debemps importar la libreria time
    # time.sleep(5)
    
    """ ESTO PUEDE SER REEMPLAZADO EN LAS LIENAS DE ABAJO
    # elemento = driver.find_element(By.NAME, "username") # NAME es otro metodo para localizar elementos
    # elemento = driver.find_element(By.NAME, "password") # NAME es otro metodo para localizar elementos """
    
    # Lo ideal es encerrar toto esto en un try, para ello tendriamos que hacer en cada elemento en caso de error
    try: 
        elemento = wait.until(EC.visibility_of_element_located((By.NAME, "username"))) # sustituimos el time.sleep(3)
    except TimeoutException:
        print("Error: Elemento username no diponible")
        return "Error"
    elemento.send_keys(USER_IG)
    elemento = wait.until(EC.visibility_of_element_located((By.NAME, "password"))) # sustituimos el | time.sleep(3)
    elemento.send_keys(PASS_IG)
    # elemento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))) # Este es otro metodo para un selector
    elemento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button"))) 
    elemento.click()
    # Cualquiera de los 2 metodos funciona
    # elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div/div/button"))) # Ventana | Ahora no
    elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Guardar informaci??n']"))) # Ventana | Guardar informaci??n
    elemento.click()
    try:
        elemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article[role='presentation']"))) 
        print("Login desde cero: Correcto")
    except TimeoutException:
        print("Error: El feed de noticias no se ha cargado")
        return "Error"
    # guardar cookies con pickle
    cookies = driver.get_cookies()
    pickle.dump(cookies, open("instagram.cookies", "wb"))
    print("Cookies guardadas")
    return "Ok"

def descargar_fotos_instagram(hashtag, minimo):
    # Descarga las fotos del hashtag indicado

    # Realizamos la peticion
    print(f"Buscando por hashtag #{hashtag}")
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}")
    #  realizamos scroll de la pagina
    url_fotos = set() # conjunto vacio en el que iremos a??adiendo los link de las fotos
    while len(url_fotos) < minimo:
        # Ejecutamos script de javascript que realiza scroll hasta el final de la pagina
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # window.scrollTo(0, document.body.scrollHeight); | este es un codigo de javascrip que ayuda a realizar scroll o avanzar pagina
        elemetos = driver.find_elements(By.CSS_SELECTOR, "div._aagu")
        for elemento in elemetos:
            try:
                url = elemento.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                url_fotos.add(url)
            except:
                pass
        print(f"Total fotos: {len(url_fotos)}")
        cursor_arriba()
        
    # Creamos una carpeta con el nombre del hasg??htag
    if not os.path.exists(hashtag):
        os.mkdir(hashtag)
    # Descargamos las fotos del conjunto
    n = 0 # Numero de foto en curso
    for url_foto in url_fotos:
        n+= 1
        print(f"Descargando {n} de {len(url)}")
        nombre_archivo = wget.download(url_foto, hashtag) # Como primer argumento url_fotos que es el enlace que vamos a descargar, y 2ndo argumento indicamos la carpeta donde queremos descargar 
        cursor_arriba()
        print(f"\33[K descargando {nombre_archivo}")
        print()
    return len(url_fotos)
        
if __name__ == "__main__" :
    # Ponemos variables de tipo string
    modo_de_uso = f'Modo de uso:\n'
    modo_de_uso = input(f'{os.path.basename(sys.executable)} {sys.argv[0]} hashtag[minimo]\n\n')
    modo_de_uso = f'opciones: \n'
    modo_de_uso = f'minimo: minimo de descargas a realizar (por defecto 300)\n\n'
    modo_de_uso = f'Ejemplos:\n'
    modo_de_uso = f'{os.path.basename(sys.executable)} {sys.argv[0]} cats\n'
    modo_de_uso = f'{os.path.basename(sys.executable)} {sys.argv[0]} superman 300\n'
    
     # Control de parametos
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print(modo_de_uso)
        sys.exit(1)
    elif len(sys.argv) == 3: # Puede darse que el argumento sea 3
        if sys.argv[2].isdigit(): # Es decir si se cumple esto se definira una constante "MINIMO"
            MINIMO = int(sys.argv[2]) # Se convierte el string en un entero
        else:
            print(f" Error: {sys.argv[2]} no es un numero")
            sys.exit(1)
    else:    # Nos queda un posible caso, es decir que el usuario solo haya puesto el hashtag
        MINIMO = 100    
    HASHTAG = sys.argv[1].strip('#') # como el hashtag es obligatorio este parametro siempre existiara
    
    # iniciamos selenium
    driver = iniciar_chrome()
    # Configuramos el tiempo de espera para cargar elementos
    wait = WebDriverWait(driver, 10) # Tiempo de espera hasta que un elemento este disponible
    #nos logueamos en Instagram
    res = login_instagram()
    if res == "Error": # si se produce un error en el login
        input("Pulsa enter para salir") # Pausa para poder ver el error
        driver.quit() # cerramos chrome
        sys.exit(1) # salimos del programa
    raya() # Linea separadora
    # Descargamos las fotos del hashtag indicado
    res = descargar_fotos_instagram(HASHTAG, MINIMO)
    print(f"Se han descargado {res} fotos")
    # input("Pulsa enter para salir")
    driver.quit()
    
    
    
    
    
    