import config
import json, websocket
from bot import Bot


trading_bot = Bot()

# need to set the amounts to trade with

print("Initialized Bot")

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "auth",
        "key": config.API_KEY,
        "secret": config.API_SECRET_KEY
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "subscribe", "bars":Bot.bar_threads}

    ws.send(json.dumps(listen_message))


socket = "wss://stream.data.alpaca.markets/v2/iex"

#This is where I send messages to react to the data
def on_message(ws, message):
    json_data = json.loads(message)
    if json_data[0]['T'] == 'b':
        trading_bot.transmit_data(json_data[0]['t'], json_data[0]['S'], json_data[0]['c'], json_data[0]['v'])
    else:
        print(message)

def on_close(ws):
    #print(data_processor.trade_data)
    print("closed connection")

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()