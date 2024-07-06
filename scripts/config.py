#!/usr/bin/env python3

import configparser

path_config_file = r'scripts/config.ini'

cp = configparser.ConfigParser()
cp.optionxform = str

cp.read(path_config_file)

variables = dict(cp.items('hildegard'))
# print(variables)

# pause 
# input("Press Enter to continue...")

for value in variables:
   exec(f"{value}={variables[value]}")

# print(PATH_LITURGIA)

# print output message
print("💻 Variables from config file imported!")