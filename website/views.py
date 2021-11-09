from flask import Blueprint, render_template, request, flash, redirect
import challonge
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from .tourney import sheetSetup, chalSetup, addResults

views = Blueprint('views', __name__)


#all vars needed for using tourney fucntions
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
sheetjson = "creds.json"
challongejson = "challonge.json"

@views.route('/', methods=['GET', 'POST'])
def home():
	data = request.form
	if request.method == 'POST':

		Tid = request.form.get('challongeID')
		filename = request.form.get('googlesheet')
		sheetname = request.form.get('sheetname')

		sheet = sheetSetup(sheetjson,scope,filename,sheetname)
		tournament = chalSetup(challongejson,Tid)
		addResults(sheet,tournament)
		if(len(Tid)>1 and len(filename)>1 and len(sheetname)>1):
			flash("The tournament results have been added to "+filename, category="success")
		else:
			flash("Your inputs are invalid",category="error")
		

	return render_template("home.html")

@views.route('/help')
def help():
	return render_template("help.html")

