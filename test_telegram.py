from config import * #Importamos el token
import telebot #para manejar la API de telegram

# Instanciamos el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Para controlar que va hacer el bot
# Responde al comando /start

# Los decoradores inician con @ son funciones que resiven
# como parametros de entrada una funcion y devuelven otra funsion

@bot.message_handler(commands=["start", "ayuda", "help"])
# Acontinuacion debemos definir una funcion

def cmd_start(message):
    # Da la bienvenida al usuario del bot
    bot.reply_to(message, "Hola, aqui encontraras todo lo que te gusta")

@bot.message_handler(content_types=["text"])
# Responde a los mensajes de texto que no son comandos o se puede usar los de abajo dependiendo
# text, audio, document, photo, sticker, video, video_note, 
# voice, location, contact, new_chat_members, left_chat_member, 
# new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, 
# supergroup_chat_created, channel_chat_created, migrate_to_chat_id, 
# migrate_from_chat_id, pinned_message
def bot_mensajes_texto(message):
# FORMATOS HTML 
    texto_html = '<b><u>Formatos Html</u>:</b>' + '\n' #Manera de anidar etiquetas
    texto_html+= '<b>NEGRITA</b>' + '\n' #Negrita en html
    texto_html+= '<i>CURSIVA</i>' + '\n' #Cursiva en html
    texto_html+= '<u>SUBRAYADO</u>'+ '\n' #Subrayado en html
    texto_html+= '<s>TACHADO</s>' + '\n' #Tachado en html
    texto_html+= '<code>MONOESPACIADO</code>' + '\n' #Monoespaciado en html
    texto_html+= '<span class="tg-spoiler">SPOILER</span>' + '\n' #Spoiler en html 
    texto_html+= '<a href="https://retrogeeksla.blogspot.com/">ENLACE</a>' + "\n" #Enlace en html
#FORMATOS MARKDOWNV2 
    texto_markdown ='*__Formatos Markdown__:*' + '\n'
    texto_markdown+= '*NEGRITA*' + '\n' #Negrita 
    texto_markdown+= '_CURSIVA_' + '\n' #Cursiva 
    texto_markdown+= '__SUBRAYADO__'+ '\n' #Subrayado 
    texto_markdown+= '~TACHADO~' + '\n' #Tachado 
    texto_markdown+= '```MONOESPACIADO```' + '\n' #Monoespaciado 
    texto_markdown+= '||SPOILER||' + '\n' #Spoiler 
    texto_markdown+= '[ENLACE](https://retrogeeksla.blogspot.com/)' + '\n' #Enlace
#Gestionar los mensajes de texto recibidos    
    if message.text.startswith("/"): #Controlo el texto para que no inicien con barra
        bot.send_message(message.chat.id, "Comando no disponible") #Controlo el texto si por ejemplo ponen: /hola 
    else:
        bot.send_message(message.chat.id, texto_html, parse_mode="html", disable_web_page_preview=True) 
        bot.send_message(message.chat.id, texto_markdown, parse_mode="MarkdownV2", disable_web_page_preview=True)  # Podemos ver en formato Markdown    
                                                                                                                    #De esta manera obtenemos el chat id del usuario que nos envio el mensaje
                                                                                                                    # parse_mode me permite enviar en formato html #  Para controlar la previsualizacion de nuestro enlace usamos disable_web_page_preview
# Comenzamos a escribir nuestro programa principal
if __name__== '__main__': # Para indicar que se inicia el bot
    print('Iniciando el bot') 
    bot.infinity_polling() # Este metodo se trata de un bucle infinito, comprueba constante mente si se resiven mensajes nuevos
    print('Fin')









