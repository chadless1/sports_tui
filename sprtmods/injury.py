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
from textual.widgets import Label, Markdown, Select, Static
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual import work

team_list = []

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
    
    def compose(self):
        yield Static('Select Team')

    def on_mount(self):
        # get team name from bs4
        url_team_name = get('https://www.cbssports.com/{}/injuries/'.format(self.sport))
        soup = BeautifulSoup(url_team_name.content, 'html.parser')
        team_names = soup.find_all('span', {'class': 'TeamName'})   

        for team in team_names:
            team_list.append(team.text.strip())

        self.mount(Select.from_values(team_list))

    @on(Select.Changed)
    def select_change(self, event):
        self.load_data(event.value)

    @work(exclusive=True)
    async def load_data(self, team):
        # remove old data
        self.query(Label).remove()
        self.query(Markdown).remove()

        # get injury from url and create dataframe
        url = 'https://www.cbssports.com/{}/injuries/'.format(self.sport)
        df = pd.read_html(url)
        df_list = []
        
        for table in df:
            table['first_name'] = table['Player'].str.split().str[0]
            table['last_name'] = table['Player'].str.split().str[2]
            table['Player'] = table['first_name'] + table['last_name']
            table = table.drop(['first_name', 'last_name'], axis=1)
            table_md = table.to_markdown(index=False)
            df_list.append(table_md)
       
        team_dict = dict(zip(team_list, df_list))
       
        self.mount(Label(''))
        self.mount(Label(f'[bold purple][u]{team}[/u][/bold purple]'))
        self.mount(Label(''))
        self.mount(Markdown(team_dict[team]))
        self.mount(Label(''))

