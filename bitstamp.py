import websocket
import ssl

import datetime

import json

def ao_abrir(ws):
   print('Conexão aberta')
   json_subscribe = """
{
       "event": "bts:subscribe",
       "data": {
           "channel": "live_trades_btcusd"
     }
}
"""
   ws.send(json_subscribe)

def ao_fechar(ws, close_status_code, close_msg):
    print(f'{close_status_code} fechado {close_msg}')

def comprar():
     pass


def vender():
      pass


def ao_receber_mensagem(ws, mensagem):
    try:
        mensagem = json.loads(mensagem)
        if mensagem.get("event") == "trade":
            price = float(mensagem['data']['price']) / 100
            timestamp = int(mensagem['data']['timestamp'])
            datetime_object = datetime.datetime.fromtimestamp(timestamp)
            print(f"Preço do BTC/USD: ${price:.2f}, {datetime_object}")

            if price > 100500:
               vender()

            elif price < 91000:
               comprar()

            else:
               print('aguardar...')

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


def erro(ws, erro):
   print('Deu erro:')
   print(erro)


if __name__ == '__main__':
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_abrir ,
                                on_close=ao_fechar ,
                                on_error=erro ,
                                on_message=ao_receber_mensagem)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})