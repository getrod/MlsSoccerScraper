from bs4 import BeautifulSoup
import requests
import sys

#Check that user enters at least 1 argument
arguments = len(sys.argv) - 1
if (arguments < 1):
    print("Must enter a month number!")
    sys.exit()


#Check that the arg is an integer between 1-12
try:
    queryMonth = int(sys.argv[1])
except ValueError:
    print("You must enter a number, not a letter!")
    sys.exit()

if queryMonth not in range(1,13):
    print(sys.argv[1] + " is not a month")
    print("Please enter a month number! [1 - 12]")
    sys.exit()


#Make an array of team names and team urls in the order of the website
teams = [
    ["Atlanta United FC", "https://www.mlssoccer.com/rosters/2019/atlanta-united"],
    ["Chicago Fire", "https://www.mlssoccer.com/rosters/2019/chicago-fire"],
    ["FC Cincinnati", "https://www.mlssoccer.com/rosters/2019/fc-cincinnati"],
    ["Colorado Rapids", "https://www.mlssoccer.com/rosters/2019/colorado-rapids"],   
    ["Columbus Crew SC", "https://www.mlssoccer.com/rosters/2019/columbus-crew-sc"],
    ["FC Dallas", "https://www.mlssoccer.com/rosters/2019/fc-dallas"],
    ["D.C. United", "https://www.mlssoccer.com/rosters/2019/dc-united"],
    ["Houston Dynamo", "https://www.mlssoccer.com/rosters/2019/houston-dynamo"],
    ["Los Angeles Football Club", "https://www.mlssoccer.com/rosters/2019/lafc"],
    ["LA Galaxy", "https://www.mlssoccer.com/rosters/2019/la-galaxy"],
    ["Minnesota United FC", "https://www.mlssoccer.com/rosters/2019/minnesota-united"],
    ["Montreal Impact", "https://www.mlssoccer.com/rosters/2019/montreal-impact"],
    ["New England Revolution", "https://www.mlssoccer.com/rosters/2019/new-england-revolution"],
    ["New York City FC", "https://www.mlssoccer.com/rosters/2019/new-york-city-fc"],
    ["New York Red Bulls", "https://www.mlssoccer.com/rosters/2019/new-york-red-bulls"],
    ["Orlando City SC", "https://www.mlssoccer.com/rosters/2019/orlando-city"],
    ["Philadelphia Union", "https://www.mlssoccer.com/rosters/2019/philadelphia-union"],
    ["Portland Timbers", "https://www.mlssoccer.com/rosters/2019/portland-timbers"],
    ["Real Salt Lake", "https://www.mlssoccer.com/rosters/2019/real-salt-lake"],
    ["San Jose Earthquakes", "https://www.mlssoccer.com/rosters/2019/san-jose-earthquakes"],
    ["Seattle Sounders FC", "https://www.mlssoccer.com/rosters/2019/seattle-sounders"],
    ["Sporting Kansas City", "https://www.mlssoccer.com/rosters/2019/sporting-kansas-city"],
    ["Toronto FC", "https://www.mlssoccer.com/rosters/2019/toronto-fc"],
    ["Vancouver Whitecaps FC", "https://www.mlssoccer.com/rosters/2019/vancouver-whitecaps"],
]

#TODO: Refactor this seciton to loop through all team links 
#Get the html document of one team page url (teams[0][1]). And print it to the console.
teamName = teams[0][0]
teamHtml = requests.get(teams[0][1]).text
soup = BeautifulSoup(teamHtml, "html.parser")

#For that team html document, find the href attribute for the first player
#TODO: for each "tr in tbody" when refactoring to all team players
mlsUrl = "https://www.mlssoccer.com"
teamTable = soup.find("tbody")
playerUrl = mlsUrl + teamTable.tr.td.a.get("href")
playerHtml = requests.get(playerUrl).text
soup = BeautifulSoup(playerHtml, "html.parser")

#Find div containing player info
playerContainer = soup.find("div", "player_container")

#Find the Photo, Name, D.O.B, Club Name, and Position
photoUrl = playerContainer.div.div.img["src"]
name = playerContainer.div.div.img["alt"]
ageContainer = playerContainer.find("div", "age").text
birthday = ageContainer.split("\n")[1].split(" ")[1]
birthMonth = birthday[birthday.find("(") + 1 : birthday.find(")")].split("/")[0]
position = playerContainer.find("span", "position").text

#Store the player information in a hashmap
player = {
    "Photo": str(photoUrl),
    "Name": str(name),
    "DOB": str(birthday),
    "Club": str(teamName),
    "Position": str(position)
}

print(player)