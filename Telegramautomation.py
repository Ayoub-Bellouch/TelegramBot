# File generation 
from datetime import datetime 
from os import path 
import pandas as pd 
import openpyxl
import requests
import sys

def send_local_file(file_path, chat_id, TELEGRAM_TOKEN, API_URL):
    f = open(file_path, 'rb')
    file_bytes = f.read()
    f.close()
    response = {
        'document': (f.name, file_bytes),
        'chat_id': chat_id,
        'TELEGRAM_TOKEN' : TELEGRAM_TOKEN, 
        'API_URL': API_URL
    }
    method_name = 'sendDocument'
    return method_name, response

def send_response(method_name, params):
    API_URL = params['API_URL']
    if method_name == 'sendDocument':
        document = params['document']
        del params['document']
        r = requests.post(url=API_URL.format(method_name=method_name), params=params, files={'document': document})
    else:
        r = requests.post(url=API_URL.format(method_name=method_name), params=params)
    
    return r
#     return r.status_code == 200

def is_descending(list_):
    if len(list_) <= 1:
        return True
    # Strictement inférieur dans chaque enregistrement ou peut etre semblable dans des niveaux successives?
    if list_[0] < list_[1]:
        print({"LogInfo" : "the list values is not in a descending order !"})
        return False
    return is_descending(list_[1:])

def collect_values():
    counter = 0
    InputValuesDict = {}
    while counter <= 20:
        # verify inputs type
        try:
            NewInput = int(input("Enter the exact {} - th value of a the Stocker Status Please ! = > ".format(counter+1)))
        except ValueError:
            error_message = {"error": "XxX _ Log Error : the entred value is not valid !"}
            return error_message
        # assign the inputs to the dictionary with an entry date specification 
        InputValuesDict[str(datetime.now())] = NewInput
        counter += 1
    return InputValuesDict

def file_generation():
    InputDict = collect_values()
    FileInfo_Res  = {}
    FileInfo_Res["path"] = "No path"
    FileInfo_Res["path"] = "No data"
    if "error" in InputDict:
        error_message = InputDict['error']
        return error_message
    
    values = list(InputDict.values())
    print('values : ', values)
    if is_descending(values):
        data = {'Date': list(InputDict.keys()), 'Values': list(InputDict.values())}
        data_frame = pd.DataFrame.from_dict(data)
        
        # Data Saving: Optional or not ? 
        Data_Saving_path = """.\\StockerStatus_Data.xlsx"""
        FileInfo_Res["path"] = Data_Saving_path
        FileInfo_Res["data"] = data_frame
        #
        data_frame.to_excel("""StockerStatus_Data.xlsx""")
        
        return FileInfo_Res
    # The list is not in a descendinf order !
    else:   
        return False
    
def sending_telegram_notification(file_path, chat_id, TELEGRAM_TOKEN, API_URL):
    file_generation_response  = file_generation()
    
    if file_generation_response == False:
        informational_message1 = {"LogInfo": "No warning detected !"}
        return informational_message1

    if path.exists(file_generation_response["path"]):
        method_name, params = send_local_file(file_path, chat_id, TELEGRAM_TOKEN, API_URL)
        response = send_response(method_name, params)
        print({"LogInfo":"Sending process is Done ! - Response Status : {} ".format(response.status_code)})
    else:
        error_message = {"error": "saving data failure !"}
        return error_message
		
def main():
    file_path = ".\\StockerStatus_Data.xlsx"
    TELEGRAM_TOKEN = '5121400289:AAHRZKx2voyY3HSfHJi2bgsLdHqnKB_WpcY'
    API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}' + '/{method_name}'
    chat_id = '1104376640'

    sending_telegram_notification(file_path, chat_id, TELEGRAM_TOKEN, API_URL)
    
if __name__ == '__main__':
    main()
    