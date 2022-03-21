from datetime import datetime,timedelta
from os import path
import pandas as pd
import numpy as np
import requests
import schedule
import openpyxl
import random
import time
import sys

def DataToString(dataFrame):

    columns = list(dataFrame.columns)

    lengthColMax = 0

    for col in columns:
        if lengthColMax < len(col):
            lengthColMax = len(col)
    # definire la langueur de la plus grande cellule :
    for index, row in dataFrame.iterrows():
        for col in columns:
            if lengthColMax < len(row[col]):
                lengthColMax = len(row[col])+1

    # fixé une valeur paire de cette valeur: Val modulo 2 = 0
    if bool(lengthColMax % 2):
        lengthColMax += 1
#     print("Max Lenght : {} \n ".format(lengthColMax))

    StringData = ''
    lenghDelta = 0
    
    for col in columns:
        additionalSpaces2 = 0
        lenghDelta = lengthColMax - len(col)
        additionalSpaces = lenghDelta//2+bool(lenghDelta % 2)

        addedValue = additionalSpaces*" "+col+" "*additionalSpaces2

    #     while len(addedValue) != lengthColMax:
        if len(addedValue) > lengthColMax:
            additionalSpaces2 = additionalSpaces - 1
        elif len(addedValue) < lengthColMax:
            additionalSpaces2 = additionalSpaces + 1
        else:
            additionalSpaces2 = additionalSpaces

            addedValue = additionalSpaces*" "+col+" "*additionalSpaces2

        StringData += addedValue
#         print("Delta : ", lenghDelta, ' --> ', additionalSpaces, ' Total length: ', len(addedValue))
#         print(StringData)

    StringData += "\n"+(lengthColMax*len(columns)+2)*"-"+"\n"

    for index, row in dataFrame.iterrows():
        lenghDelta = 0
        for col in columns:
            lenghDelta = lengthColMax - len(row[col])
            additionalSpaces = lenghDelta//2+bool(lenghDelta % 2)

            if additionalSpaces*2+len(row[col]) > lengthColMax:
                additionalSpaces2 = additionalSpaces - 1
            elif additionalSpaces*2+len(row[col]) < lengthColMax:
                additionalSpaces2 = additionalSpaces + 1
            else:
                additionalSpaces2 = additionalSpaces

            addedValue = additionalSpaces*" "+row[col]+" "*additionalSpaces2+"|"
            StringData += addedValue
#             print("Delta : ", lenghDelta, ' --> ', additionalSpaces, ' Total length: ', len(addedValue))
#             print(StringData)

        StringData += "\n"
    return StringData


def telegram_bot_sendtext(bot_message, TELEGRAM_TOKEN, chat_id):
    bot_token = TELEGRAM_TOKEN
    bot_chatID = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)
    return response.text

import schedule
import time

def generate_data():
    ar = np.array([["loader", random.randint(0,102)], ["CuttingCellNbr1",random.randint(0,882)], ["CuttingCellNbr2", random.randint(0,442)], ["CuttingCellNbr3", random.randint(400,1500)], ["FurnaceExit", random.randint(0,2222)]])
    df = pd.DataFrame(ar, index = [' ', ' ', ' ', '', ''], columns = [' name ', ' value '])
    msg_entete = "Recap du : "+str(datetime.now()).split('.')[0]+"\n"
    bot_message = msg_entete+"\n"+DataToString(df)
    message_info = {"LogInfo":bot_message}
    print("LogInfo : \n {}".format(message_info['LogInfo']))
    return bot_message

def main(bot_message, TELEGRAM_TOKEN, chat_id):
    schedule.every().day.at("00:00").do(telegram_bot_sendtext, bot_message, TELEGRAM_TOKEN, chat_id)
    schedule.every().day.at("08:00").do(telegram_bot_sendtext, bot_message= bot_message, TELEGRAM_TOKEN= TELEGRAM_TOKEN, chat_id= chat_id)
    schedule.every().day.at("16:00").do(telegram_bot_sendtext, bot_message= bot_message, TELEGRAM_TOKEN= TELEGRAM_TOKEN, chat_id= chat_id)
    # Test runner :
    schedule.every(5).seconds.do(telegram_bot_sendtext, bot_message, TELEGRAM_TOKEN, chat_id)
    while True:
        bot_message = generate_data()
        schedule.run_pending()
        time.sleep(1)


TELEGRAM_TOKEN = '5121400289:AAHRZKx2voyY3HSfHJi2bgsLdHqnKB_WpcY'
# Individual 
# chat_id = '1104376640'
# Groupe
chat_id = '-783940739'
bot_message = generate_data()

if __name__ == '__main__':
    
    main(bot_message, TELEGRAM_TOKEN, chat_id)