from genericpath import isfile
from json import load
import os
import sys
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
import pickle # para cargar / guardar las cookies

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
       
    
    s = Service(ruta) # Instanciamos el servicio de chromedriver
    driver = webdriver.Chrome(service=s, options=options) # instanciamos webdriver de selenium con chrome #añadimos el argumento Options
    driver.set_window_position(0,0) #posicionamos la ventana en la coordenada 0,0
    return driver # devolvemos el driver
    
def login_instagram ( ) :
    # Realiza login en Instagram , si es posible por cookies y sino desde cero " " "
    
    # comprobamos si existe el archico de cookies
    print("Login en Instagran por COOKIES")
    if os.path.isfile("instagram.cookies"):
    # Leemos las cookies del archivo
        cookies = pickle.load(open("instagram.cookies", "rb"))
        # Cargamos robots.txt del dominio instagram
        driver.get("https://www.instagram.com/robots.txt")
        # recorremos el objeto cookies y las añadimos al driver
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
        
    # abrimos la página de Instagram
    print('Login en INSTAGRAM desde CERO')
    driver.get(" https://www.instagram.com/")
    
    """ elemento = driver.find_element(By.XPATH,  "/html/body/script[1]/text()") # Lo utilizamos en caso de que salga la ventana de cookies
    elemento.click() # Permite hacer click en el elemento en caso tengamos una ventana de cookies
    # Puede ocurrir una exepcion, debido a que vamos muy rapido, justo al momento de entrar en la ventana esta automanticamente 
    # realiza la opcion de click que se hizo antes, para solucionar ello podemos hacer una pequeña pausa, debemps importar la libreria time
    time.sleep(5)
     """
    """ TODO ESTO PUEDE SER REEMPLAZADO EN LAS LIENAS DE ABAJO
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
    elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Guardar información']"))) # Ventana | Guardar información
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

if __name__ == "__main__" :
    # iniciamos selenium
    driver = iniciar_chrome()
    # Configuramos el tiempo de espera para cargar elementos
    wait = WebDriverWait(driver, 10) # Tiempo de espera hasta que un elemento este disponible
    #nos logueamos en Instagram
    res = login_instagram()
    if res == "Error":
        input("Pulsa enter para salir") # Pausa para poder ver el error
        driver.quit() # cerramos chrome
        sys.exit(1) # salimos del programa
    input("Pulsa enter para salir")
    driver.quit()
    
    
    
    
    
    