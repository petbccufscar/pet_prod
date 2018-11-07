from channels.routing import route

import jogo.consumers as j_cns
from jogo.consumers import ws_add_on_rodada, ws_message, ws_rodada_disconnect, ws_add_on_timer

channel_routing = [
    route("websocket.connect", ws_add_on_rodada, path=r"^/rodada/$"),
    route("websocket.connect", ws_add_on_timer, path=r"^/timer/$"),
    route("websocket.connect", j_cns.ws_add_on_mercado, path=r"^/mercado/$"),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_rodada_disconnect),
]
