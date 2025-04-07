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
from textual.binding import Binding
from textual import on
from textual.widgets import Label, Markdown
from textual.containers import ScrollableContainer
from textual import work

class ScheduleContainer(ScrollableContainer):

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
        # get schedule from url and create dataframe
        url = 'https://www.cbssports.com/{}/schedule/'.format(self.sport)
        df = pd.read_html(url)

        # get dates from bs4
        url_date = get('https://www.cbssports.com/{}/schedule/'.format(self.sport))
        soup = BeautifulSoup(url_date.content, 'html.parser')
        dates = soup.find_all('h4', {'class': 'TableBase-title TableBase-title--large'})
        dates_list = [d.text.strip() for d in dates]
        
        for date,table in zip(dates_list, df):
            table = table.iloc[:, 0:4]
            table = table.to_markdown(index=False)
            self.mount(Label(f'[bold purple]{date}[/bold purple]'))           
            self.mount(Label(''))
            self.mount(Markdown(table, classes='mrkdown'))

