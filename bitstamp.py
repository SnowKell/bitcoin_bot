import websocket
import ssl

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

def ao_receber_mensagem(ws, mensagem):
    try:
        mensagem = json.loads(mensagem)
        if mensagem.get("event") == "trade":
           price = mensagem['data']['price']
           print(f"Preço do BTC/USD: {price}")
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