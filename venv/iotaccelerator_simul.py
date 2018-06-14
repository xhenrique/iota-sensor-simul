#AUTOR : JOSE XAVIER
#ULTIMA MODIFICAÇÃO : 20/04/2018 12:02


#NECESSARIO INSTALAR A BIBLIOTECA REQUESTS
import requests
import random
import json
import time
from tkinter import Tk, Label, Button, OptionMenu, Text, PhotoImage, StringVar, Image
from threading import Thread

#MODELO DE PAYLOAD DO DDM                       este campo representa o endpoint do device que está sendo referenciado no DDM
payload ="{\"bu\":\"default-unit\",\"e\":[{\"n\":\"testDev/3303/0/5700\",\"u\":\"default-unit\",\"v\":0,\"bv\":null,\"sv\":null,\"t\":1522245761.295}]}"

#A CHAVE DE AUTORIZAÇÃO DEVE SER RECUPERADA DO TICKET DO GATEWAY ONDE O DEVICE ESTÁ REGISTRADO
#ESSA CHAVE ESTÁ DENTRO DO CAMPO "OUTBOX ACCESS TICKET"
dataCollectorId = "e7ea53a2-3bc5-4bac-9d89-497313e6c2c5"
auth = "SharedAccessSignature sr=https%3a%2f%2fiotabusinesslab.servicebus.windows.net%2fdatacollectoroutbox%2fpublishers%2fe7ea53a2-3bc5-4bac-9d89-497313e6c2c5%2fmessages&sig=fwIoUJdEffKJRONb2mGUOTLaq3cF2HnWAOCf0%2fX8%2f%2fM%3d&se=4681981352&skn=SendAccessPolicy"

headers = {
    'DataCollectorId': dataCollectorId,
    'Authorization': auth,
    'PayloadType': "application/senml+json",
    'Content-Type': "application/json",
    'Cache-Control': "no-cache"

}
headers2 = {
    'PayloadType': "application/text",
    'Content-Type': "text/plain",
    'Cache-Control': "no-cache"

}
#VARIÁVEL DE CONTROLE DE FLUXO
end = False

#ENDEREÇO QUE É FEITO OS POSTS NO DDM, ALTERA-SE APENAS O DATACOLLECTORID PARA REFERENCIAR OUTROS DEVICES
url = "https://iotabusinesslab.servicebus.windows.net/datacollectoroutbox/publishers/"+dataCollectorId+"/messages"
value = 0

#VARIÁVEL DE CONTROLE DE FLUXO
flag = False

#FUNÇÃO PARA PARAR O ENVIO
def raise_flag():
    global flag
    flag = True
    btnStop['text']= 'Stoped!'
    btnLaunch['text']='Start again?'

#RESPONSAVEL PELA ATUALIZAÇÃO DOS VALORES NA UI
def attLabel():
    global value
    lbl1['text'] = str(value)
    lbl1.update_idletasks()

#COMEÇA O ENVIO DE DADOS
def begin():
    cont = 0
    btnLaunch['text']='Sending Data'
    global value
    global flag
    while flag or True:
        payload_json = json.loads(payload)
        value = random.randrange(40,65)
        payload_json['e'][0]['v'] = value
        #payload_json['e'][0]['t'] = time.time()

        print(payload_json['e'][0]['v'])
        response = requests.request("POST", url, json=payload_json, headers=headers, timeout= 15)
        time.sleep(5)
        response.close()
        #response2 = requests.request('POST', 'http://ptsv2.com/t/y524k-1526300901/post', data=payload_json, auth=('user','pass'))
        print('DDM' + str(response.status_code))
        #print('ptsv' + str(response2.status_code))
        #print(str(payload_json))
        cont = cont+1
        window.after(300,attLabel)

#INICIA A THREAD DA FUNÇÃO DE ENVIO
#PRECISA SER EM UMA THREAD SEPARADA DA UI PARA NÃO TRAVAR A EXECUÇÃO DA INTERFACE
def endTrue():
    global flag
    send_process = Thread(target=begin)
    send_process.start()
    flag = False

#DEFINIÇÕES DA GUI(BOTÕES/POSIÇÕES/CORES/ETC)
window = Tk()
#image = PhotoImage(file='eri-logo.png')
#lbl_bg = Label(window, image = image)
#lbl_bg.place(x=0,y=0, relwidth=1, relheight=1)
btnLaunch = Button(window, text='Começar envio', width='15',font='Helvetica', fg='white',bg='black', command=endTrue)
btnLaunch.place(x=40,y=150)
btnStop = Button(window, text='Parar envio', width='15',font='Helvetica', fg='white',bg='black', command=raise_flag)
btnStop.place(x=230, y=150)

lbl1 = Label(window, text='Output',font='Helvetica', fg='blue',bg='white')
lbl1.place(x=178, y=215)
lbl2 = Label(window, text= 'APPIoT SENSOR SIMULATOR',font='Helvetica', fg='black',bg='white')
lbl2.place(x=90 ,y=70 )
window.title('SENSOR SIMULATOR')
window.geometry('400x400')
window.mainloop()
