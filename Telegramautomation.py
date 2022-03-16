# File generation 
from datetime import datetime
from os import path
import pandas as pd
import openpyxl
import requests
import sys

def telegram_bot_sendtext(bot_message, TELEGRAM_TOKEN, chat_id):
    bot_token = TELEGRAM_TOKEN
    bot_chatID = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response

def sending_telegram_notification(data_delivery, chat_id, TELEGRAM_TOKEN, API_URL):

        bot_message = data_delivery.to_string()
        response = telegram_bot_sendtext(bot_message, TELEGRAM_TOKEN, chat_id)
        print({"LogInfo":"Sending process is Done ! - Response Status : {} ".format(response.status_code)})
        
def is_descending(list_):
    if len(list_) <= 1:
        return True
    # Strictement inférieur dans chaque enregistrement ou peut etre semblable dans des niveaux successives? Res: oui 
    if list_[0] < list_[1]:
        print({"LogInfo" : "the list values is not in a descending order !"})
        return False
    return is_descending(list_[1:])

def preProcess_collected_data(chat_id, TELEGRAM_TOKEN, API_URL):
    TimeIndicatorList = []
    ValuesList = []
    counter = 0
    InputValuesDict = {}
    
    while True:
        # verify inputs type & methode || ensure that the input value is in the correct format 
        testInput = 0
        while testInput == 0: 
            try:
                NewInput = int(input("\n\n XxX _ Enter the exact {} - th value of a the Stocker Status Please ! = > ".format(counter+1)))
                testInput = 1
#                 print(" XxX _ {} entred value !  ".format(counter))
            except ValueError:
                error_message = {"error": "XxX _ Log Error : the entred value is not valid !"}
                print(error_message)
        
        # assign all inputs to a list with a date entry specification in another list 
        TimeIndicatorList.append(str(datetime.now()))
        ValuesList.append(NewInput)
        
        if len(TimeIndicatorList) == len(ValuesList) and len(ValuesList) == 4:
            # Verify if values are descending or  not and continue the process 
            print({"LogInfo":"We get for the first time the desired level to continue the verification process in this level !"})
            
        elif len(TimeIndicatorList) == len(ValuesList) and len(ValuesList) > 4: 
            # Use the FIFO methode to garantie the data shape equals 20
            TimeIndicatorList = TimeIndicatorList[1:]
            ValuesList = ValuesList[1:]
            
        else:
            # Just continue appending values to the dataFrame   
            print('\n\n')
            counter += 1
            continue
        
        # continue the process after preparing data and limiting it's lenght on 20 elements 
        assert len(ValuesList) == 4, 'Only lists with a length of 20 are accepted for processing.'
        InputValuesDict = dict(zip(TimeIndicatorList, ValuesList))
        
        values = list(InputValuesDict.values())
        if is_descending(values):
            data = {'Date': list(InputValuesDict.keys()), 'Values': list(InputValuesDict.values())}
            data_delivery = pd.DataFrame.from_dict(data)
            print({"LogInfo":"Call the bot groupe, there is a work to do ! "})
            sending_telegram_notification(data_delivery, chat_id, TELEGRAM_TOKEN, API_URL)
        else:
            print({"LogInfo": "data input Nmbr : {} with the value : {}, no need for notification call, 👮: EverEverything's all right !".format(counter, NewInput)})
        counter += 1
       
def main():
    TELEGRAM_TOKEN = '5121400289:AAHRZKx2voyY3HSfHJi2bgsLdHqnKB_WpcY'
    API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}' + '/{method_name}'
# # For a groupe of users grouped on a telegram groupe 
    chat_id = '-783940739'
    
    preProcess_collected_data(chat_id, TELEGRAM_TOKEN, API_URL)
    
if __name__ == '__main__':
    main()