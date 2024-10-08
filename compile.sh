#!/usr/bin/env bash
#
# BY: chadless1
#
# DESCRIPTION:
# 
pyinstaller --collect-all pyfiglet --onefile --add-data 'style.tcss:.' --name 'sports' sports_menu.py
