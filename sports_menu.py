#!Scripts/.venv/bin/python3

import os 
import pandas as pd
from bs4 import BeautifulSoup 
from requests import get 
from tabulate import tabulate
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem
from textual.widgets import Label, Pretty, Rule
from textual.widget import Widget
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import Vertical, Container

class SportsScreen(Screen):

    BINDINGS = [("escape", "app.pop_screen", "Back")]

    sport_name = reactive('sport', recompose=True)

    def compose(self):
        yield Header()
        yield Label(self.sport_name, classes='sport')
        yield Rule(line_style='ascii', classes='sport')
        yield Pretty(run_sport(self.sport_name), classes='sport')
        yield Footer()
   
class SportsListView(ListView):

    BINDINGS = [
            Binding("enter", "select_cursor", "Select", show=False),
            Binding("up", "cursor_up", "Cursor Up", show=False),
            Binding("k", "cursor_up", "Cursor Up", show=False),
            Binding("down", "cursor_down", "Cursor Down", show=False),
            Binding("j", "cursor_down", "Cursor Down", show=False),
            ]
    
class Sports(App):
    
    CSS_PATH = 'style.tcss'
    
    SCREENS = {'sport': SportsScreen}

    BINDINGS = [
            ('escape', 'close_window', 'Exit App'),
            ('q', 'close_window', 'Exit App'),
            ('d', 'toggle_dark', 'Toggle Dark Mode'),
            ("m", "push_screen('sport')", "Change Window"),
            ]
      
    def compose(self):
        yield Header()
        yield Label(' Select Sport ...')
        yield SportsListView(
                ListItem(Label(':baseball: MLB'), name='mlb'),
                ListItem(Label(':basketball: NBA'), name='nba'),
                ListItem(Label(':football: NFL'), name='nfl'),
                ListItem(Label(':ice_hockey: NHL'), name='nhl'),
                )
        yield Footer()

    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_close_window(self):
        self.exit()

    @on(SportsListView.Selected)
    def show_sport(self, event):
        self.push_screen('sport')
        self.query_exactly_one(SportsScreen).sport_name = event.item.name
        
def run_sport(user_input):

    user_input = user_input.lower()

    # get schedule from url and create dataframe
    url = 'https://www.cbssports.com/{}/schedule/'.format(user_input)
    df = pd.read_html(url)

    # get dates from bs4
    url_date = get('https://www.cbssports.com/{}/schedule/'.format(user_input))
    soup = BeautifulSoup(url_date.content, 'html.parser')
    dates = soup.find_all('h4', {'class': 'TableBase-title TableBase-title--large'})

    for table,date in zip(df, dates):

        table = table.iloc[:,0:3]

        #print(date.text.strip())
        return(table)
        
##########################
 
if __name__ == '__main__':
    app = Sports()
    app.run()
