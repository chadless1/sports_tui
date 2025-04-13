#!/usr/bin/env bash
#
# BY: chadless1
#
# DESCRIPTION:
# 
# script using pyinstaller to create executable file
#
pyinstaller --collect-all pyfiglet --hidden-import=html5lib --hidden-import=tabulate --onefile --add-data 'style.tcss:.' --name 'sports' sports_tui.py
