#!Scripts/.venv/bin/python3

import os 
import pandas as pd
from bs4 import BeautifulSoup 
from requests import get 
import pyfiglet
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem
from textual.widgets import Label, Pretty, Rule
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import Container, ScrollableContainer

class SportsTableContainer(ScrollableContainer):

    BINDINGS = [
            Binding("up", "scroll_up", "Scroll Up", show=False),
            Binding("k", "scroll_up", "Scroll Up", show=False),
            Binding("down", "scroll_down", "Scroll Down", show=False),
            Binding("j", "scroll_down", "Scroll Down", show=False),
            ]

class SportsScreen(Screen):

    BINDINGS = [
            ("backspace", "app.pop_screen", "Back"),
            ("escape", "app.pop_screen", "Back")
            ]

    sport_name = reactive('sport', recompose=True)
    
    def compose(self):

        # get schedule from url and create dataframe
        url = 'https://www.cbssports.com/{}/schedule/'.format(self.sport_name)
        df = pd.read_html(url)

        # get dates from bs4
        url_date = get('https://www.cbssports.com/{}/schedule/'.format(self.sport_name))
        soup = BeautifulSoup(url_date.content, 'html.parser')
        dates = soup.find_all('h4', {'class': 'TableBase-title TableBase-title--large'})

        yield Header()
        with Container(classes='top'):
            yield Label(pyfiglet.figlet_format(self.sport_name, font='banner4'), id='sportTitle')
            yield Rule(line_style='ascii')
        with SportsTableContainer(classes='bottom'):
            for date,table in zip(dates, df):
                table = table.iloc[:, 0:3]
                yield Label(f'[bold purple]{date.text.strip()}[/bold purple]')
                yield Label('')
                yield Pretty(table)
                yield Label('')
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
            ('q', 'close_window', 'Exit'),
            ('escape', 'close_window', 'Exit'),
            ('d', 'toggle_dark', 'Toggle Dark Mode'),
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
        
##########################
 
if __name__ == '__main__':
    app = Sports()
    app.run()
