import time
import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import geckodriver_autoinstaller

class Betano:

    def __init__(self):
        geckodriver_autoinstaller.install()

    def get_football_bets(self):
        driver = Firefox()
        
        driver.get("https://www.betano.de/sport/fussball/ligen/216r/")
        driver.minimize_window()

        time.sleep(5)

        class_team_name = 'events-list__grid__info__main__participants'
        class_team_name = 'events-list__grid__event'
        
    
        teams = driver.find_elements(By.CLASS_NAME, class_team_name)
        print(teams)
        print([t.text.split("\n") for t in teams])
        '''
        teams = [team.text.split("\n") for team in teams]
        teams = [team for team in teams if len(team)==2]
        print(teams)

        class_odds = "table__markets__market"
        odds = driver.find_elements(By.CLASS_NAME, class_odds)
        odds = [odd.text.split("\n") for odd in odds]
        odds = [odd[1:] for odd in odds if odd[0]=='Endergebnis']
        print(odds)
        print(len(teams)==len(odds))
        '''

        driver.quit()


if __name__ == '__main__':
    betano = Betano()
    betano.get_football_bets()