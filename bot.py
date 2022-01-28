# numero aleatorio para testear el bot
import random
# para la variable de entorno
import os, sys
# from dotenv import load_dotenv
import telegram
'''
Updater -> recibe los mensajes de telegram
CommandHandler -> Para ejecutar los callbacks de eventos
MessageHandler -> Para recibir informacion de texto, asignar filtros (Filters), etc
'''
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# logger -> informa sobre los sucesos
import logging

#funciones
def start(update, context):
    logger.info(f'El usuario {update.effective_user["first_name"]} ha iniciado una conversacion')

    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot.")


def random_number(update, context):
    user_id = update.effective_user['id']
    logger.info(f'El usuario {user_id} ha solicitado un numero aleatorio')
    number = random.randint(0, 10)
    context.bot.sendMessage(chat_id=user_id, parse_mode="HTML",text=f"<b>Numero aleatorio:</b>\n{number}")


def echo(update, context):
    user_id = update.effective_user['id']
    logger.info(f'El usuario {user_id} ha enviado un mensaje de texto')
    text = update.message.text
    context.bot.sendMessage(
        chat_id=user_id,
        parse_mode='MarkdownV2',
        text=f"*Escribiste:*\n_{text}_"
    )


#configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s %(levelname)s - %(message)s",
)
logger = logging.getLogger()

#solicitar TOKEN y MODE
TOKEN = os.getenv('TOKEN')
MODE = os.getenv('MODE')

if MODE == "dev":
    # Acceso local (dev)
    def run(updater):
        #iniciar a recibir mensajes
        updater.start_polling()
        print('BOT READY')
        updater.idle() #Permite finalizar el Bot con Ctrl + C
elif MODE== 'prod':
    # Acceso Heroku (production)
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443")) #puerto soportado para webhooks
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen='0.0.0.0', 
                                port=PORT,
                                url_path=TOKEN,
                                webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
        updater.idle()
else:
    logger.info('No se especifico el modo.')
    sys.exit()


if __name__ == "__main__":
    my_bot = telegram.Bot(token=TOKEN)

    #enlazar updater con el token
    updater = Updater(my_bot.token, use_context=True)

    #creamos un despachador
    dp = updater.dispatcher

    #creamos los manejadores
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("random", random_number))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # ejecutamos la aplicacion
    run(updater)
