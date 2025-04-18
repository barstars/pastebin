'''
config.txt
username = username
password = password
server_ip = server_ip
database_name = database_name
'''

with open("config.txt", "r") as file:
	lines = file.readlines()
	CONFIG = {}
	for el in lines:
		el = (el.split("#"))[0]
		el = el.strip()
		if (el == ""):
			continue
		var, value = el.split(" = ")
		CONFIG[var] = value