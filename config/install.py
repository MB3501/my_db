import os

import requests

import csv

import pandas as pd

from colorama import Fore, Style, init, Back

username = os.environ.get('USER')

mc_path = f"/home/{username}/.mc"
dow_path = f"{mc_path}/code/pg/exr/ao/config.py"
pgao = f"{mc_path}/code/pg/pgao.csv"

raw_file_url = f"https://raw.githubusercontent.com/MB3501/my_db/main/config/main.py"
data = {
    "index":["23586"],
    "comm":["config"],
    "namefile":["config.py"],
    "version":["0.1.5"],
    "type":["-ao"],
    "ph":["ao"],
    "from":["python3"]
}

try:
    response = requests.get(raw_file_url)
    
    response.raise_for_status()

    with open(dow_path, 'wb') as f:
        f.write(response.content)
        
        with open(pgao, mode="r", encoding='utf-8', newline='') as file:
            commcsv = csv.DictReader(file)
            pgic = {"update":False}
            for row in commcsv:
                if row["namefile"] == "config.py":
                    pgic = {"update":True}
                    break
                else:
                    pgic = {"update":False}
            df_append = pd.DataFrame(data)
            df_append.to_csv(
                pgao, 
                mode='w',
                header=True,
                index=False
            )
    if pgic["update"] == False:
        print("ติดตั้งสำเร็จ")
    else:
        print(f"อัพเดทเป็น {data["version"]}")
except requests.exceptions.RequestException as e:
    print("ติดตั้งไม่สำเร็จ")
