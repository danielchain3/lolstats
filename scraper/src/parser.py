from selenium import webdriver
from player import PlayerInfo
from team import Team

def formatHTML(raw_html):
    '''removes leading and trailing space from text'''
    return raw_html.get_attribute("textContent").strip()

def getMatchInfo(match_info, match_id, formatText = formatHTML):
    match_stats = list(map(formatText, match_info.find_elements_by_tag_name("span")))
    match_duration = "00:" + match_stats[1]
    date = match_stats[2].split("/")
    date = date[2] + "-" + date[1] + "-" + date[0]  #ordering depends on region
    
    return {"match_duration": match_duration, "date": date, "match_id" : match_id}

def getTeamInfo(team_info, formatText = formatHTML):
    '''takes team information and generates a team object'''
    #Put player names in array
    player_names = team_info.find_elements_by_class_name("champion-nameplate-name")
    player_names = list(map(formatText, player_names))

    #Extract team information
    result_raw = team_info.find_element_by_class_name("game-conclusion")
    gold_raw = team_info.find_element_by_class_name("gold")
    kills_raw = team_info.find_element_by_class_name("kills")
    towers_raw = team_info.find_element_by_class_name("tower-kills")
    inhibs_raw = team_info.find_element_by_class_name("inhibitor-kills")
    barons_raw = team_info.find_element_by_class_name("baron-kills")
    dragons_raw = team_info.find_element_by_class_name("dragon-kills")
    rift_herald_raw = team_info.find_element_by_class_name("rift-herald-kills")

    result = formatText(result_raw) == "VICTORY"
    gold = float(formatText(gold_raw).strip("k")) * 1000
    kills = float(formatText(kills_raw))
    towers = int(formatText(towers_raw))
    inhibs = int(formatText(inhibs_raw))
    barons = int(formatText(barons_raw))
    dragons = int(formatText(dragons_raw))
    rift_herald = int(formatText(rift_herald_raw))

    team_name = player_names[0].split(" ")[0]
    team = Team(team_name, result, gold, kills, towers, inhibs, barons, dragons, rift_herald)

    #Extract player names
    players = []
    for player in player_names:
        #removes teamname from name
        name = " ".join(player.split(" ")[1:]) 
        players.append(PlayerInfo(name))

    team.players = players

    return team 

def getPlayerStats(raw_html, blue_team, red_team, formatText = formatHTML):
    '''adds player stats to the team object'''
    def getChampName(element):
        return element.find_element_by_xpath(".//div/div/div").get_attribute("data-rg-id")

    #Add champion information to players
    champions = raw_html.find_element_by_class_name("grid-header-row")
    blue_champs = list(map(getChampName, champions.find_elements_by_class_name("team-100")))
    red_champs = list(map(getChampName, champions.find_elements_by_class_name("team-200")))

    for playerIndex in range(5):
        blue_team.players[playerIndex].addInformation("champion", blue_champs[playerIndex])
        red_team.players[playerIndex].addInformation("champion", red_champs[playerIndex])


    #Add stats to players
    rows = raw_html.find_elements_by_class_name("grid-row")
    for row in rows:
        stat_type = formatText(row.find_element_by_class_name("grid-label")).lower()
        blue_stats = list(map(formatText, row.find_elements_by_class_name("team-100")))
        red_stats = list(map(formatText, row.find_elements_by_class_name("team-200")))

        stat_type_values = stat_type.split(" ")

        for playerIndex in range(5):
            blue_player_stats = blue_stats[playerIndex]
            red_player_stats = red_stats[playerIndex]

            if stat_type == "kda":
                blue_player_stats = blue_player_stats.split("/")
                blue_team.players[playerIndex].addInformation("kills", blue_player_stats[0])
                blue_team.players[playerIndex].addInformation("deaths", blue_player_stats[1])
                blue_team.players[playerIndex].addInformation("assists", blue_player_stats[2])

                red_player_stats = red_player_stats.split("/")
                red_team.players[playerIndex].addInformation("kills", red_player_stats[0])
                red_team.players[playerIndex].addInformation("deaths", red_player_stats[1])
                red_team.players[playerIndex].addInformation("assists", red_player_stats[2])

            elif stat_type == "first blood":
                if blue_player_stats == "●":
                    blue_team.players[playerIndex].addInformation(stat_type, 1)
                else:
                    blue_team.players[playerIndex].addInformation(stat_type, 0)

                if red_player_stats == "●":
                    red_team.players[playerIndex].addInformation(stat_type, True)
                else:
                    red_team.players[playerIndex].addInformation(stat_type, False)

            elif "largest" in stat_type_values or "wards" in stat_type_values \
                    or "killed" in stat_type_values:
                if blue_player_stats == '-':
                    blue_player_stats = 0

                if red_player_stats == '-':
                    red_player_stats = 0
                blue_team.players[playerIndex].addInformation("".join(stat_type), blue_player_stats)
                red_team.players[playerIndex].addInformation("".join(stat_type), red_player_stats)

            else: 
                blue_player_stats = int(float(blue_player_stats.split("k")[0]) * 1000)
                red_player_stats = int(float(red_player_stats.split("k")[0]) * 1000)

                blue_team.players[playerIndex].addInformation(stat_type, blue_player_stats)
                red_team.players[playerIndex].addInformation(stat_type, red_player_stats)

