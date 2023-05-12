import time
import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller


def get_basketball_games():
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
    games_frame.to_csv('basketball_games.csv')

    driver.quit()


def get_football_games():
    driver = Firefox()
    driver.minimize_window()
    driver.get("https://sports.bwin.de/en/sports/football-4")
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
    cols = ["Team1", "Team2", "Team1 points", "Team2 points"]+cols
    #odds = [odd.text.split("\n") for odd in odds]
    odds.pop(0)
    #print([odd.text.split("\n") for odd in odds])
    games = [team.text.split("\n") + score.text.split("\n") + odd.text.split("\n")
             for team, score, odd in zip(games, scores, odds)]
    
    for game in games:
        if "@" in game:
            game.remove("@")
            
    games_frame = pd.DataFrame(
        data=games, columns=cols)
    games_frame.to_csv('football_games.csv')

    driver.quit()


if __name__ == '__main__':
    geckodriver_autoinstaller.install()
    get_football_games()
