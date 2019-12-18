from bs4 import BeautifulSoup
import requests
import sys

#Check that user enters at least 1 argument
arguments = len(sys.argv) - 1
if (arguments < 1):
    print("Must enter a month number!")
    sys.exit()


#Check that the arg is an integer between 1-12. If so, store that number in queryMonth
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

outputText = ""
caution = ""

for team in teams:
    #Get html of team roster page
    teamName = team[0]
    teamHtml = requests.get(team[1]).text
    soup = BeautifulSoup(teamHtml, "lxml")
    print("Getting " + teamName + " players...")

    mlsUrl = "https://www.mlssoccer.com"
    teamTable = soup.find("tbody")

    #Collect an array of player url (exclude non- active roster players)
    playerUrlList = []
    for tr in teamTable.find_all("tr"):
        if tr.find("a") == None:
            break
        playerUrl = mlsUrl + tr.find("a").get("href")
        playerUrlList.append(playerUrl)

    #Query player info per player link (active roster only) and add it to players list
    players = []
    for url in playerUrlList:
        #Get the player's html page
        playerHtml = requests.get(url).text
        soup = BeautifulSoup(playerHtml, "lxml")

        #Find div containing player info
        playerContainer = soup.find("div", "player_container")

        #If the playerContainer is not present, add it to caution string and skip this player link
        if playerContainer == None:
            caution += url + "\n"
            continue

        #Find the Photo, Name, D.O.B, Club Name, and Position
        photoUrl = playerContainer.find("img", "headshot_image")["src"]
        name = playerContainer.find("img", "headshot_image")["alt"]
        ageContainer = playerContainer.find("div", "age").text
        birthday = ageContainer.split("\n")[1].split(" ")[1]
        birthMonth = birthday[birthday.find("(") + 1 : birthday.find(")")].split("/")[0]
        position = playerContainer.find("span", "position").text

        #If the players birth month is not the same as queryMonth, don't add the player
        if (int(birthMonth)) != queryMonth:
            continue

        #Store the player information in a hashmap
        player = {
            "Photo": photoUrl,
            "Name": name,
            "DOB": birthday,
            "Club": teamName,
            "Position": position
        }

        players.append(player)

    # Add the players to the ouptut text
    outputText += "---------------------\n" + teamName + "\n\n"
    for player in players:
        outputText += "Photo: " + player["Photo"] + "\n" + \
        "Name: " +  player["Name"] + "\n" + \
        "D.O.B: " + player["DOB"] + "\n" + \
        "Club: " + player["Club"] + "\n" + \
        "Position: " + player["Position"] + "\n\n"

    print("Done\n\n")


warningText = "\n-----------------------------------\n" + "Double Check these brocken player sites for birthdays:\n" + caution

if caution != "":
    print(warningText)
    outputText += warningText

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
fileName = months[queryMonth - 1] + "_MLS.txt"
birthdayFile = open(fileName, "w")
birthdayFile.write(outputText.encode('utf8'))
birthdayFile.close

print("Your file is in: " + fileName)


