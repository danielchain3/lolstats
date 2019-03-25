from selenium import webdriver
from player import PlayerInfo
from team import Team
import parser, database
import os

def main():
    #url = "https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1071787?gameHash=1d6a8f1e229aff57&tab=stats"
    url = "https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1071778?gameHash=59ed416c4088b7e2&tab=stats"

    # read html
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path = DRIVER_BIN, options=options)
    driver.get(url)

    try:
        match_info_raw = driver.find_element_by_class_name("map-header-additional-details")
        blue_team_raw = driver.find_element_by_class_name("team-100")
        red_team_raw = driver.find_element_by_class_name("team-200")
        stats_raw = driver.find_element_by_tag_name("tbody")

        match_id = url.split("=")[1].split("&")[0] 
        match_info = parser.getMatchInfo(match_info_raw, match_id)
        blue_team = parser.getTeamInfo(blue_team_raw)
        red_team = parser.getTeamInfo(red_team_raw)

        parser.getPlayerStats(stats_raw, blue_team, red_team)

        database.addTeamInfo(blue_team, red_team)
        database.addTeamStats(blue_team, red_team, match_info)
    
    finally:
        driver.quit()   #end process

if __name__ == "__main__":
    main()
