#!/usr/bin/python3.7

import random, telepot
from string import ascii_lowercase as ascii
from time import sleep
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

bot = telepot.Bot('INSERIRE_TOKEN_QUI')

a = list(ascii)
#a += ['1','2','3','4','5','6','7','8','9','0'] #da aggiungere in futuro
morse = {
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

val_iniz = random.choice(a)
ris = [val_iniz,val_iniz] #aggiungo due valori identici così che quando verrà utilizzato il primo valore per la prima domanda, al secondo ciclo la risposta risulterà comunque corretta...

usrErrCor = {} #user: [errors,correct]

def handle(msg):
    global ris

    content_type, chat_type, chat_id = telepot.glance(msg)
    usr = msg['from']['username']

    #il primo valore è l'ultimo inserito
    ris.insert(0,random.choice(a)) #ogni volta salvo la risposta della domanda in modo da averlo al ciclo successivo
    ris.pop(2) #dal secondo ciclo rimuovo la risposta alla domanda già che è già stata fatta in modo da avere sempre e solo 2 valori in lista.
    r = ris[1] #e uso come risposta corretta quella della domanda più vecchia
    d = ris[0] # come domanda il nuovo valore

    if content_type == 'text':
        text = msg['text']
        if text == morse[r]:
            try: #se per qualche ragione usr non avesse iniziato con /start
                usrErrCor[usr][1] +=1
            except:
                usrErrCor[usr] = [0,1]
        elif text == '/start': #reset totale
            usrErrCor[usr] = [0,0]
            val_iniz = random.choice(a)
            ris = [val_iniz,val_iniz]
            d = ris[0]
        elif text == '/morse':
            val_iniz = random.choice(a)
            ris = [val_iniz,val_iniz] #reset valori iniziali
            d = ris[0]
            codeMorse = str(morse).replace("'",'').replace('{','').replace('}','').replace(',','\n')
            bot.sendMessage(chat_id,codeMorse)
        else:
            try:
                usrErrCor[usr][0] +=1
            except:
                usrErrCor[usr] = [1,0]

    bot.sendMessage(chat_id,("corrette: %d \terrate: %d"%(usrErrCor[usr][1],usrErrCor[usr][0])))

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
                                 [KeyboardButton(text=morse[key_1]), KeyboardButton(text=morse[key_2])],
                                 [KeyboardButton(text=morse[key_3]), KeyboardButton(text=morse[key_4])]
                            ],
                            resize_keyboard=True, one_time_keyboard=True
                        ))




MessageLoop(bot, handle).run_as_thread()
print(".. -.     .- - - . ... .-") #in attesa
while 1:
    sleep(60)



#----------------
# da aggiungere
# tenere traccia degli errori e dei successi in modo da mandare con più probabilità le lettere sbagliate e meno frequentemente quelle corrette (stile SRS)

# v1.8.3 - LearnMorseBot

