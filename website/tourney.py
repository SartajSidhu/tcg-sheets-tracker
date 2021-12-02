import challonge
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint



def sheetSetup(jsonName,scope,filename,sheetname):
	creds=ServiceAccountCredentials.from_json_keyfile_name(jsonName, scope)
	client = gspread.authorize(creds)
	sheet = client.open(filename).worksheet(sheetname)
	#data = sheet.get_all_records()
	return sheet

def chalSetup(jsonName,Tid):
	creds = open(jsonName)
	data = json.load(creds)
	challonge.set_credentials(data["user"],data["key"])
	tournament = challonge.tournaments.show(Tid)
	return tournament


def addResults(sheet,tourney):
	decks = sheet.col_values(1) #get first column for names of decks 
	numOfDecks = len(decks)

	participants = challonge.participants.index(tourney["id"]) #holds all data of all participants within the challonge tournament
	numOfParticipants = len(participants) #number of people in tournament 
	matches = challonge.matches.index(tourney["id"]) #holds all matches data
	numOfMatches = len(matches) #number of matches in the tournament

	players = [[],[],[],[]] #player array to hold Names,Wins,Losses, and ties of each participant

	# create the list a 2d list for names wins losses and ties with all 0 values
	for x in range(len(players)):
		for j in range(numOfParticipants):
			players[x].append(0)

	# add names of participants to first list of the list
	for x in range(numOfParticipants):
		players[0][x]=(participants[x]["name"])

	#for loop for each match to find results and add to players 		
	for x in range(numOfMatches): 
	# get player 1 and player 2
		p1 = challonge.participants.show(tourney["id"],matches[x]["player1_id"])
		p2 = challonge.participants.show(tourney["id"],matches[x]["player2_id"])
	#check if there is a draw for the current match
		if(matches[x]["scores_csv"]=="1-1" or matches[x]["scores_csv"]=="0-0"):
			tieVal = int(matches[x]["scores_csv"][0]) # gets first value of scores, since it is a draw both polayers will get the win and the tie
			#find the players who had a draw and add to their tie value
			for y in range(numOfParticipants): 
				if(players[0][y]==p2["name"] or players[0][y]==p1["name"] ):
					players[3][y]+=1 #adding tie to each player
					players[1][y]+=tieVal #adding each wins to player
					players[2][y]+=tieVal #adding each losses to player

		else:
			#find the winner and loser of the current match
			winner = challonge.participants.show(tourney["id"],matches[x]["winner_id"]) 
			loser = challonge.participants.show(tourney["id"],matches[x]["loser_id"])
			
			#variables to hold amount of wins by each player
			winVal = int(matches[x]["scores_csv"][0])
			lossVal = int(matches[x]["scores_csv"][2])
			temp = 0 #to switch vals if incorrect
			if(winVal<lossVal): #makes wins the greater value since (winner should have more wins)
				temp = winVal
				winVal = lossVal
				lossVal = temp
				
			#loop through the player list
			for y in range(numOfParticipants):
				if(players[0][y]==winner["name"]): #find the winner 
					players[1][y]+= winVal #add games won in match for winner
					players[2][y]+= lossVal #add games lost in match for winner
				elif(players[0][y]==loser["name"]): #find the loser 
					players[1][y]+=lossVal #add games won in match for loser
					players[2][y]+=winVal #add games lost in match for loser

	#now all wins losses and ties have been added to the player array
	#now to add them to the googlesheet
	insheet = False #flag to check if the current players name or deck is already within the sheet
	for j in range(numOfParticipants):	
		inSheet = False
		for i in range(numOfDecks): #nested loop to check each player deck name with each sheet deck name 
			if(decks[i].lower()==players[0][j].lower()): #check if equal
				
				#retrieve current values inside sheet 
				win = int(sheet.cell(i+1,2).value)
				loss = int(sheet.cell(i+1,3).value)
				draw = int(sheet.cell(i+1,4).value)

				#update sheet adding on to the old values
				sheet.update_cell(i+1,2,players[1][j]+win)
				sheet.update_cell(i+1,3,players[2][j]+loss)
				sheet.update_cell(i+1,4,players[3][j]+draw)
				
				inSheet = True #set flag to true since it was in the sheet
		
		if(inSheet == False):	#if it wasnt in the sheet 
			sheet.append_row([players[0][j],players[1][j],players[2][j],players[3][j]]) #Create a new row for the new deck with all data


