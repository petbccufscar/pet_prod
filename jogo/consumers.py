from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group


# Connected to websocket.connect

def ws_add_on_mercado(message):
    message.reply_channel.send({"accept": True})
    Group("mercado").add(message.reply_channel)

def ws_add_on_rodada(message):
    message.reply_channel.send({"accept": True})
    Group("rodada").add(message.reply_channel)

def ws_add_on_timer(message):
    message.reply_channel.send({"accept": True})
    Group("timer").add(message.reply_channel)
# Connected to websocket.receive
def ws_message(message):
    pass

# Connected to websocket.disconnect
def ws_rodada_disconnect(message):
    Group("rodada").discard(message.reply_channel)
