# -*- coding: UTF-8 -*-
from secrets import token_urlsafe

def gerar_token():
    return token_urlsafe(16)

def json_para_mercado(tipo, id, qtd):
    return "{\"tipo\": \""+tipo+"\",\"id\":"+ str(id) +",\"qtd\":"+ str(qtd)+"}"
