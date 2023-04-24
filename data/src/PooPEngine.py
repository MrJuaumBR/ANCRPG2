import pygame as pyg
from subprocess import run
from math import sqrt
from pygame.locals import *
import sqlite3 as sql
import json
from datetime import datetime as date
from pyperclip import copy, paste
import requests

pyg.init()

class pygame_rework():
	def __init__(self,scrSize = (800,600),title="By Poop Engine"):
		self.window: pyg.display = None
		self.scrSize: tuple = scrSize
		self.hScrSize: tuple = (scrSize[0]/2,scrSize[1]/2)
		self.window_title: str = title

		self.fonts = []
		self.textboxes = []
		self.volume = 100
		pyg.init()
		# DataBase
		self.database = None
		self.cursor = None
		pyg.init()

		self.installed_ver = 1.2
		self.__ver__:dict = json.loads(requests.get("https://raw.githubusercontent.com/MrJuaumBR/ReleaseRPGTest/main/version.json").text)
		if self.__ver__['engine_version'] > self.installed_ver:
			print("PooPEngine not updated!")
			quit()
		elif self.__ver__['engine_version'] <= self.installed_ver:
			print('PooPEngine updated!')

		# WINDOW SCALE
		self.WScaleRatio = self.scrSize[0]/self.scrSize[1]
		self.HScaleRatio = self.scrSize[1]/self.scrSize[0]
		self.pixels = self.scrSize[0] * self.scrSize[1]

		#FPS Control
		self.FPS_CONTROL_REPEAT = 0
	
	def create_window(self): # Create the starter window of pygame
		self.window = pyg.display.set_mode(self.scrSize,pyg.DOUBLEBUF)
		pyg.display.set_caption(self.window_title)
	
	def GetScalePos(self,Position):
		width,height = pyg.display.get_surface().get_size()
		return (width * Position[0],height * Position[1])

	def events(self): #Get all events of pygame
		r_: list = pyg.event.get()
		return r_ # Return a List

	def fill(self,color= (255,255,255)): #Fill the screen
		self.window.fill(color)

	def FPS(self,fps=60): # Set a clock to FPS
		pyg.time.Clock().tick(fps)
		return pyg.time.Clock().get_fps()

	def create_font(self,font,size): # Create a font and insert it in the fonts list
		"""Create an font(can be referenced with number see: fonts list)"""
		font = pyg.font.SysFont(font,size,True,False)
		self.fonts.append(font)
		id = len(self.fonts)-1
		return (font,id)

	def button(self,XY,colors,text,font,rep=False): # Create a button with a interation!
		"""Create an button"""
		if type(font) == int:
			font = self.fonts[font]
		text = font.render(text,True,colors[0],colors[1])
		textobj = text.get_rect()
		textobj.center= XY
		obj = self.window.blit(text,textobj)
		if obj.collidepoint(pyg.mouse.get_pos()):
			if pyg.mouse.get_pressed(3)[0]:
				if rep:
					self.delay(200)
					return True
				else:
					return True
			else:
				return False
		else:
			return False

	def rect(self,XY,WH,color=(0,0,0),alpha=255): # Create a rectangle
		s = pyg.Surface(WH)
		s.set_alpha(alpha)
		s.fill(color)
		obj = self.window.blit(s, (XY[0]-WH[0]/2,XY[1]-WH[1]/2))
		return obj

	def rect2(self,XY,WH,color=(0,0,0),alpha=255): # Create a rectangle2
		s = pyg.Surface(WH)
		s.set_alpha(alpha)
		s.fill(color)
		s.get_rect().center = XY
		obj = self.window.blit(s,(s.get_rect().x,s.get_rect().y))
		return obj

	def rect3(self,surface,XY,WH,color=(0,0,0),alpha=255): # Create a rectangle2
		s = pyg.Surface(WH)
		s.set_alpha(alpha)
		s.fill(color)
		s.get_rect().topleft = XY
		obj = surface.blit(s,(s.get_rect().x,s.get_rect().y))
		return obj

	class spritesheet(object): # Class to spritesheet
		def __init__(self,filename):
			pyg.init()
			try:
				self.sheet = pyg.image.load(filename).convert()
			except:
				print(f'Unable to load spritesheet')
		def _image_at(self,rectangle,colorkey=None):
			rect = pyg.Rect(rectangle)
			image = pyg.Surface(rect.size).convert()
			image.blit(self.sheet,(0,0), rect)
			if colorkey is not None:
				if colorkey == -1:
					colorkey = image.get_at((0,0))
				image.set_colorkey(colorkey,pyg.RLEACCEL)

			return image

		def _images_at(self,rects,colorkey = None):
			return [self._image_at(rect,colorkey) for rect in rects]

		def load_strip(self, rect, image_count, colorkey=None):
			tups = [(rect[0]+rect[2]*x, rect[1],rect[2],rect[3])for x in range(image_count)]
			return self._images_at(tups,colorkey)

	def image_at(self,file,rectangle,colorkey=None): # Put an image from sprite sheet
		"""Get an image in the rectangle position of an file"""
		s = self.spritesheet(file)
		ss = s._image_at(rectangle,colorkey)
		return ss

	def key_pressed(self,event,key): #Check if a key pressed
		if event.type == pyg.KEYDOWN and pyg.key.get_pressed()[key]:
			return True
		else:
			return False

	def while_key_hold(self,key):
		"""While an key hold"""
		keys = pyg.key.get_pressed()
		if keys[key]:
			return True
		else:
			return False

	def text(self,XY,color,text,font): # Insert a text
		"""Draw an text in screen"""
		if type(font) == int:
			font = self.fonts[font]
		text = font.render(text,True,color)
		textobj = text.get_rect()
		textobj.center= XY
		obj = self.window.blit(text,textobj)
		return obj

	def atext(self,XY,color,text,font,url):
		"""An text, when you click you will be redirected to an url"""
		if type(font) == int:
			font = self.fonts[font]
		text = font.render(text,True,color)
		textobj = text.get_rect()
		textobj.center = XY
		obj = self.window.blit(text,textobj)
		if obj.collidepoint(pyg.mouse.get_pos()):
			if pyg.mouse.get_pressed(3)[0]:
				import webbrowser
				webbrowser.open_new_tab(url)


	def textbox(self,rect,colors,font,act,user_text): # Make a input box
		"""
		rect = Rectangle(e.g. (X,Y,W,H))
		colors = 2 color in rgb(e.g. ((0,0,0),(100,100,100),(255,255,255)))
		font = font object or a id from the list(e.g. 0 or create_font[0])
		act = if the input box is in use, need a external variable(e.g. a[0]==False)
		user_text = all the text of input box, need a external variable(e.g. a[1]=='Hello World!')
		"""
		blacklist = [pyg.K_RETURN,pyg.K_ESCAPE,pyg.K_TAB,pyg.K_DELETE,K_BACKSPACE]

		width = rect[2]
		if type(font) == int:
			font = self.fonts[font]
		if len(user_text) > 1:
			if not width >= (self.scrSize[0]):
				width += round((len(user_text)**2)*0.6)
		if act:
			box = self.rect((rect[0],rect[1]),(width,rect[3]),colors[1])
		else:
			box = self.rect((rect[0],rect[1]),(width,rect[3]),colors[0])
		box2 = self.text((rect[0],rect[1]),colors[2],user_text,font)
		if pyg.mouse.get_pressed(3)[0]:
			if box.collidepoint(pyg.mouse.get_pos()) or box2.collidepoint(pyg.mouse.get_pos()):
				act = True
			else:
				act = False
		else:
			if not act:
				act = False
		if act:
			if not width >= (self.scrSize[0]*2):
				if self.while_key_hold(K_BACKSPACE):
					user_text = user_text[:-1]
					pyg.time.delay(100)
				for ev in self.events():
					if ev.type == pyg.KEYDOWN:
						if not ev.key in blacklist:
							user_text += ev.unicode
					if ev.type == QUIT:
						pyg.quit()

		return (act,user_text)
	def options(self,optionList:list,colors,XY,font,curOption:int):
		if type(font) == int:
			font = self.fonts[font]
		maxOptions = len(optionList)-1
		if len(str(optionList[curOption])) >=6:
			add = 80 + len(str(optionList))*2
		else:
			add = 80
		left =self.button((XY[0]-(add),XY[1]),colors,'<',font)
		right =self.button((XY[0]+(add),XY[1]),colors,'>',font)
		self.button(XY,colors,str(optionList[curOption]),font)
		if left:
			curOption -= 1
			if curOption < 0:
				curOption = maxOptions
			pyg.time.delay(100)
		if right:
			curOption += 1
			if curOption > maxOptions:
				curOption = 0	
			pyg.time.delay(100)
		return curOption

	def update(self,item=None):
		pyg.init()
		if item:
			pyg.display.update(item)
		elif not item:
			item = self.window
			pyg.display.update()

	def delay(self,millieseconds):
		pyg.time.delay(millieseconds)

	def slider(self,colors,XY1,XY2,MaxSize,MaxValue,):
		if XY1[0] > (XY2[0] + MaxSize -1):
			bX = XY2[0] + MaxSize
		else:
			bX = XY1[0]
		pyg.draw.rect(self.window,colors[1],Rect(XY2[0],XY2[1]-5,MaxSize,10))
		s1 = pyg.draw.circle(self.window,colors[0],(bX,XY1[1]),10)
		convert =  round(bX/(MaxSize/MaxValue)*0.82)				#round(((XY1[0])/(MaxSize/MaxValue)*0.9)+2.95)
		if convert > MaxValue:
			convert -= (convert - MaxValue)
		pyg.display.update(s1)
		pyg.time.Clock().tick(600)
		if s1.collidepoint(pyg.mouse.get_pos()):
			if pyg.mouse.get_pressed(3)[0]:
				if pyg.mouse.get_pos()[0] >= (XY2[0]+MaxSize+1):
					return (XY2[0]+MaxSize-1,XY2[1]),convert
				elif pyg.mouse.get_pos()[0] <= (XY2[0]-1):
					return (XY2[0]+1,XY2[1]),convert
				else:
					return (pyg.mouse.get_pos()[0],XY2[1]), convert
			else:
				return (bX,XY1[1]),convert
		else:
			return (bX,XY1[1]),convert

	def rgb_to_hex(self,r,g,b):
		return ('{:X}{:X}{:X}').format(r,g,b)

	def hex_to_rgb(self,hex):
		rgb = []
		for i in (0,2,4):
			decimal = int(hex[i:i+2], 16)
			rgb.append(decimal)

		return tuple(rgb)
	def string_to_list(self,string="A B"):
		li = list(string.split(" "))
		return li
	def list_to_string(self,listo=['a','b']):
		if len(listo) < 1:
			return ' '
		return ' '.join(str(x) for x in listo)
	def set_volume(self,volume=100):
		if volume == 0:
			pyg.mixer.music.set_volume(0)
		else:
			pyg.mixer.music.set_volume(volume/100)
		self.volume = volume

	def play_music(self,file,loop=False):
		music = pyg.mixer.music.load(file) # Need to be mp3
		if loop:
			pyg.mixer.music.play(-1)
		else:
			pyg.mixer.music.play(1)
		return pyg.mixer.music

	def play_sound(self,file,play=False):
		sound = pyg.mixer.Sound(file)
		if play:
			sound.play()
		return sound
	
	def create_json_table(self,table,json_str=False):
		self.database.row_factory = sql.Row
		cur = self.database.cursor()
		rows = cur.execute(f'''SELECT * FROM {table}''').fetchall()
		self.database.commit()
		if json_str:
			b = {}
			for i in rows[0].keys():
				#a =json.dumps({f'{i}': f'{cur.execute(f"SELECT {i} FROM {table}").fetchone()[0]}'}) #
				b[i] =cur.execute(f"SELECT {i} FROM {table}").fetchone()[0]
			#a = json.dumps([dict(ix) for ix in rows])
			return b
		return rows
	def copyToClipboard(self,value):
		copy(value)

	def pasteFromClipboard(self):
		return paste()
	
class console_():
	def __init__(self,file=None):
		self.file = file

	def write(self,content=date.now(),time=True):
		with open(self.file,'r') as f:
			last = f.read()
		with open(self.file,'w') as f:
			dt = date.now()
			if time:
				dt = f' - {dt.strftime("%d/%m/%y - %H:%M:%S")}'
			else:
				dt = ''
			f.write(f'{last}{content}{dt}\n')

	def writes(self,contents=[date.now(),'Console Logs'],times=True):
		for line in contents:
			self.write(f'{line}',times)

import socket
import pickle

class Network():
	def __init__(self,IpV4=""):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = IpV4
		self.port = 5555
		self.addr = (self.server,self.addr)
		self.data = self.connect()

	def setIpV4(self,IPV4=""):
		if IPV4 == "":
			IPV4 = socket.gethostbyname(socket.gethostname())
		
		self.server = IPV4
		self.addr = (self.server,self.addr)
		self.data = self.connect()

	def getData(self):
		return self.data
	
	def connect(self):
		try:
			self.client.connect(self.addr)
			return pickle.loads(self.client.recv(2048))
		except:
			pass

	def send(self,data):
		try:
			self.client.send(pickle.dumps(data))
		except socket.error as e:
			print(e)

from _thread import *

class Server():
	def __init__(self,ControlClass,IpV4=""):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IPV4 = IpV4
		self.port = 5555
	def connect(self):
		try:
			self.server.bind((self.server,self.port))
		except socket.error as e:
			print(e)