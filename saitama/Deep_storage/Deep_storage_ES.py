


from datetime import date, datetime, timedelta
today = date.today()

def grab_data(isin,from_date):   # "YEAR-MONTH-DATE"     
    import requests
    url = f'https://api.upstox.com/v2/historical-candle/{isin}/1minute/{today}/{from_date}'
    headers = {  'Accept': 'application/json'   }
    response = requests.get(url, headers=headers)
    #open('file name.txt','w').write(response.text)
    return response.text


def deep(isin,file_path):
    import os
    if os.path.isfile(file_path):
        print(f" File '{file_path}' exists! Appending to it. ")
        import json
        with open(file_path, 'r') as file:
            old_data = json.load(file)
        old_data_candles=old_data['data']['candles']
        last_update_string=old_data_candles[0]          #["2024-11-13T15:29:00+05:30",70.98,71.05,70.85,71.04,286908,0]
        last_update_date=last_update_string[0].split("T")[0]
        # Convert late_update_date string to datetime object
        last_update_date = datetime.strptime(last_update_date, "%Y-%m-%d")
        # Add one day
        from_date = last_update_date + timedelta(days=1)
        # Convert back to string (optional)
        from_date = from_date.strftime("%Y-%m-%d")
        new_data=json.loads(grab_data(isin,from_date))
        #print(json.loads(new_data)['data']['candles'])
        if new_data['status']=="success" and len(new_data['data']['candles'])>0:
            combined_data_candles=new_data['data']['candles']+old_data['data']['candles']  #if i dont use the old_data_candles directly will i create this thing again unncecessarily in RAM
            new_data['data']['candles'] = combined_data_candles
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(new_data, file)  # , indent=4 preety-printed JSON

           
    else:        # If  file does not exist. Downloading, checking non-emptiness, creating file and writing.
        print(f" Creating file '{file_path}'. Saving to it. ")
        from_date='1900-01-01'
        import json
        data=json.loads(grab_data(isin,from_date))
        if data['status']=="success" and len(data['data']['candles'])>0:
            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(data,file)
        else:
            print('Data is not available for isin='+isin+' or downloading error.')
        #Result of this part is: an empty file will never be created


def panda():
    import pandas as pd
    # Read the CSV file
    data = pd.read_csv("E:/RV/saitama/Deep_storage/EQUITY_L.csv")
    # Strip leading and trailing whitespace from column names
    data.columns = data.columns.str.strip()
    # Access specific columns    print(data['NAME OF COMPANY'])
    #print(len(data['NAME OF COMPANY']))            print(len(data['ISIN NUMBER']))
    #s=data.loc[6, "NAME OF COMPANY"]   print(s)     print(len(data.iloc[:, 2]))   print(len(data['SERIES']))
    #print(data["FACE VALUE"].count())  non-null values
    #s=data.loc[6, "NAME OF COMPANY"]   print(s)     print(len(data.iloc[:, 2]))   
    #print(data['SYMBOL'][2])

    for n in range(0,len(data['ISIN NUMBER'])):                 ################ -2030
       c_isin=data['ISIN NUMBER'][n]
       c_symbol=data['SYMBOL'][n]
       file_name=c_symbol+'_'+c_isin+'.txt'

       file_path = "E:/RV/saitama/Deep_storage/Equity_storage/"+file_name

       isin='NSE_EQ|'+c_isin
       deep(isin,file_path) 
       


def error(): ## see how error handling happens
    import json
    import os

    def write_data(file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            print(f"Data successfully written to '{file_path}'.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")
        except TypeError as e:
            print(f"Data serialization error: {e}")

    def read_data(file_path):
        if not os.path.isfile(file_path):
            print(f"File '{file_path}' does not exist.")
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"Data successfully read from '{file_path}':")
            print(data)
            return data
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    # Example Usage
    file_path = "output.txt"
    new_data = {
        "name": "Alice",
        "age": 30,
        "is_member": True
    }

    write_data(file_path, new_data)
    read_data(file_path)



if __name__ == '__main__':
    panda()       

