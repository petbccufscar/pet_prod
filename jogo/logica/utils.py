# -*- coding: UTF-8 -*-
import random
import string


def gerar_token(N):
    token = []
    tam = 5  # tamanho do token
    for i in range(0, N):
        token.append("asdf")

    return token

def json_para_mercado(tipo, id, qtd):
    return "{\"tipo\": \""+tipo+"\",\"id\":"+ str(id) +",\"qtd\":"+ str(qtd)+"}"
