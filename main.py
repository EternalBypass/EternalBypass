'''
EternalBypass, an network of methods to bypass web filtering.
Copyright (C) 2021 James Hoffman

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, please check the COPYING file
	or see <https://www.gnu.org/licenses/>.

You can contact me at jamesgene@icloud.com.
'''
print('Starting...')
from flask import Flask, render_template
import os
from datetime import datetime
import time
from threading import Thread
import shutil
import threading
import sys
dotenv_loaded=False
path=''
try:
	import pyautogui
except Exception: #TODO Fix pyautogui to work with X, or preferably better solution.
	pass
import subprocess
try: #If you have problems trying to load the dotenv, use the printed info to find the cwd and place the necessary files in there.
	print(str(os.system('pwd')))
	from dotenv import load_dotenv
	dot = open('./static/eternalBypass.env')
	dotr = dot.read()
	load_dotenv('./static/eternalBypass.env')
	path=str(os.getenv("FULL_PATH"))
	print('INFO - Path is ' + path)
	if path[-1] != '/':
		path = str(path + '/')
		print('INFO - Path has been corrected to ' + path)
	dotenv_loaded = True
except Exception as err:
	print('ERROR - Unable to load dotenv. Err:', str(err) + ' . Current working directory is ' + str(os.getcwd()))
	try:
		path = os.environ.get('FULL_PATH')
		print('INFO - Path is '+path)
		if path[-1] != '/':
			path = str(path + '/')
			print('INFO - Path has been corrected to '+path)
	except Exception:
		print('ERROR - Unable to load dotenv, or load full path of necessary files from system vars. Defaulting to current directory.')
		path = './'

#==========Editable==========
logFileOutPlain = False #When writing to the log file, write in plaintext.
allOutPlain = False #no colors
noSubprocess = False #Dont start the discord subproc, or any subproc.
#=========EOEditable=========
crappyprxyStatus = ''
doNotStartDownDaemon = False
logTestBool='False'
titaniumStatus=' Not yet ported.'
discPid=''
no_username = os.environ.get('USERNAME_EB')
no_password = os.environ.get('PASSWORD_EB')
def die():
	global path
	#global downDaemon
	global t
	global td
	global tc
	try:
		local_export = open(path + 'logs/locals.log', 'w')
		d2 = str(datetime.now())
		local_export.write(d2 + '\n' + str(locals()))
		global_export = open(path + 'logs/globals.log', 'w')
		local_export.write(d2 + '\n' + str(globals()))
		t.do_run = False
		td = open('tempF', 'w')
		td.close()
		time.sleep(3)
		os.system('rm -rf '+path+'temp.py '+path+'logs/tempScript.log tempF')
		tc.do_run = False
	except Exception as die_err:
		try:
			log("ERROR", ' - Failed to die gracefully. Reason: '+str(die_err))
		except Exception:
			print("ERROR", " - Failed to die gracefully, and could not log. Reason: "+str(die_err))
		exit()
	log("INFO", " - Died gracefully. For all time. Always.[all threads reset/killed] ("+str(datetime.now())+") \n")
	exit()


def log(level, message):
	global path
	try:
		global logTestBool
		global logFileOutPlain
		d1 = str(datetime.now())
		logFile = open(path+'logs/main.log', 'a')
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = __file__
		try:
			lineno = exc_tb.tb_lineno
		except Exception as linenoErr:
			#print('LOGGER: Using alternate method for lineno. Err: '+str(linenoErr))
			lineno=sys.exc_info()[-1].tb_lineno
		if level == 'error' or level == 'ERROR' or level == 'Error':

			LMsg = d1 + ' - ' + filename + ':' + '\033[31;1m' + level + '\033[0m' + '\033[0;1m' + message + '\033[0m' + ' on line ' + str(lineno) + '\n'
			if allOutPlain == False:
					print(LMsg, end="")

			else:
					LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
					print(LMsg, end="")
			if logFileOutPlain == True:
				LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'

			logFile.write(LMsg)
			logFile.close()
		else:
			if level == 'warning' or level == 'WARNING' or level == 'Warning' or level == 'warn' or level == 'WARN' or level == 'warn':
				LMsg = d1 + ' - ' + filename + ':' + '\033[33;1m' + level + '\033[0m' + '\033[0;1m' + message + '\033[0m\n'
				if allOutPlain == False:
					print(LMsg, end="")

				else:
					LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
					print(LMsg, end="")

				if logFileOutPlain == True:
					LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
				logFile.write(LMsg)
				logFile.close()
			else:
				if level == 'info' or level == 'INFO' or level == 'Info':
					if 'New session start' in message:
						LMsg = '\n\n\n'+d1 + ' - ' + filename + ':' + '\033[36;1m' + level + '\033[0m' + '\033[0;1m' + message + '\033[0m\n'
					else:
						LMsg = d1 + ' - ' + filename + ':' + '\033[36;1m' + level + '\033[0m' + '\033[0;1m' + message + '\033[0m\n'
					if allOutPlain == False:
						print(LMsg, end="")

					else:
						if 'New session start' in message:
							LMsg = '\n\n\n'+d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
							print(LMsg, end="")
						else:
							LMsg = '\n\n\n' + d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
					if logFileOutPlain == True:
						if 'New session start' in message:
							LMsg = '\n\n\n'+d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
						else:
							LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
					logFile.write(LMsg)
					logFile.close()
				else:
					if level == 'critical' or level == 'CRITICAL' or level == 'Critical' or level == 'catastrophe' or level == 'Catastrophe' or level == 'CATASTROPHE':
						if allOutPlain == False:
								print('\033[31;1m==========CATASTROPHE OCCURED===========\033[0m')
						else:
								print('==========CATASTROPHE OCCURED===========')
						if logFileOutPlain != True:
							logFile.write('\033[31;1m==========CATASTROPHE OCCURED===========\033[0m\n')
						else:
							logFile.write('==========CATASTROPHE OCCURED===========')
						LMsg = d1 + ' - ' + filename + ':' + '\033[31;1m' + level + '\033[0m' + '\033[0;1m' + message + '\033[0m' + ' on line ' + str(lineno) + '\n'
						if allOutPlain == False:
								print(LMsg, end="")
								print('\033[31;1m========================================\033[0m')
								print('')
						else:
								LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
								print(LMsg, end="")
								print('========================================')
						if logFileOutPlain == True:
							LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
						if logFileOutPlain != True:
							logFile.write(LMsg)
							logFile.write('\033[31;1m========================================\033[0m\n')
						else:
							logFile.write(LMsg)
							logFile.write('========================================\n')
						logFile.write(LMsg)
						logFile.close()
						if logTestBool != True:
							die()
					else:
						LMsg = d1+' - ' + filename +':'+level+' -   '+message+'\n'
						print(LMsg, end="")
						if logFileOutPlain == True:
							LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\n'
						logFile.write(LMsg)
						logFile.close()
	except Exception as logErr:
		global dotenv_loaded
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		lineno = exc_tb.tb_lineno
		path  = os.path.dirname(os.path.realpath(__file__))
		if dotenv_loaded == True:
			print('The logger failed! Exiting. Error: '+str(logErr)+' On line '+str(lineno)+'. Current working directory is '+path+' and the set path var is set to '+path+', and was loaded by the dotenv file.')
		else:
			print('The logger failed! Exiting. Error: ' + str(logErr) + ' On line ' + str(
				lineno) + '. Current working directory is ' + path + ' and the set path var is set to ' + path + ', and was loaded by the global system vars.')
		die()

def login(username, password):
	os.system('firefox -url https://www.noip.com/login?ref_url=console#!/dynamic-dns && xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11')
	time.sleep(10)
	for i in range(3):
		pyautogui.typewrite(['TAB'])
		time.sleep(.1)
	time.sleep(.1)
	pyautogui.typewrite(username)
	pyautogui.typewrite(['TAB'])
	pyautogui.typewrite(password)
	pyautogui.typewrite(['TAB'])
	pyautogui.typewrite(['ENTER'])
def newDomain(domain):
	global no_username
	global no_password
	login(no_username, no_password)
	pyautogui.moveTo(290, 568)
	pyautogui.click()
	pyautogui.typewrite(domain)
	pyautogui.moveTo(821, 571)
	pyautogui.click()
	pyautogui.moveTo(1004, 829)
	pyautogui.click()
	pyautogui.moveTo(1015, 470)
	pyautogui.click()
	pyautogui.moveTo(1299, 746)
	pyautogui.click()
	pyautogui.moveTo(282, 528)
	c = pyautogui.displayMousePosition()
	if '255, 255, 255' not in c:
		return ' - New domain was already registered. fakeroot/new_domain.py, non-fatal.'
		exit()
	pyautogui.moveTo(502, 720)
	pyautogui.click()
	time.sleep(1)
	pyautogui.moveTo(1375, 552)
	pyautogui.click()
	return ' - fakeroot/new_domain.py finished. Exiting :-)'

def check_ping(host):
	response = os.system("ping -c 1 " + host)
	if response == 0:
		return ' Online.'
	else:
		return ' Down.'

def downDetector():
	try:
		global crappyprxyStatus
		crappyprxyStatus = check_ping('https://crappy-prxy.hopto.org')
	except Exception as downDetectorError:
		log('ERROR', ' - downDetector was unable to run ping.')

def checkThreads():
	global t
	global noSubprocess
	global discPid
	global discProc
	try:
		tc = threading.currentThread()
		while getattr(tc, "do_run", True):
			time.sleep(2)
			try:

				KillSwitch=open('tempF', 'r')
				fd = KillSwitch.read()
				#print('found switch')
				discProc.kill()
				os.system('rm -rf tempF')


			except Exception as fdsa:
				#print('no switch: '+str(fdsa))
				pass
			if t.is_alive() != True:
				log('ERROR', ' - downDaemon died! Restarting.')
				log('INFO', ' - downDaemon starting thread...')
				t = Thread(target=downDetector_daemon, name="downDetectorDaemon")
				t.start()
				log('INFO', ' - downDaemon started thread.')
			if noSubprocess == False:
				try:
					
					os.kill(discPid, 0)
				except OSError:
					discErr = open(path+'logs/tempScript.log', 'r')
					discErrDat = discErr.read()
					log('ERROR', ' - discDaemon died! Restarting. Error: '+discErrDat)
	
					log('INFO', ' - discDaemon starting subproc...')

					discFile = open(path+'temp.py', 'w')
					discFile.write(disc)
					discFile.close()
					discProc = subprocess.Popen(['python3', path+'temp.py'])
	
					time.sleep(3)  # Wait at least 3 seconds to make sure its up. We have no way to talk to it, so...
					discPid = discProc.pid
					log('INFO', ' - discordMirror subproc started. PID: ' + str(discPid))


		log('INFO', 'Flag set to die, dying.')
	except Exception as checkThreadsErr:
		log('CATASTROPHE', ' - An fatal error occured in checkThreads. checkThreads must stay alive!!! Error: '+str(checkThreadsErr))

def downDetector_daemon():
	global t
	try:
		first = True
		t = threading.currentThread()
		while getattr(t, "do_run", True):
			if first != True:
				downDetector()
				time.sleep(120)
			else:
				downDetector()
				first = False
	except Exception as downDaemonErr:
		log('ERROR', ' - downDetector_daemon died with error: '+str(downDaemonErr)+' Will be restarted within 10 seconds.')
#Keep it all in one script. Ugly, but whatever.
disc = ''' 
"""
EternalBypass, an network of methods to bypass web filtering.
Copyright (C) 2021 James Hoffman

	This file is part of EternalBypass.
	EternalBypass is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, please check the COPYING file
	or see <https://www.gnu.org/licenses/>.

You can contact me at jamesgene@icloud.com.
"""
import sys
import time
from threading import Thread
import os
import datetime
from datetime import datetime
dotenv_loaded=False
allOutPlain=False
logFileOutPlain=False
path='./'
def die():
	try:
		tempErr = open(path + 'logs/tempScript.log', 'w')
		tempErr.write('Manual initiated kill.')
		tempErr.close()
	except Exception:
		tempErr = open('./logs/tempScript.log', 'w')
		tempErr.write('Manual initiated kill.')
		tempErr.close()
	print('Found tempF flag, killing self. pid will be reserved for less than 3 seconds.')

	os.system('kill -9 ' + str(os.getpid()))
	exit()
from dotenv import load_dotenv
try: #If you have problems trying to load the dotenv, use the printed info to find the cwd and place the necessary files in there.
	print(str(os.system('pwd')))
	from dotenv import load_dotenv
	dot = open('./static/eternalBypass.env')
	dotr = dot.read()
	load_dotenv('./static/eternalBypass.env')
	path=str(os.getenv("FULL_PATH"))
	TOKEN=os.getenv("DISCORD_TOKEN")
	print('INFO - Path is ' + path)
	if path[-1] != '/':
		path = str(path + '/')
		print('INFO - Path has been corrected to ' + path)
	dotenv_loaded = True
except Exception as err:
	print('ERROR - Unable to load dotenv. Err:', str(err) + ' . Current working directory is ' + str(os.getcwd()))
	try:
		path = './'
		TOKEN = os.environ.get('DISCORD_TOKEN')
		print('INFO - Path is '+path)
	except Exception as err:
		print('CATASTROPHE - Unable to load token from dotenv or enviroment!')
		die()
		
def log(level, message): #This function only exists because of the fact that this script will only get more and more complicated.
	global path
	try:
		global logTestBool
		global logFileOutPlain
		d1 = str(datetime.now())
		logFile = open(path+'logs/tempScript.log', 'a')
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = __file__
		try:
			lineno = exc_tb.tb_lineno
		except Exception as linenoErr:
			#print('LOGGER: Using alternate method for lineno. Err: '+str(linenoErr))
			lineno=sys.exc_info()[-1].tb_lineno
		if level == 'error' or level == 'ERROR' or level == 'Error':

			LMsg = d1 + ' - ' + filename + ':' + '\\033[31;1m' + level + '\\033[0m' + '\\033[0;1m' + message + '\\033[0m' + ' on line ' + str(lineno) + '\\n'
			if allOutPlain == False:
					print(LMsg, end="")

			else:
					LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
					print(LMsg, end="")
			if logFileOutPlain == True:
				LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'

			logFile.write(LMsg)
			logFile.close()
		else:
			if level == 'warning' or level == 'WARNING' or level == 'Warning' or level == 'warn' or level == 'WARN' or level == 'warn':
				LMsg = d1 + ' - ' + filename + ':' + '\\033[33;1m' + level + '\\033[0m' + '\\033[0;1m' + message + '\\033[0m\\n'
				if allOutPlain == False:
					print(LMsg, end="")

				else:
					LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
					print(LMsg, end="")

				if logFileOutPlain == True:
					LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
				logFile.write(LMsg)
				logFile.close()
			else:
				if level == 'info' or level == 'INFO' or level == 'Info':
					if 'New session start' in message:
						LMsg = '\\n\\n\\n'+d1 + ' - ' + filename + ':' + '\\033[36;1m' + level + '\\033[0m' + '\\033[0;1m' + message + '\\033[0m\\n'
					else:
						LMsg = d1 + ' - ' + filename + ':' + '\\033[36;1m' + level + '\\033[0m' + '\\033[0;1m' + message + '\\033[0m\\n'
					if allOutPlain == False:
						print(LMsg, end="")

					else:
						if 'New session start' in message:
							LMsg = '\\n\\n\\n'+d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
							print(LMsg, end="")
						else:
							LMsg = '\\n\\n\\n' + d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
					if logFileOutPlain == True:
						if 'New session start' in message:
							LMsg = '\\n\\n\\n'+d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
						else:
							LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
					logFile.write(LMsg)
					logFile.close()
				else:
					if level == 'critical' or level == 'CRITICAL' or level == 'Critical' or level == 'catastrophe' or level == 'Catastrophe' or level == 'CATASTROPHE':
						if allOutPlain == False:
								print('\\033[31;1m==========CATASTROPHE OCCURED===========\\033[0m')
						else:
								print('==========CATASTROPHE OCCURED===========')
						if logFileOutPlain != True:
							logFile.write('\\033[31;1m==========CATASTROPHE OCCURED===========\\033[0m\\n')
						else:
							logFile.write('==========CATASTROPHE OCCURED===========')
						LMsg = d1 + ' - ' + filename + ':' + '\\033[31;1m' + level + '\\033[0m' + '\\033[0;1m' + message + '\\033[0m' + ' on line ' + str(lineno) + '\\n'
						if allOutPlain == False:
								print(LMsg, end="")
								print('\\033[31;1m========================================\\033[0m')
								print('')
						else:
								LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
								print(LMsg, end="")
								print('========================================')
						if logFileOutPlain == True:
							LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
						if logFileOutPlain != True:
							logFile.write(LMsg)
							logFile.write('\\033[31;1m========================================\\033[0m\\n')
						else:
							logFile.write(LMsg)
							logFile.write('========================================\\n')
						logFile.write(LMsg)
						logFile.close()
						if logTestBool != True:
							die()
					else:
						LMsg = d1+' - ' + filename +':'+level+' -   '+message+'\\n'
						print(LMsg, end="")
						if logFileOutPlain == True:
							LMsg = d1 + ' - ' + filename + ':' + level + message + ' on line ' + str(lineno) + '\\n'
						logFile.write(LMsg)
						logFile.close()
	except Exception as logErr:
		global dotenv_loaded
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		lineno = exc_tb.tb_lineno
		path  = os.path.dirname(os.path.realpath(__file__))
		if dotenv_loaded == True:
			print('The logger failed! Exiting. Error: '+str(logErr)+' On line '+str(lineno)+'. Current working directory is '+path+' and the set path var is set to '+path+', and was loaded by the dotenv file.')
		else:
			print('The logger failed! Exiting. Error: ' + str(logErr) + ' On line ' + str(
				lineno) + '. Current working directory is ' + path + ' and the set path var is set to ' + path + ', and was loaded by the global system vars.')
		die()
		
try:
	log('INFO', ' - New session start at '+str(datetime.now()))
	from discord.ext import commands

	client = commands.Bot(command_prefix='$')
	import discord
	log('INFO', 'Cleaning flag')
	#client = discord.Client()
	os.system('rm -rf tempF')


	@client.event
	async def on_ready():
		print('Subproccess logged in as {0.user}'.format(client))


	def killCheck(pid):
		while True:
			if os.path.exists('tempF') == True:
				log('INFO', ' - Found tempF flag, killing self. PID will be reserved for less than 3 seconds.')
				tempErr = open(path+'logs/tempScript.log', 'w')
				tempErr.write('Manual initiated kill.')
				tempErr.close()
				os.system('kill -9 ' + str(pid))
				exit()

			time.sleep(.3)
	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		if message.content.startswith('$status'):
			await message.channel.send('Alive and well.')
			
		if message.content.startswith('$kill'):
			await message.channel.send('Goodbye, Ill be back soon.')
			dieFile2 = open('tempF', 'w')
			dieFile2.close()
			
			
		channel = client.get_channel(866063852382453791)
		messages = await channel.history().flatten()
		messages.reverse()
		discMessages=open('./data/discord/channelMessagesProxy', 'w')
		for i, message in enumerate(messages):
			messageCon = message.content
			discMessages.write(str(message.author)+': '+messageCon+'\\n')
			
		channel = client.get_channel(864258119881064462)
		messages = await channel.history().flatten()
		messages.reverse()
		discMessages=open('./data/discord/channelMessagesGeneral', 'w')
		for i, message in enumerate(messages):
			messageCon = message.content
			discMessages.write(str(message.author)+': '+messageCon+'\\n')
			
		channel = client.get_channel(866898966720806983)
		messages = await channel.history().flatten()
		messages.reverse()
		discMessages=open('./data/discord/channelMessagesTools', 'w')
		for i, message in enumerate(messages):
			messageCon = message.content
			discMessages.write(str(message.author)+': '+messageCon+'\\n')
			
	# log("INFO", "discordMirror starting loops.")
	currentPid = os.getpid()
	killDaemon = Thread(target=killCheck, args=(currentPid,))
	killDaemon.daemon = True
	killDaemon.start()
	#TOKEN = os.environ.get('DISC_TOKEN')
	client.run(TOKEN)
except Exception as discErr:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	try:
		filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	except Exception:
		filename = __file__
	try:
		lineno = exc_tb.tb_lineno
	except Exception as linenoErr:
		# print('LOGGER: Using alternate method for lineno. Err: '+str(linenoErr))
		lineno = sys.exc_info()[-1].tb_lineno
	log('CATASTROPHE', 'An error occured. Error: ' + str(discErr) + ' in file ' + str(filename) + ' on line ' + str(lineno))
	exit()
'''

def logTest():
	logTestBool='True'
	log('INFO', 'Initial log test. INFO')
	log('WARNING', 'Warning')
	log('ERROR', 'Error')
	log('CRITICAL', 'Catastrophe')
	logTestBool()

def start():
	global discPid
	global discProc
	global disc
	global t
	global tc
	global noSubprocess
	global td
	try: #Exception handling is in this scope so you can get an actual line number, instead of the number of the function executing.
		log('INFO', ' - New session start at '+str(datetime.now()))
		log('INFO', ' - Start executed.')
		try:
			downDetector()
			doNotStartDownDaemon = False
		except Exception as down_exception:
			log('ERROR', ' - downDetector() failed with error: '+str(down_exception))
			down_exception=''
			doNotStartDownDaemon = True

		if doNotStartDownDaemon == False:
			try:
				log('INFO', ' - downDaemon starting thread...')
				t = Thread(target=downDetector_daemon, name='downDaemon')
				t.daemon = True
				t.start()
				log('INFO', ' - downDaemon started thread.')
			except Exception as downDaemonError:
				log('ERROR', ' - downDaemon thread start failed with error: '+str(downDaemonError))
				downDaemonError=''
		else:
			log('ERROR', ' - Flag doNotStartDownDaemon was set to True, cannot start daemon.')

		try:
			if noSubprocess == False:
				log('INFO', ' - discordMirror starting subproc...')
				discFile = open(path+'temp.py', 'w')
				discFile.write(disc)
				discFile.close()
				discProc = subprocess.Popen(['python3', path+'temp.py'])

			#time.sleep(3)  # Wait at least 3 seconds to make sure its up. We have no way to talk to it, so...
				discPid = discProc.pid
				log('INFO', ' - discordMirror subproc started. PID: '+str(discPid))
			else:
				pass
		except Exception as downDiscError:
			log('ERROR', ' - discordMirror thread start failed with error: ' + str(downDiscError))
			downDiscError = ''

		try:
			log('INFO', ' - checkThreads starting thread...')
			tc = Thread(target=checkThreads, name='checkThreadDaemon')
			tc.daemon = True
			tc.start()
			log('INFO', ' - checkThreads thread started.')
		except Exception as checkThreadsError:
			log('ERROR', ' - checkThreads thread start failed with error: ' + str(checkThreads))
			checkThreadsError = ''
		#print('\033[36;1m===============Initial logging test===============\033[0m\n')
		#logTest()
		#print('\033[36;1m===============Logging test finished==============\033[0m\n')
		try:
			os.mkdir('/tmp/foo')
			shutil.rmtree('/tmp/foo')
		except PermissionError:
			log('WARNING', ' - No root.')
	except Exception as StartErr:
		log('CATASTROPHE', ' - Start failed with uncaught error: ' + str(StartErr))
		die()

app = Flask(__name__)

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/loki")
def main_loki():
	return render_template("index_loki.html")

@app.route("/loki_test")
def test_loki():
	return render_template("test_loki.html")

@app.route("/tools")
def tools():
	return render_template("tools.html", crappyprxyStatus=crappyprxyStatus, titaniumStatus=titaniumStatus)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/tutorials")
def tutorials():
	return render_template("tutorials.html")

@app.route("/auu")
def auu():
	return render_template("auu.html")

@app.route("/tutorials/novnc")
def tutorials_novnc():
	return render_template("novnc.html")

@app.route("/tools/disc-mirror")#TODO: Add an tools discord mirror, offical list.
def discMirrorFlask():
	messageFile = open('./data/discord/channelMessagesProxy', 'r')
	messagesHistory = messageFile.read()
	return render_template("discordMirror.html", messagesHistory=messagesHistory)

@app.route("/tools/general")
def general():
	messageFile = open('./data/discord/channelMessagesGeneral', 'r')
	messagesHistoryGeneral = messageFile.read()
	return render_template("general.html", messagesHistoryGeneral=messagesHistoryGeneral)

@app.route("/tools/tool-mirror")
def toolsRoute():
	messageFile = open('./data/discord/channelMessagesTools', 'r')
	messagesHistoryTools = messageFile.read()
	return render_template("toolsMirror.html", messagesHistoryTools=messagesHistoryTools)

@app.route("/log")
def logs():
	global path
	logMirrorFile = open(path+'logs/main.log', 'r').replace(os.system('pwd'), "")
	logMirror = logMirrorFile.read().replace('\033[31;1m', '').replace('\033[36;1m', '').replace('\033[33;1m', '').replace('\033[0m', '').replace('\033[0;1m0', '')
	return render_template("logFile.html", logMirror=logMirror)


start()
log("INFO", " - Start finished with no fatal errors. Starting up flask server")

if __name__ == "__main__":
	try:
		try:
			app.run(host='0.0.0.0')
		except KeyboardInterrupt:
			die()
	except Exception as flask_error:
		log('CATASTROPHE', ' - An flask error occured. Error: '+str(flask_error))
