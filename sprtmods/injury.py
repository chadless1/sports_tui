#!/usr/bin/env python3
#
# BY: chadless1
#
# DESCRIPTION:
#
# a simple sports tui app
#
# select sport and view data
#  - schedule
#  - standings
#  - injury Report

import pandas as pd
from bs4 import BeautifulSoup 
from requests import get 
from textual import on
from textual.widgets import Label, Markdown
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual import work

class InjuryContainer(ScrollableContainer):

    BINDINGS = [
            Binding("k", "scroll_up", "Scroll Up", show=False),
            Binding("j", "scroll_down", "Scroll Down", show=False),
            Binding("h", "scroll_left", "Scroll Left", show=False),
            Binding("l", "scroll_right", "Scroll Right", show=False),
            ]

    def __init__(self, sport, id):
        self.sport = sport
        super().__init__(id=id)
    
    async def on_mount(self):
        self.load_data()
    
    @work(exclusive=True)
    async def load_data(self):
        # get injury from url and create dataframe
        url = 'https://www.cbssports.com/{}/injuries/'.format(self.sport)
        df = pd.read_html(url)

        # get team name from bs4
        url_team_name = get('https://www.cbssports.com/{}/injuries/'.format(self.sport))
        soup = BeautifulSoup(url_team_name.content, 'html.parser')
        team_names = soup.find_all('span', {'class': 'TeamName'})   

        for name,table in zip(team_names, df):
            table['first_name'] = table['Player'].str.split().str[0]
            table['last_name'] = table['Player'].str.split().str[2]
            table['Player'] = table['first_name'] + table['last_name']
            table = table.drop(['first_name', 'last_name'], axis=1)
            table_md = table.to_markdown(index=False)
            self.mount(Label(f'[bold purple][u]{name.text.strip()}[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(table_md))
            self.mount(Label(''))

