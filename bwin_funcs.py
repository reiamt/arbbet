import time
import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller


class Bwin:

    def __init__(self):
        geckodriver_autoinstaller.install()
        

    def get_basketball_games(self):
        driver = Firefox()
        driver.minimize_window()
        driver.get("https://sports.bwin.de/en/sports/basketball-7")

        time.sleep(5)

        class_team_names = "participants-pair-game"
        score_names = "grid-scoreboard"

        games = driver.find_elements(By.CLASS_NAME, class_team_names)
        scores = driver.find_elements(By.CLASS_NAME, score_names)
        games = [team.text.split("\n") + score.text.split("\n")
                for team, score in zip(games, scores)]
        print(games)
        for game in games:
            if "@" in game:
                game.remove("@")

        games_frame = pd.DataFrame(
            data=games, columns=["Team1", "Team2", "Team1 points", "Team2 points"])
        games_frame.to_csv('bwin/basketball_games.csv')

        driver.quit()


    def get_football_games(self):
        driver = Firefox()
        #driver.minimize_window()
        #driver.get("https://sports.bwin.de/en/sports/football-4")
        driver.get("https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/deutschland-17/bundesliga-102842")
        time.sleep(5)
        class_team_names = 'participants-pair-game'
        class_score = 'grid-scoreboard'
        class_option = 'grid-group-container'
        class_col_names = 'grid-group-header'
        games = driver.find_elements(By.CLASS_NAME, class_team_names)
        scores = driver.find_elements(By.CLASS_NAME, class_score)
        odds = driver.find_elements(By.CLASS_NAME, class_option)
        cols = driver.find_elements(By.CLASS_NAME, class_col_names)
        cols = [col.text for col in cols]
        cols = list(pd.unique(cols))
        cols = ["Team1", "Team2", "Team1_points", "Team2_points"]+cols
        cols = [c + '_bwin' if 'T' not in c else c for c in cols]
        
        scores = [s.text.split("\n") if len(s.text.split("\n")) == 2 else ['NaN','NaN'] for s in scores]
                
        #odds = [odd.text.split("\n") for odd in odds]
        print(odds)
        try:
            odds.pop(0)
        except Exception as e:
            print(e)
            driver.quit()

        #print([odd.text.split("\n") for odd in odds])
        games = [team.text.split("\n") + score + odd.text.split("\n")
                for team, score, odd in zip(games, scores, odds)]
        
        for game in games:
            if "@" in game:
                game.remove("@")
                
        games_df = pd.DataFrame(
            data=games, columns=cols)
        
    
        games_df[cols[4:]] = games_df[cols[4:]].replace(',','.', regex=True)
        games_df[cols[4:]] = games_df[cols[4:]].astype(float)
        
        
        #games_df["prob"] = games_df['1'].apply(lambda x: 1/x) + games_df['X'].apply(lambda x: 1/x) + games_df['2'].apply(lambda x: 1/x)
        

        driver.quit()

        return games_df


if __name__ == '__main__':
    #geckodriver_autoinstaller.install()
    bwin = Bwin()
    games = bwin.get_football_games()
    print(games)
