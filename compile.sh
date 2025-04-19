#!/usr/bin/env bash
#
# BY: chadless1
#
# DESCRIPTION:
# 
# execute pyinstaller to create executable file

pyinstaller --hidden-import=html5lib --hidden-import=tabulate --onefile --add-data 'style.tcss:.' --name 'sports' sports_tui.py
