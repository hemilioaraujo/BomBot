import telebot
from decouple import config
import re
import random


key = config('TOKEN')

bot = telebot.TeleBot(key)


@bot.message_handler(commands=["oi", "Oi", "oI", "OI"])
def oi(message):
    bot.reply_to(message, f"Oi {message.from_user.username}")


@bot.message_handler(content_types="location")
def local(message):
    bot.reply_to(message, message.location)


@bot.message_handler(regexp="^/dado")
def dado(message):
    """[Retorna o valor de um dado de N faces N vezes]

    Arguments:
        message {[dict]} -- [conteúdo da mensagem recebida]
    """

    # numeros[0] faces, numeros[1] repetições
    numeros = re.findall("[0-9]+", message.text)

    resultado = ''

    try:
        faces = int(numeros[0])
        repeticoes = int(numeros[1])

        if len(numeros) == 2:
            if repeticoes > 100:
                bot.reply_to(message, "Número de repetições máximo de 100 vezes!")
                return

            for i in range(1, repeticoes + 1):
                numero_sorteado = random.randint(1, faces)
                resultado += str(numero_sorteado)
                if i != repeticoes:
                    resultado += ' - '

            bot.reply_to(message, resultado)
    except IndexError:
        bot.reply_to(message, 'Por favor informe /dado {nº faces} {repetições}\n'
                              'Ex.: /dado 6 3')
    finally:
        return


bot.polling(interval=10)
