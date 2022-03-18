# File generation 
from datetime import datetime,timedelta
from os import path
import pandas as pd
import numpy as np
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
        msg_entete = "Recap du : "+str(datetime.now()).split('.')[0]
        # Message with full data description:
        bot_message_data = data_delivery.to_string()
        
        # Wanted & Significant Data:
        nbr_glass_on_stocker = list(data_delivery["Values"])[-1]
        time_to_stop_sec = 25 * nbr_glass_on_stocker
        splited_chreno = str(timedelta(seconds=time_to_stop_sec)).split(":")

        estimated_date_of_stop_date = datetime.now() + timedelta(seconds = int(time_to_stop_sec))
        estimated_date_of_stop_str  =  " 💢 Next Stop on:"+str(estimated_date_of_stop_date).split('.')[0]
        
        chreno_to_stop = """     🛑 Warning ⚠ \n {} :  houuurs |\ \n {} : minutes | - > To Stop ! \n {} : seconds |/ """.format(splited_chreno[0], splited_chreno[1], splited_chreno[2])
        # Another way to avoid anotates eliminations
        # ar = np.array([[splited_chreno[0], " : ", "Heurs", "|\\", "", ""], [splited_chreno[1] ," : ", "Minutes ", " | ", " - - >", " To Stop 🛑 "], [splited_chreno[2], " : ", "Seconds", "|/", "", ""],])
        # df = pd.DataFrame(ar, index = [' ', ' ', ' '], columns = ['  ', '  ', '  ', '  ', ' ', ''])
        # chreno_to_stop = df.to_string()
        # print("chreno_to_stop : ", chreno_to_stop)

        bot_message = """{} \n {} \n\n {} """.format(msg_entete, chreno_to_stop, estimated_date_of_stop_str)        
        # print("bot_message : \n ", bot_message)

        # Send Warning Message : 
        response = telegram_bot_sendtext(bot_message, TELEGRAM_TOKEN, chat_id)
        
        print(response.text)
        print({"LogInfo":" Sending process ! - Response Status : {} \n\n".format(response.status_code)})
        
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
        TimeIndicatorList.append(str(datetime.now()).split('.')[0])
        ValuesList.append(NewInput)
        
        if len(TimeIndicatorList) == len(ValuesList) and len(ValuesList) == 20:
            # Verify if values are descending or  not and continue the process 
            print({"LogInfo":"We get for the first time the desired level to continue the verification process in this level !"})
            
        elif len(TimeIndicatorList) == len(ValuesList) and len(ValuesList) > 20: 
            # Use the FIFO methode to garantie the data shape equals 20
            TimeIndicatorList = TimeIndicatorList[1:]
            ValuesList = ValuesList[1:]
            
        else:
            # Just continue appending values to the dataFrame   
            print('\n\n')
            counter += 1
            continue
        
        # continue the process after preparing data and limiting it's lenght on 20 elements 
        assert len(ValuesList) == 20, 'Only lists with a length of 20 are accepted for processing.'
        InputValuesDict = dict(zip(TimeIndicatorList, ValuesList))
        print("InputValuesDict -> ", InputValuesDict)
        values = list(InputValuesDict.values())
        print("Values  -> ", values)
        # verify the descendence of data to send a notification call !
        if is_descending(values):
            data = {'Date': list(InputValuesDict.keys()), 'Values': list(InputValuesDict.values())}
            data_delivery = pd.DataFrame.from_dict(data)
            print(data_delivery)
            print({"LogInfo":"Call the bot groupe, there is a work to do ! "})
            sending_telegram_notification(data_delivery, chat_id, TELEGRAM_TOKEN, API_URL)
            # Sleep the process after sending the notification !
            sleep(600)
        else:
            print({"LogInfo": "data input Nmbr : {} with the value : {}, no need for notification call, 👮: EverEverything's all right !".format(counter, NewInput)})
        counter += 1

def main():
    TELEGRAM_TOKEN = '5121400289:AAHRZKx2voyY3HSfHJi2bgsLdHqnKB_WpcY'
    API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}' + '/{method_name}'
# # For a groupe of users grouped on a telegram groupe 
    chat_id = '-783940739'
    # Origin !
    preProcess_collected_data(chat_id, TELEGRAM_TOKEN, API_URL)
    
if __name__ == '__main__':
    main()