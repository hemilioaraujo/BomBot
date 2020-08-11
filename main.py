import telebot
from decouple import config
import re
import random
import time
from pyrastreio import correios

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["oi", "Oi", "oI", "OI"])
def oi(message):
    bot.reply_to(message, f"Oi {message.from_user.username}")


@bot.message_handler(content_types="location")
def local(message):
    texto = (
        f"""
<b>Longitude: </b> {message.location.longitude}
<b>Latitude: </b> {message.location.latitude}
"""
    )
    bot.send_message(message.chat.id, texto, parse_mode='HTML')


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
        texto = (
            """
<b>Instruções comando /dado</b>
<b>Sintaxe:</b> /dado <b>X</b> <b>Y</b>
<b>Onde:</b>
    <b>X: </b> Número de faces.
    <b>Y: </b> Número de lances.
<b>Exemplo:</b>
    /dado 6 10
"""
        )
        bot.send_message(message.chat.id, texto, parse_mode='HTML')
    finally:
        return


@bot.message_handler(regexp="^/rastrear")
def rastrear(message):
    codigo = str(message.text).upper().split(' ')[-1]

    if verificar_codigo(codigo):
        dados = correios(codigo)
        texto = ''
        if len(dados):
            for i in dados:
                texto += f"{i['data']} - {i['hora']}\n"
                texto += f"{i['local']}\n"
                texto += f"<b>{i['mensagem']}</b>\n"
                texto += "============================\n\n"
            # bot.reply_to(message, texto)
            bot.send_message(message.chat.id, texto, parse_mode='HTML')
        else:
            bot.reply_to(message, "Objeto não encontrado!")
    else:
        texto = """
<b>Instruções comando /rastrear</b>
<b>Sintaxe:</b> 
    /rastrear <b>código</b>
<b>Exemplo:</b>
    /rastrear AA111111111BB
        """
        bot.send_message(message.chat.id, texto, parse_mode='HTML')


def verificar_codigo(codigo):
    """[Método que verifica o formato do código]
    Arguments:
        codigo {[str]} -- [código de rastreamento]
    Returns:
        object {[boolean]}: [True se atende o requisito]
    """
    codigo = codigo.upper()
    # if re.search("[A-Z]{2}+[0-9]{9}+[A-Z]{2}", codigo):
    # TEM QUE MELHORAR ESTA EXPRESSÃO HEIN
    if re.search("[A-Z]+[A-Z]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[A-Z]+[A-Z]", codigo):
        return True
    return False


while True:
    try:
        bot.polling(interval=2)
    except Exception:
        time.sleep(2)
