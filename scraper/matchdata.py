from bs4 import BeautifulSoup
from selenium import webdriver
from player import PlayerInfo
from team import Team
import os

def main():
    url = "https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT01/1071778?gameHash=59ed416c4088b7e2&tab=stats"

    # read html
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path = DRIVER_BIN, options=options)
    driver.get(url)

    blue_team_raw = driver.find_element_by_class_name("team-100")
    red_team_raw = driver.find_element_by_class_name("team-200")
    stats_raw = driver.find_element_by_tag_name("tbody")
    
    blue_team = getTeamInfo(blue_team_raw)
    red_team = getTeamInfo(red_team_raw)

    getPlayerStats(stats_raw, blue_team, red_team)
    print(blue_team)
    print(red_team)


#removes leading and trailing space from text
def formatHTML(raw_html):
    return raw_html.get_attribute("textContent").strip()


def getTeamInfo(team_info, formatText = formatHTML):
    #Put player names in array
    player_names = team_info.find_elements_by_class_name("champion-nameplate-name")
    player_names = list(map(formatText, player_names))

    #Extract team information
    result_raw = team_info.find_element_by_class_name("game-conclusion")
    gold_raw = team_info.find_element_by_class_name("gold")
    kills_raw = team_info.find_element_by_class_name("kills")
    result = formatText(result_raw) == "VICTORY"
    gold = float(formatText(gold_raw).strip("k")) * 1000
    kills = float(formatText(kills_raw))

    team_name = player_names[0].split(" ")[0]
    team = Team(team_name, result, gold, kills)

    #Extract player names
    players = []
    for player in player_names:
        #removes teamname from name
        name = " ".join(player.split(" ")[1:]) 
        players.append(PlayerInfo(name))

    team.players = players

    return team 

def getPlayerStats(raw_html, blue_team, red_team, formatText = formatHTML):
    rows = raw_html.find_elements_by_class_name("grid-row")
    for row in rows:
        stat_type = formatText(row.find_element_by_class_name("grid-label")).lower()
        blue_stats = list(map(formatText, row.find_elements_by_class_name("team-100")))
        red_stats = list(map(formatText, row.find_elements_by_class_name("team-200")))

        stat_type_values = stat_type.split(" ")

        for playerIndex in range(5):
            playerStats = blue_stats[playerIndex]

            if stat_type == "kda":
                playerStats = playerStats.split("/")
                blue_team.players[playerIndex].addInformation("kills", playerStats[0])
                blue_team.players[playerIndex].addInformation("deaths", playerStats[1])
                blue_team.players[playerIndex].addInformation("assists", playerStats[2])

            elif stat_type == "first blood":
                if playerStats == "●":
                    blue_team.players[playerIndex].addInformation(stat_type, True)
                else:
                    blue_team.players[playerIndex].addInformation(stat_type, False)

            elif "largest" in stat_type_values or "wards" in stat_type_values \
                    or "killed" in stat_type_values:
                blue_team.players[playerIndex].addInformation("".join(stat_type), playerStats)

            else: 
                if playerStats != "-":
                    playerStats = int(float(playerStats.split("k")[0]) * 1000)
                blue_team.players[playerIndex].addInformation(stat_type, playerStats)


if __name__ == "__main__":
    main()
