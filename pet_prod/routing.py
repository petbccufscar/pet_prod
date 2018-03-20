from channels.routing import route
from jogo.consumers  import ws_add_on_rodada, ws_message, ws_rodada_disconnect

channel_routing = [
    route("websocket.connect", ws_add_on_rodada, path=r"^/rodada/$"),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_rodada_disconnect),
]
