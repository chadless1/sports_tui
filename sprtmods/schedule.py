#!/usr/bin/env python3
#
# BY: chadless1
#
# DESCRIPTION:
#
# container to display selected sport schedule
# defaults to current day
# options:
#   - yesterday
#   - today
#   - tomorrow

import itertools
import pandas as pd
from bs4 import BeautifulSoup 
from requests import get 
from textual.binding import Binding
from textual import on
from textual.widgets import Label, Markdown, Select
from textual.containers import ScrollableContainer
from textual import work
from datetime import datetime, timedelta

class ScheduleContainer(ScrollableContainer):
    # vim bindings
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
        date_options = ['Yesterday', 'Today', 'Tomorrow']
        yield Select.from_values(date_options, value=date_options[1])

    async def on_mount(self):
        select_date = self.query_one(Select)
        self.load_data(select_date.value)
    
    @on(Select.Changed)
    def select_change(self, event):
        self.load_data(event.value)

    @work(exclusive=True)
    async def load_data(self, date):
        # delete contents for change
        lb = self.query(Label).remove()
        md = self.query(Markdown).remove()

        # create date objects
        today = datetime.today().strftime('%Y%m%d')
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
        yesterday = (datetime.today() + timedelta(days=-1)).strftime('%Y%m%d')
        date_dic = {'Yesterday': yesterday, 'Today': today, 'Tomorrow': tomorrow}
        
        # get schedule from url and create dataframe
        url = 'https://www.cbssports.com/{}/schedule/{}'.format(self.sport,
                    date_dic[date])

        try:
            df = pd.read_html(url)

            # get dates from bs4
            url_date = get('https://www.cbssports.com/{}/schedule/{}'.format(self.sport,
                        date_dic[date]))
            soup = BeautifulSoup(url_date.content, 'html.parser')
            dates = soup.find_all('h4', {'class': 'TableBase-title TableBase-title--large'})
            dates_list = [d.text.strip() for d in dates]
            
            # loop and display
            for date,table in itertools.zip_longest(dates_list, df, fillvalue=' '):
                table = table.iloc[:, 0:4]
                table = table.to_markdown(index=False)
                self.mount(Label(''))
                self.mount(Label(f'[bold purple]{date}[/bold purple]'))           
                self.mount(Label(''))
                self.mount(Markdown(table, classes='mrkdown'))
        except ValueError:
            self.mount(Label('No Data found for selection', id='errmsg'))

