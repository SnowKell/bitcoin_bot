import json
import ssl

import datetime
import websocket
import bitstamp.client

import credenciais

def cliente():
    return bitstamp.client.Trading( username=credenciais.USERNAME,
                                    key=credenciais.KEY,
                                    secret=credenciais.SECRET)


def comprar(quantidade):
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)


def vender(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


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

def ao_fechar(_ws, close_status_code, close_msg):
    print(f'{close_status_code} fechado {close_msg}')

def ao_receber_mensagem(_ws, mensagem):
    try:
        mensagem = json.loads(mensagem)
        if mensagem.get("event") == "trade":
            price = float(mensagem['data']['price']) / 100
            timestamp = int(mensagem['data']['timestamp'])
            datetime_object = datetime.datetime.fromtimestamp(timestamp)
            print(f"Preço do BTC/USD: ${price:.2f}, {datetime_object}")

            if price > 1056.67:
               vender(0.001)

            elif price < 938.46:
               comprar(0.001)

            else:
               print('aguardar...')

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


def erro(_ws, error):
   print('Deu erro:')
   print(error)


if __name__ == '__main__':
    ws_app = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_abrir ,
                                on_close=ao_fechar ,
                                on_error=erro ,
                                on_message=ao_receber_mensagem)

    ws_app.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})