import telebot
import requests
import time
import threading
import schedule

bottoken = '6295107125:AAHQkKI2NdRLjQl1so7Drcz7np3o-hUTkcQ'
bot = telebot.TeleBot(bottoken)
chat_id = '-1001767046320'

@bot.message_handler(commands=['start'])
def start(message):
    """Handler para o comando /start"""
    text = "Olá! Eu sou o Rumo_à_JMJ_bot, eu tenho a missão de monitorar as cotações do dólar e do euro para você. Use o comando /monitorar para iniciar o monitoramento."
    bot.send_message(chat_id, text)

def schedule_send_exchange_rates():
    while True:
        schedule.every(20).minutes.do(send_exchange_rates)

@bot.message_handler(commands=['monitorar'])
def monitor(message):
    """Handler para o comando /monitorar"""
    text = "O monitoramento das cotações foi iniciado. Você será notificado se houver variações de mais de 1 centavo."
    bot.send_message(chat_id, text)
    t1 = threading.Thread(target=schedule_send_exchange_rates)
    t2 = threading.Thread(target=monitor_exchange_rates)
    t1.start()
    t2.start()
 

""" @bot.message_handler(commands=['configurar'])
def configurar(update, context):
    #Handler para o comando /configurar
    message = "Use /limites para definir os limites de variação das cotações."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

@bot.message_handler(commands=['limites'])
def limites(update, context):
    #Handler para o comando /limites
    message = "Digite os limites de variação em centavos. Exemplo: 10 para 10 centavos."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    context.user_data['limites'] = True

@bot.message_handler(commands=['listar'])
def listar(update, context):
    #Handler para o comando /listar
    message = "Últimas cotações:\n" + context.user_data['last_prices']
    context.bot.send_message(chat_id=update.effective_chat.id, text=message) """

def send_message(message):
    bot.send_message(chat_id, message)

def monitor_exchange_rates():
    dol_url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    eur_url = 'https://economia.awesomeapi.com.br/json/last/EUR-BRL'
    preco_max_dol = 5.20
    preco_max_eur = 5.52
    ult_precos = {'USD': None, 'EUR': None}
    while True:
        try:
            dol_resp = requests.get(dol_url)
            eur_resp = requests.get(eur_url)
            if dol_resp.status_code != 200 or eur_resp.status_code != 200:
                raise ValueError('Erro ao acessar API de cotações')
            usd_preco = float(dol_resp.json()['USDBRL']['bid'])
            eur_preco = float(eur_resp.json()['EURBRL']['bid'])
            if ult_precos['USD'] is not None and abs(ult_precos['USD'] - usd_preco) != 0:
                diff = usd_preco - ult_precos['USD']
                if diff > 0:
                    message = f'Dólar subiu {diff:.3f} e está cotado a {usd_preco:.4f}'
                else:
                    message = f'Dólar caiu {abs(diff):.3f} e está cotado a {usd_preco:.4f}'
                send_message(message)
            if ult_precos['EUR'] is not None and abs(ult_precos['EUR'] - eur_preco) != 0:
                diff = eur_preco - ult_precos['EUR']
                if diff > 0:
                    message = f'Euro subiu {diff:.3f} e está cotado a {eur_preco:.4f}'
                else:
                    message = f'Euro caiu {abs(diff):.3f} e está cotado a {eur_preco:.4f}'
                send_message(message)
            ult_precos['USD'] = usd_preco
            ult_precos['EUR'] = eur_preco
        except Exception as e:
            send_message(f'Erro no monitoramento: {str(e)}')
            time.sleep(300)
            continue
        time.sleep(600)

import requests

def send_exchange_rates():
    usd_url = 'https://query1.finance.yahoo.com/v8/finance/chart/USDBRL=X?interval=1d&range=1d'
    eur_url = 'https://query1.finance.yahoo.com/v8/finance/chart/EURBRL=X?interval=1d&range=1d'
    try:
        usd_resp = requests.get(usd_url)
        eur_resp = requests.get(eur_url)
        if usd_resp.status_code != 200 or eur_resp.status_code != 200:
            raise ValueError('Erro ao acessar API de cotações')
        usd_preco = float(usd_resp.json()['chart']['result'][0]['meta']['regularMarketPrice'])
        eur_preco = float(eur_resp.json()['chart']['result'][0]['meta']['regularMarketPrice'])
        message = f'Cotações atuais:\nDólar: {usd_preco:.4f}\nEuro: {eur_preco:.4f}'
        send_message(message)
    except Exception as e:
        send_message(f'Erro no envio de cotações: {str(e)}')



if __name__ == '__main__':
    try:    
        bot.polling()
    except Exception as e:
        send_message(f'O bot foi parado devido a um erro: {str(e)}')
        send_message("O bot foi encerrado.")
