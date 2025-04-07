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

import sys
import pandas as pd
from bs4 import BeautifulSoup 
from requests import get 
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ListView, ListItem
from textual.widgets import Label, Rule, TabbedContent, Markdown
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import Container, ScrollableContainer
from textual import work
from textual.lazy import Lazy
from sprtmods.standings import StandingsContainer
from sprtmods.schedule import ScheduleContainer
from sprtmods.injury import InjuryContainer

__version__ = 1.1

class SportsScreen(Screen):

    BINDINGS = [
            ("backspace", "app.pop_screen", "Back"),
            ("escape", "app.pop_screen", "Back")
            ]

    sport_name = reactive('sport', recompose=True)
    
    def compose(self):
        
        ## display content ##
        yield Header()
        with Container(classes='top'):
            #yield Label(pyfiglet.figlet_format(self.sport_name, font='small'), id='sportTitle')
            yield Label(self.sport_name.upper(), id='sportTitle')
            yield Rule(line_style='heavy')
        with Container(classes='bottom'):
            with TabbedContent('Schedule', 'Standings', 'Injury Report', classes='bottom'):
                yield Lazy(ScheduleContainer(self.sport_name, 'schedule'))
                yield Lazy(StandingsContainer(self.sport_name, 'standings'))
                yield Lazy(InjuryContainer(self.sport_name, 'injury'))
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
        yield Label(' Select a Sport ...')
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
