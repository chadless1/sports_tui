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

class StandingsContainer(ScrollableContainer):

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
 
        # get standings from url and create dataframe
        url = 'https://www.cbssports.com/{}/standings/'.format(self.sport)
        df = pd.read_html(url)

        if self.sport == 'mlb':
            df1 = df[1]
            df1 = df1.iloc[:, 0:3]
            df1 = df1.droplevel(0, axis=1)
            df1 = df1.dropna()
            df1_md = df1.to_markdown(index=False)
            df2 = df[3]
            df2 = df2.iloc[:, 0:3]
            df2 = df2.droplevel(0, axis=1)
            df2 = df2.dropna()
            df2_md = df2.to_markdown(index=False)
            self.mount(Label('[bold purple][u]American[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df1_md))
            self.mount(Label('[bold purple][u]National[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df2_md))
            self.mount(Label(''))
        elif self.sport == 'nba':
            df1 = df[0]
            df1 = df1.iloc[:, 1:5]
            df1 = df1.droplevel(0, axis=1)
            df1 = df1.dropna()
            df1_md = df1.to_markdown(index=False)
            df2 = df[1]
            df2 = df2.iloc[:, 1:5]
            df2 = df2.droplevel(0, axis=1)
            df2 = df2.dropna()
            df2_md = df2.to_markdown(index=False)
            self.mount(Label('[bold purple][u]Eastern[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df1_md))
            self.mount(Label('[bold purple][u]Western[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df2_md))
            self.mount(Label(''))
        elif self.sport == 'nhl':
            df1 = df[0]
            df1 = df1.iloc[:, 0:6]
            df1 = df1.droplevel(0, axis=1)
            df1 = df1.dropna()
            df1_md = df1.to_markdown(index=False)
            df2 = df[1]
            df2 = df2.iloc[:, 0:6]
            df2 = df2.droplevel(0, axis=1)
            df2 = df2.dropna()
            df2_md = df2.to_markdown(index=False)
            self.mount(Label('[bold purple][u]Eastern[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df1_md))
            self.mount(Label('[bold purple][u]Western[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df2_md))
            self.mount(Label(''))
        elif self.sport == 'nfl':
            df1 = df[0]
            df1 = df1.iloc[:, 0:4]
            df1 = df1.droplevel(0, axis=1)
            df1 = df1.dropna()
            df1_md = df1.to_markdown(index=False)
            df2 = df[1]
            df2 = df2.iloc[:, 0:4]
            df2 = df2.droplevel(0, axis=1)
            df2 = df2.dropna()
            df2_md = df2.to_markdown(index=False)
            self.mount(Label('[bold purple][u]AFC[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df1_md))
            self.mount(Label('[bold purple][u]NFC[/u][/bold purple]'))
            self.mount(Label(''))
            self.mount(Markdown(df2_md))
            self.mount(Label(''))

