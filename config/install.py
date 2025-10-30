import os

import requests

import csv

import pandas as pd

import json

username = os.environ.get('USER')

mc_path = f"/home/{username}/.mc"
dow_path = f"{mc_path}/code/pg/exr/ao/config.py"
pgao = f"{mc_path}/code/pg/pgao.csv"
pg = f"{mc_path}/code/pg/Program-information.json"

mx = "1.0.0"
mn = "0.0.0"

raw_file_url = f"https://raw.githubusercontent.com/MB3501/my_db/main/config/main.py"
data = {
    "index":["23586"],
    "comm":["config"],
    "namefile":["config.py"],
    "version":["0.2.7"],
    "type":["-ao"],
    "ph":["ao"],
    "from":["python3"]
}

vb = {
    "mix" : "1.9.9",
    "min" : "1.0.0"
}

for mm in ["mix", "min"]:
    vb[mm] = vb[mm].split(".")
    i = 0
    for v in vb[mm]:
        vb[mm][i] = int(v)
        i += 1
    vb[mm] = vb[mm][2] + (vb[mm][1] * 10) + (vb[mm][0] * 100)

pgv = {}

with open(pg, 'r') as f:
    datajson = json.load(f)
    pgv["version"] = datajson["ProgramInfo"]["version"].split(".")
    i = 0
    for v in pgv["version"]:
        pgv["version"][i] = int(v)
        i += 1
    pgv["version"] = pgv["version"][2] + (pgv["version"][1] * 10) + (pgv["version"][0] * 100)
    if pgv["version"] <= vb["mix"] and pgv["version"] >= vb["min"]:
        pgv["ioru"] = True
    else:
        pgv["ioru"] = False
        
if pgv["ioru"] == False:
    print("ไม่รองรับกับเวอร์ชั่นนี้")
    ip = input("คุณจะพยายามติดตั้งต่อไหม[y/n] : ")
    if ip.lower().strip() == "y":
        pgv["ioru"] = True

if pgv["ioru"] == True:
    try:
        response = requests.get(raw_file_url)
        
        response.raise_for_status()

        with open(dow_path, 'wb') as f:
            f.write(response.content)
            
            with open(pgao, mode="r", encoding='utf-8', newline='') as file:
                commcsv = csv.DictReader(file)
                pgic = {"update":False}
                for row in commcsv:
                    if row["namefile"] == data["namefile"]:
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
            print(f"ติดตั้ง {data["comm"]} สำเร็จ {data["version"]}")
    except requests.exceptions.RequestException as e:
        print("ติดตั้งไม่สำเร็จ")
