#!/usr/bin/python3.7

import random, telepot, urllib3
from string import ascii_lowercase as ascii
from time import sleep
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.delegate import per_chat_id, create_open, pave_event_space


proxy_url = "http://proxy.server:3128"
telepot.api._pools = { 'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30), }
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


class MorseQuiz(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.a = list(ascii)
        #self.a += ['1','2','3','4','5','6','7','8','9','0']
        self.morse = {
            'a':'.-',
            'b':'-...',
            'c':'-.-.',
            'd':'-..',
            'e':'.',
            'f':'..-.',
            'g':'--.',
            'h':'....',
            'i':'..',
            'j':'.---',
            'k':'-.-',
            'l':'.-..',
            'm':'--',
            'n':'-.',
            'o':'---',
            'p':'.--.',
            'q':'--.-',
            'r':'.-.',
            's':'...',
            't':'-',
            'u':'..-',
            'v':'...-',
            'w':'.--',
            'x':'-..-',
            'y':'-.--',
            'z':'--..',
        }
        val_iniz = random.choice(self.a)
        self.ris = [val_iniz,val_iniz] #aggiungo due valori identici così che quando verrà utilizzato il primo valore per la prima domanda, al secondo ciclo la risposta risulterà comunque corretta...
        self.usrErrCor = {} #user: [errors,correct]

    def on_chat_message(self,msg):

        content_type, chat_type, chat_id = telepot.glance(msg)
        usr ='id_'+str(chat_id)
        print(usr+' is online\tsent:'+content_type+'\t on:'+chat_type)

        #il primo valore è l'ultimo inserito
        self.ris.insert(0,random.choice(self.a)) #ogni volta salvo la risposta della domanda in modo da averlo al ciclo successivo
        self.ris.pop(2) #dal secondo ciclo rimuovo la risposta alla domanda già che è già stata fatta in modo da avere sempre e solo 2 valori in lista.
        r = self.ris[1] #e uso come risposta corretta quella della domanda più vecchia
        d = self.ris[0] # come domanda il nuovo valore

        if content_type == 'text':
            text = msg['text']
            if text == self.morse[r]:
                try: #se per qualche ragione usr non avesse iniziato con /start
                    self.usrErrCor[usr][1] +=1
                except:
                    self.usrErrCor[usr] = [0,1]
            elif text == '/start': #reset totale
                self.usrErrCor[usr] = [0,0]
                val_iniz = random.choice(self.a)
                self.ris = [val_iniz,val_iniz]
                d = self.ris[0]
            elif text == '/morse':
                val_iniz = random.choice(self.a)
                self.ris = [val_iniz,val_iniz] #reset valori iniziali
                d = self.ris[0]
                codeMorse = str(self.morse).replace("'",'').replace('{','').replace('}','').replace(',','\n')
                bot.sendMessage(chat_id,codeMorse)
            else:
                try:
                    self.usrErrCor[usr][0] +=1
                except:
                    self.usrErrCor[usr] = [1,0]
        if text != '/stop':
            bot.sendMessage(chat_id,("corrette: %d \terrate: %d"%(self.usrErrCor[usr][1],self.usrErrCor[usr][0])))

            #Generazione bottoni risposte casuali (3 errate, 1 corretta)
            a_copy = list(ascii)
            a_copy.remove(d)

            d1 = random.choice(a_copy)
            a_copy.remove(d1)

            d2 = random.choice(a_copy)
            a_copy.remove(d2)

            d3 = random.choice(a_copy)

            KEYS = [d,d1,d2,d3]
            key_1 = random.choice(KEYS)

            KEYS.remove(key_1)
            key_2 = random.choice(KEYS)

            KEYS.remove(key_2)
            key_3 = random.choice(KEYS)

            KEYS.remove(key_3)
            key_4 = random.choice(KEYS)


            bot.sendMessage(chat_id,("a cosa corrisponde %s ?"%(d)),
                                reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[
                                         [KeyboardButton(text=self.morse[key_1]), KeyboardButton(text=self.morse[key_2])],
                                         [KeyboardButton(text=self.morse[key_3]), KeyboardButton(text=self.morse[key_4])]
                                    ],
                                    resize_keyboard=True, one_time_keyboard=False
                                ))

            print(self.ris[0])



TOKEN = 'INSERIRE_TOKEN_QUI'
bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MorseQuiz, timeout=3600),
])

MessageLoop(bot).run_as_thread()
print(".. -.     .- - - . ... .-") #in attesa

while 1:
    sleep(60)
