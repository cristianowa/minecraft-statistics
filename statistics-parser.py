#!/usr/bin/python
import re
import traceback
from commands import getoutput as cmd_
from datetime import timedelta
from display import stats as stats_display
from display import achievements as achi_display
def cmd(s):
	r = cmd_(s)
#	print r
	return r
import sys
import json
display = {}
display["stats"] = stats_display
display["achievements"] = achi_display


def minutesToTime(minutes):
	try:
		min = int(minutes)
	except:
		return "error"
	return  timedelta(seconds=min).__str__()
	

def import_player_info(world_dir,player_name):
	try:
	
		json_data=open(world_dir + "/stats/" + player_name + ".json")
		player_info = json.load(json_data)
		json_data.close()
		stats = {}
		achievements = {}
		for i in player_info:
			indexes = i.split(".")
			if indexes[0] == "stat":
				if(len(indexes) == 2):
					stats[indexes[1]] = player_info[i]
				else: # subitem
					stats[indexes[1] + indexes[2]] = player_info[i]
			elif indexes[0] == "achievement":
				achievements[indexes[1]] = player_info[i]
			else:
				print("unsed item : " + i )
		info = {}
		info["stats"] = stats
		info["achievements"] = achievements
		info["name"] = player_name
		return info
	except:
		traceback.print_exc(file=sys.stdout)
		print "error !!! "
		sys.exit(-1)
#this only is used to create the auxiliary names file
def create_display(info,key):
	display = {}
	for i in info:
		for j in i[key]:
			if j not in display.keys() :
				display[j] = raw_input("Name for \"" + j + "\":\n")
	print display
	return display

def CmToDistance(value):
	st = ""

	return st

def join(info,key):
	full = {}
	for i in info:
		for j in i[key]:
			try:
				if j not in full.keys():
					full[j] = {}
				if "vector" not in full[j].keys():
					full[j]["vector"] = [None]*len(info)
				if j == "playOneMinute" :
					full[j]["vector"][i["player_id"]] = minutesToTime(i[key][j])
				elif j == "exploreAllBiomes":#TODO: print this better
					 full[j]["vector"][i["player_id"]] = i[key][j]
				elif j[len(j) - 2:len(j)] == "Cm":
					full[j]["vector"][i["player_id"]] = CmToDistance(i[key][j])
				else:
					full[j]["vector"][i["player_id"]] = i[key][j]
				full[j]["name"] = display[key][j]
			except:
				print "error in " + j
				del full[j]
			
		
	return full

class maxx:
	def __init__(self):
		self.max_size =0
		return
	def max(self,b):
		try:
			tmp = max(len(b),self.max_size)
		except:
			return
		self.max_size = tmp
		return
	def value(self):
		return self.max_size

def print_table(table,size):
	for i in range(len(table)):
		for j in range(len(table[i])):
			try:
				print str(table[i][j]).rjust(size) + " | ",
			except:
				print "".rjust(size) + " | ",
		print
	return	
def html_table(table):
	html = "<table border=\"1\" style=\"width:1500px\">"
	for i in range(len(table)):
		html += "<tr>\n"
		for j in range(len(table[i])):
			html += "\t<td>"
			try:
				html += str(table[i][j])
			except:
				html+= ""
			html += "</td>\n"
		html += "</tr>\n"
	html+= "</table>"
	return html
def display_info(info,players):
	cols = len(players) + 1
	table = []
	table.append([""]*cols)
	m = maxx()
	for i in range(0,len(players)):
		table[0][i+1] = players[i]
		m.max( players[i])
	for i in info:
		if info[i]["name"] != "":
			table.append([""]*cols)
			table[len(table)-1][0] = info[i]["name"]
			for j in range(0,len(info[i]["vector"])):
				table[len(table)-1][j+1] = info[i]["vector"][j]
				m.max(info[i]["vector"][j])
				if table[len(table)-1][j+1] == None:
					table[len(table)-1][j+1] = ""
	print " ---- " + str(m.value())
	table.sort()
	print_table(table,20)
	return table

def generate_html(st,ac,filename):
	f = open(filename,"w")
	f.write("<!DOCTYPE html>\n")
	f.write("<html>\n")
	f.write("<body>\n")
	f.write("\n")
	f.write("<h1>Minecraft Statistics</h1><p><p>\n")
	f.write("<h2>Statistics </h2>\n")
	f.write(html_table(st))
	f.write("<h2>Achievements </h2>\n")
	f.write(html_table(ac))
	f.write("</body>\n")
	f.write("</html>\n")
	f.close()
def parse_all(world_dir):
	lst = cmd("ls " + world_dir + "/stats/").replace(".json","").splitlines()
	info = []
	
	for player_id in range(0,len(lst)):
		info.append(import_player_info(world_dir,lst[player_id]))
		info[len(info)-1]["player_id"] = player_id
		info[len(info)-1]["player_id"] = player_id
	stats =  join(info,"stats")
	achi = join(info,"achievements")
	st = display_info(stats,lst)
	ac = display_info(achi,lst)
	generate_html(st,ac,"index.html")
if __name__ == "__main__" :
	parse_all(sys.argv[1])
	
