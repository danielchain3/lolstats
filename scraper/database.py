import mysql.connector
from player import PlayerInfo
from team import Team

def connectToDatabase(file_name):
    DBinfo = []
    file = open(file_name, 'r')

    for line in file:
        DBinfo.append(line.rstrip("\n"))

    file.close()

    mydb = mysql.connector.connect(
            host=DBinfo[0],
            user=DBinfo[1],
            passwd=DBinfo[2],
            database=DBinfo[3]
            )

    return mydb

def addTeamInfo(blue_team, red_team):

connectToDatabase("DBInfo")
