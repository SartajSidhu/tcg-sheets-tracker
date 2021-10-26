import challonge
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)
print("Welcome to my program!")
# Tell pychallonge about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
challonge.set_credentials("gabru22", "1efPkjbTMb6LotjvOjbplXKpDZlPHcp44bkBBJss")

#Tid = (input("Enter the challonge tournament ID: ")) #jfaaprm5
print("Please share the google sheet with the email: sartaj@tourney-329922.iam.gserviceaccount.com")
#filename = input("Enter the name of your google sheet: ")
filename = "tracker"
#sheetname = input("Enter the specific sheet name\nAn example would be 'sheet1' or 'sheet2': ")
sheetname = "hey"
sheet = client.open(filename).worksheet(sheetname)  # Open the spreadhseet
data = sheet.get_all_records()  # Get a list of all records

#pprint(data)

#row1 = sheet.row_values(1)  # Get a specific row
#proper = ['Decks','Wins','Losses','GP','%']

decks = sheet.col_values(1)  # Get a specific column
#cell = sheet.cell(1,2).value  # Get the value of a specific cell
#pprint(decks)
numOfDecks=(len(decks))

#insertRow = ["hello", 5, "red", "blue"]


#sheet.update_cell(2,2, "CHANGED")  # Update one cell

#numRows = sheet.row_count  # Get the number of rows in the sheet


Tid = "jfaaprm5"
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show(Tid)

# Tournaments, matches, and participants are all represented as normal Python dicts.
#print(tournament["id"]) # 3272
print(tournament["name"]) # My Awesome Tournament
#print(tournament["started_at"]) # None

# Retrieve the participants for a given tournament.
participants = challonge.participants.index(tournament["id"])
#pprint(participants)
print(len(participants)) # 4
numOfParticipants = len(participants) #size of tournament
players = [[],[],[],[]] # list of players:names,wins,losses

# create the list a 2d list for names wins and losses with all 0 values
for x in range(4):
	for j in range(numOfParticipants):
		players[x].append(0)

# add names of participants to first list of the list
for x in range(numOfParticipants):
	players[0][x]=(participants[x]["name"])

# Retrieve the participants for a given tournament.
matches = challonge.matches.index(tournament["id"])
#pprint(matches)
numOfMatches = len(matches)
#pprint(match2)
for x in range(numOfMatches): #for loop for each match
	
	#check if there is a draw for the current match
	if(matches[x]["scores_csv"]=="1-1" or matches[x]["scores_csv"]=="0-0"):
		draw1 = challonge.participants.show(tournament["id"],matches[x]["player1_id"])
		draw2 = challonge.participants.show(tournament["id"],matches[x]["player2_id"])
		for y in range(numOfParticipants): 
			if(players[0][y]==draw2["name"] or players[0][y]==draw1["name"] ):
				players[3][y]+=1
	else:
		#find the winner and loser of the current match
		winner = challonge.participants.show(tournament["id"],matches[x]["winner_id"]) 
		loser = challonge.participants.show(tournament["id"],matches[x]["loser_id"])	
		#loop through the player list
		for y in range(numOfParticipants):
			if(players[0][y]==winner["name"]): #find the winner in the list 
				players[1][y]+=1 #add a win
			elif(players[0][y]==loser["name"]):
				players[2][y]+=1
		

#pprint(players)
	
insheet = False 
for j in range(numOfParticipants):	
	inSheet = False
	for i in range(numOfDecks):
		if(decks[i].lower()==players[0][j].lower()):
			win = int(sheet.cell(i+1,2).value)
			loss = int(sheet.cell(i+1,3).value)
			draw = int(sheet.cell(i+1,4).value)

			sheet.update_cell(i+1,2,players[1][j]+win)
			sheet.update_cell(i+1,3,players[2][j]+loss)
			sheet.update_cell(i+1,4,players[3][j]+draw)
			inSheet = True
	if(inSheet == False):	
		sheet.append_row([players[0][j],players[1][j],players[2][j],players[3][j]])

print("Tournament results have been added to your sheet!")
#cell = sheet.cell(1,1).value
#print(cell)
#pprint(players)
#sheet.update_cell(2,2,players[1][1])


#print("\n")
#print(players)
#newrow = [players[0][1],players[1][1],players[2][1]]
#pprint(newrow)
#sheet.append_row(newrow)  # Insert the list as a row at index 4


#Start the tournament and retrieve the updated information to see the effects
# of the change.
#challonge.tournaments.start(tournament["id"])
#tournament = challonge.tournaments.show(tournament["id"])
#print(tournament["started_at"]) # 2011-07-31 16:16:02-04:00
