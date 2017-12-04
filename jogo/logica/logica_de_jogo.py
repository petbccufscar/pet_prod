import datetime
from datetime import timedelta
import _thread
from time import sleep
def next():

    return 5000000

def atualiza_timer():
    global timer
    anterior = datetime.datetime.utcnow()
    print (anterior)
    timer = next()
    while(True):
        atual = datetime.datetime.utcnow()

        delta_time = atual - anterior
        anterior = datetime.datetime.utcnow()
        timer = timer - delta_time.microseconds - delta_time.seconds*1000000
        print(timer)
        sleep(0.1)
        if(timer < 0):
            print("zerou")
            timer = next()
def init_timer():
    _thread.start_new_thread(atualiza_timer, ())
