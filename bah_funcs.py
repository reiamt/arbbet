import time
import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller


class BAH:

    def __init__(self):
        geckodriver_autoinstaller.install()
    

    def get_football_bets(self):
        driver = Firefox()
        driver.minimize_window()
        driver.get("https://www.bet-at-home.de/mobile/de/sport/fussball/deutschland/bundesliga/2277364")

        time.sleep(5)

        class_team_name = 'list__item-header'
        class_odds = 'ui-grid-b'
        teams = driver.find_elements(By.CLASS_NAME, class_team_name)
        teams = [team.text.split(' - ') for team in teams]
        
        odds = driver.find_elements(By.CLASS_NAME, class_odds)
        odds = [odd.text.split("\n") for odd in odds]
    
        odds = [odd for odd in odds if len(odd) != 1] #remove empty items
        
        games = []
        for team, odd in zip(teams, odds):
            odd = [float(o) for o in odd if o not in ['1','X','2']]
            games.append(team + odd)

        cols = ['Team1','Team2','1','X','2']
        cols = [c + '_bah' if 'T' not in c else c for c in cols]
        games_df = pd.DataFrame(columns=cols, data = games)
        #games_df["prob"] = games_df['1'].apply(lambda x: 1/x) + games_df['X'].apply(lambda x: 1/x) + games_df['2'].apply(lambda x: 1/x)

        driver.quit()

        return games_df

if __name__ == '__main__':
    geckodriver_autoinstaller.install()
    bah = BAH()
    games = bah.get_football_bets()
    print(games)