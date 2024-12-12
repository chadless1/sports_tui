#!Scripts/.venv/bin/python3

import os 
import sys
import pandas as pd
from bs4 import BeautifulSoup 
from requests import get 
from tabulate import tabulate
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem
from textual.widgets import Label, Pretty, Rule, TabbedContent
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import Container, ScrollableContainer

__version__ = 1.0

class SportsTableContainer(ScrollableContainer):

    BINDINGS = [
            Binding("k", "scroll_up", "Scroll Up", show=False),
            Binding("j", "scroll_down", "Scroll Down", show=False),
            Binding("h", "scroll_left", "Scroll Left", show=False),
            Binding("l", "scroll_right", "Scroll Right", show=False),
            ]

class SportsScreen(Screen):

    BINDINGS = [
            ("backspace", "app.pop_screen", "Back"),
            ("escape", "app.pop_screen", "Back")
            ]

    sport_name = reactive('sport', recompose=True)
    
    def compose(self):

        ## schedule ##
        # get schedule from url and create dataframe
        url = 'https://www.cbssports.com/{}/schedule/'.format(self.sport_name)
        df = pd.read_html(url)

        # get dates from bs4
        url_date = get('https://www.cbssports.com/{}/schedule/'.format(self.sport_name))
        soup = BeautifulSoup(url_date.content, 'html.parser')
        dates = soup.find_all('h4', {'class': 'TableBase-title TableBase-title--large'})
        
        ## standings ##
        url_standings = 'https://www.cbssports.com/{}/standings/'.format(self.sport_name)
        df_standings = pd.read_html(url_standings)

        ## injury ##
        url_injury = 'https://www.cbssports.com/{}/injuries/'.format(self.sport_name)
        df_injury = pd.read_html(url_injury)

        # get team name from bs4
        url_team_name = get('https://www.cbssports.com/{}/injuries/'.format(self.sport_name))
        soup = BeautifulSoup(url_team_name.content, 'html.parser')
        team_name = soup.find_all('span', {'class': 'TeamName'})
        
        ## display content ##
        yield Header()
        with Container(classes='top'):
            #yield Label(pyfiglet.figlet_format(self.sport_name, font='small'), id='sportTitle')
            yield Label(self.sport_name.upper(), id='sportTitle')
            yield Rule(line_style='ascii')
        with Container(classes='bottom'):
            with TabbedContent('Schedule', 'Standings', 'Injury', classes='bottom'):
                # schedule
                with SportsTableContainer(classes='bottom'):
                    for date,table in zip(dates, df):
                        table = table.iloc[:, 0:3]
                        yield Label(f'[bold purple]{date.text.strip()}[/bold purple]')
                        yield Label('')
                        yield Pretty(table)
                        yield Label('')
                # standings
                with SportsTableContainer(classes='bottom'):
                    if self.sport_name == 'mlb':
                        df1 = df_standings[1]
                        df1 = df1.iloc[:, 0:3]
                        df1 = df1.droplevel(0, axis=1)
                        df1 = df1.dropna()
                        df2 = df_standings[3]
                        df2 = df2.iloc[:, 0:3]
                        df2 = df2.droplevel(0, axis=1)
                        df2 = df2.dropna()
                        yield Label('[bold purple]American[/bold purple]')
                        yield Pretty(df1)
                        yield Label('[bold purple]National[/bold purple]')
                        yield Pretty(df2)
                        yield Label('')
                    elif self.sport_name == 'nba':
                        df1 = df_standings[0]
                        df1 = df1.iloc[:, 1:5]
                        df1 = df1.droplevel(0, axis=1)
                        df1 = df1.dropna()
                        df2 = df_standings[1]
                        df2 = df2.iloc[:, 1:5]
                        df2 = df2.droplevel(0, axis=1)
                        df2 = df2.dropna()
                        yield Label('[bold purple]Eastern[/bold purple]')
                        yield Pretty(df1)
                        yield Label('[bold purple]Western[/bold purple]')
                        yield Pretty(df2)
                        yield Label('')
                    elif self.sport_name == 'nhl':
                        df1 = df_standings[0]
                        df1 = df1.iloc[:, 0:6]
                        df1 = df1.droplevel(0, axis=1)
                        df1 = df1.dropna()
                        df2 = df_standings[1]
                        df2 = df2.iloc[:, 0:6]
                        df2 = df2.droplevel(0, axis=1)
                        df2 = df2.dropna()
                        yield Label('[bold purple]Eastern[/bold purple]')
                        yield Pretty(df1)
                        yield Label('[bold purple]Western[/bold purple]')
                        yield Pretty(df2)
                        yield Label('')
                    elif self.sport_name == 'nfl':
                        df1 = df_standings[0]
                        df1 = df1.iloc[:, 0:4]
                        df1 = df1.droplevel(0, axis=1)
                        df1 = df1.dropna()
                        df2 = df_standings[1]
                        df2 = df2.iloc[:, 0:4]
                        df2 = df2.droplevel(0, axis=1)
                        df2 = df2.dropna()
                        yield Label('[bold purple]AFC[/bold purple]')
                        yield Pretty(df1)
                        yield Label('[bold purple]NFC[/bold purple]')
                        yield Pretty(df2)
                        yield Label('')

                # injury
                with SportsTableContainer(classes='bottom'):
                    for name,table in zip(team_name, df_injury):
                        table['first_name'] = table['Player'].str.split().str[0]
                        table['last_name'] = table['Player'].str.split().str[2]
                        table['Player'] = table['first_name'] + table['last_name']
                        table = table.drop(['first_name', 'last_name'], axis=1)
                        yield Label(f'[bold purple][u]{name.text.strip()}[/u][/bold purple]')
                        yield Label('')
                        yield Label(tabulate(table, headers='keys', showindex=False))
                        yield Label('')
        yield Footer()
   
class SportsListView(ListView):

    BINDINGS = [
            Binding("enter", "select_cursor", "Select", show=False),
            Binding("k", "cursor_up", "Cursor Up", show=False),
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
    if len(sys.argv) < 2:
        app.run()
    elif sys.argv[1] in ['-v', '--version']:
        print(f'Sports  version {__version__}')
