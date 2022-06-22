import telebot
import yfinance as yf

bot = telebot.TeleBot('5230941298:AAEl8XGs7NgMu9PxHCnsii8usDr_fwUd8z0')

@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey!")

@bot.message_handler(commands=['Hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")

def stock_request(message):
  request = message.text.split()
  return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()
  ticker = message.text.split(' ')[0].upper()
  data = yf.download(tickers=request, period='390m', interval='30m')
  CompanyName = yf.Ticker(ticker).info['shortName']
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, f'Stock Price of {CompanyName}')
    bot.send_message(message.chat.id, round(data['Close'], 2).to_string(header=False))
  else:
    bot.send_message(message.chat.id, "Invalid Ticker")

bot.polling(none_stop=True)