#!/usr/bin/env python3

# libraries
import re
import os

# importing variables from config file
import config

# importing functions from hd_py_functions.py
from functions.hd_py_functions import text_formatter

# Esempio di utilizzo
# text_formatter('input.txt', 'output.md')

# crea cartella config.PATH_LITURGIE_FORMATTED se non esiste
if not os.path.exists(config.PATH_LITURGIE_FORMATTED):
    os.makedirs(config.PATH_LITURGIE_FORMATTED)
    print(f"📁 Directory {config.PATH_LITURGIE_FORMATTED} creata!")

# assegna os.listdir(config.PATH_LITURGIE) a una variabile
liturgie_path = os.listdir(config.PATH_LITURGIE)

# conta il numero di file .txt 
n_files = len([f for f in liturgie_path if f.endswith('.txt')])

# per ogni txt file in PATH_LITURGIE, converti in md usando text_formatter()
for file_name in liturgie_path:
   if file_name.endswith('.txt'):
      print(f"🔄 {liturgie_path.index(file_name)+1}/{n_files}   Converting {file_name} to markdown...")

      # building input and output file paths
      input_file_path = os.path.join(config.PATH_LITURGIE, file_name)
      output_file_path = os.path.join(config.PATH_LITURGIE_FORMATTED, file_name.replace('.txt', '.md'))

      # convert txt to md
      text_formatter(input_file_path, os.path.join(config.PATH_LITURGIE_FORMATTED,file_name.replace('.txt', '.md')))

      # wait for user input
      # input("Press Enter to continue...")

# print output message
print("🎉 All liturgies converted to markdown!")
print(f"📁 Directory {config.PATH_LITURGIE_FORMATTED} contains all the formatted liturgies.")
