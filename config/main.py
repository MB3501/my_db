import os
import configparser
import sys

username = os.environ.get('USER')

mc_path = f"/home/{username}/.mc"

config_fila = f"{mc_path}/code/usr/config.ini"

os.open(config_fila)
