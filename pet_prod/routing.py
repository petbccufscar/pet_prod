from channels.routing import route
from jogo.consumers  import ws_add, ws_message, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add, path=r"^/time/$"),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
