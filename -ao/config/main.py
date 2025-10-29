import os
import configparser
import sys

username = os.environ.get('USER')

mc_path = f"/home/{username}/.mc"

config_fila = f"{mc_path}/code/usr/config.ini"

config = configparser.ConfigParser()

config.read(config_fila)

data_list = {}

while True:
    for section in config.sections():
        for key, value in config.items(section):
            data_list[key] = value
    try:
        with open(config_fila, mode="r", encoding='utf-8') as file:
            row = file.read()
            print(row)
    except IOError as e:
        print(f"ไม่สามารถดูการตั้งค่าได้: {e}")
        sys.exit(1)
    
    cmd = input("set : ")
    cmd = cmd.lower()
    cmd = cmd.split(" ")
    if len(cmd) == 1:
        if cmd[0] in ["exit", "quit"]:
            break
        elif cmd[0] in ["ls"]:
            print(data_list)
            try:
                with open(config_fila, 'w') as configfile:
                    config.write(configfile)
            except IOError as e:
                print(f"ไม่สามารถบันทึกได้: {e}")
                sys.exit(1)
        else:
            setic = cmd[0].split("=")
            data_list[setic[0]] = setic[1]
            if len(setic) == 2:
                config["SETTINGS"] = data_list
