"""
    Copyright (C) 2016 ECHO Coder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#Imports
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import time
import requests
import re

#Default veriables
AddonTitle     = "[COLOR pink][B]Chaturbate[/B][/COLOR]"
addon_id       = 'plugin.video.chaturbate'
dialog         = xbmcgui.Dialog()
ADDON          = xbmcaddon.Addon(id=addon_id)
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
next_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/next.png'))
twitter_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/twitter.png'))
pc_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pc.png'))
featured_icon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/featured.png'))
female_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/female.png'))
male_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/male.png'))
couple_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/couples.png'))
trans_icon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/trans.png'))

PARENTAL_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'controls.txt'))
TERMS          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'disclaimer.txt'))
I_AGREE        = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'agreed.txt'))
PARENTAL_FOLDER= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))

def MAIN_MENU():

	if not os.path.exists(I_AGREE): 
		f = open(TERMS,mode='r'); msg = f.read(); f.close()
		TextBoxes("%s" % msg)
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR white]Do you agree to the terms and conditions of this addon?[/COLOR]','',yeslabel='[B][COLOR lime]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 1:
			if not os.path.exists(PARENTAL_FOLDER):
				os.makedirs(PARENTAL_FOLDER)
			open(I_AGREE, 'w')
		else:
			sys.exit(0)

	if not os.path.exists(PARENTAL_FOLDER):
		choice = xbmcgui.Dialog().yesno(AddonTitle, "[COLOR white]We can see that this is your first time using the addon. Would you like to enable the parental controls now?[/COLOR]","" ,yeslabel='[B][COLOR red]NO[/COLOR][/B]',nolabel='[B][COLOR lime]YES[/COLOR][/B]')
		if choice == 0:
			PARENTAL_CONTROLS_PIN()
		else:
			os.makedirs(PARENTAL_FOLDER)

	elif os.path.exists(PARENTAL_FILE):
		vq = _get_keyboard( heading="Please Enter Your Password" )
		if ( not vq ): 
			dialog.ok(AddonTitle,"Sorry, no password was entered.")
			sys.exit(0)
		pass_one = vq

		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				if not password == pass_one:
					if not current_pin == pass_one:
						dialog.ok(AddonTitle,"Sorry, the password you entered was incorrect.")
						sys.exit(0)

	result = requests.get('http://www.chaturbate.com')
	
	match = re.compile('<ul class="sub-nav">(.+?)<div class="content">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile("<li(.+?)</li>",re.DOTALL).findall(string)
	fail = 0
	videos = 0
	for item in match2:
		url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
		title=re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.chaturbate.com" + url4
		if "featured" in title.lower():
			name = "[COLOR white][B]" + title + "[/B][/COLOR]"
			addDir(name,url,1,featured_icon,fanart,'')
		elif "female" in title.lower():
			name = "[COLOR white][B]FEMALES[/B][/COLOR]"
			addDir(name,url,1,female_icon,fanart,'')
		elif "male" in title.lower():
			name = "[COLOR white][B]MALES[/B][/COLOR]"
			addDir(name,url,1,male_icon,fanart,'')
		elif "couple" in title.lower():
			name = "[COLOR white][B]COUPLES[/B][/COLOR]"
			addDir(name,url,1,couple_icon,fanart,'')
		elif "trans" in title.lower():
			name = "[COLOR white][B]TRANSEXUAL[/B][/COLOR]"
			addDir(name,url,1,trans_icon,fanart,'')

	addItem("[COLOR yellow][B]Twitter Support: @echo_coding[/B][/COLOR]","url",999,twitter_icon,fanart,'')
	if not os.path.exists(PARENTAL_FILE):
		addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR red]OFF[/COLOR][/B][/COLOR]","url",11,pc_icon,fanart,'')
	else:
		addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR lime]ON[/COLOR][/B][/COLOR]","url",11,pc_icon,fanart,'')

	xbmc.executebuiltin('Container.SetViewMode(500)')

def GET_CONTENT(url):

	checker = url
	result = requests.get(url)
	match = re.compile('<ul class="list">(.+?)<ul class="paging">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile("<li>(.+?)</li>",re.DOTALL).findall(string)
	for item in match2:
		try:
			title=re.compile('<a href=".+?"> (.+?)</a>').findall(item)[0]
			url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
			iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
			try:
				age=re.compile('<span class="age gender.+?">(.+?)</span>').findall(item)[0]
			except: age = "Unknown"
			if 'thumbnail_label_c_hd">' in item:
				name = "[B][COLOR pink]HD[/COLOR][COLOR yellow] - " + title + " - Age " + age + "[/COLOR][/B]"
			elif 'label_c_new' in item:
				name = "[B][COLOR blue]NEW[/COLOR][COLOR yellow] - " + title + " - Age " + age + "[/COLOR][/B]"
			else:
				name = "[B][COLOR yellow]" + title + " - Age " + age + "[/COLOR][/B]"
			addItem(name,url,3,iconimage,iconimage,'')
		except: pass

	try:
		np=re.compile('<ul class="paging">(.+?)</ul>',re.DOTALL).findall(result.content)
		for item in np:
			next=re.compile('<li><a href="(.+?)" class="next endless_page_link">next</a></li>').findall(item)[0]
			url = "http://chaturbate.com" + str(next)
			addDir('[COLOR pink]Next Page >>[/COLOR]',url,1,next_icon,fanart,'')       
	except:pass

	xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(' ','').capitalize()
        if len(string)>1:
            url = "http://www.youporn.com/search/?query=" + string
            GET_CONTENT(url)
        else: quit()

def PLAY_URL(name,url,iconimage):
	
	dp = GET_LUCKY()
	url = "http://www.chaturbate.com" + url
	result = requests.get(url)
	match = re.compile('<head>(.+?)</html>',re.DOTALL).findall(result.content)
	string = str(match).replace('\\','').replace('(','').replace(')','')
	url = re.compile("playsinline autoplay><source src='(.+?)'").findall(string)[0]
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	time.sleep(2.00)
	dp.close()
	xbmc.Player ().play(url, liz, False)

def PARENTAL_CONTROLS():

	found = 0
	if not os.path.exists(PARENTAL_FILE):
		found = 1
		addItem("[COLOR yellow][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')
	else:
		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				found = 1
				addItem("[COLOR yellow][B]PARENTAL CONTROLS - [/COLOR][COLOR lime]ON[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR yellow][B]Current Password - [/COLOR][COLOR orangered]" + str(password) + "[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR lime][B]Change Password[/B][/COLOR]","url",12,icon,fanart,'')
				addItem("[COLOR red][B]Disable Password[/B][/COLOR]","url",13,icon,fanart,'')

	if found == 0:
		addItem("[COLOR yellow][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')

def PARENTAL_CONTROLS_PIN():

	vq = _get_keyboard( heading="Please Set Password" )
	if ( not vq ):
		dialog.ok(AddonTitle,"Sorry, no password was entered.")
		sys.exit(0)
	pass_one = vq

	vq = _get_keyboard( heading="Please Confirm Your Password" )
	if ( not vq ):
		dialog.ok(AddonTitle,"Sorry, no password was entered.")
		sys.exit(0)
	pass_two = vq
		
	if not os.path.exists(PARENTAL_FILE):
		if not os.path.exists(PARENTAL_FOLDER):
			os.makedirs(PARENTAL_FOLDER)
		open(PARENTAL_FILE, 'w')

		if pass_one == pass_two:
			writeme = base64.b64encode(pass_one)
			f = open(PARENTAL_FILE,'w')
			f.write('<password>'+str(writeme)+'</password>')
			f.close()
			dialog.ok(AddonTitle,'Your password has been set and parental controls have been enabled.')
			xbmc.executebuiltin("Container.Refresh")
		else:
			dialog.ok(AddonTitle,'The passwords do not match, please try again.')
			sys.exit(0)
	else:
		os.remove(PARENTAL_FILE)
		
		if pass_one == pass_two:
			writeme = base64.b64encode(pass_one)
			f = open(PARENTAL_FILE,'w')
			f.write('<password>'+str(writeme)+'</password>')
			f.close()
			dialog.ok(AddonTitle,'Your password has been set and parental controls have been enabled.')
			xbmc.executebuiltin("Container.Refresh")
		else:
			dialog.ok(AddonTitle,'The passwords do not match, please try again.')
			sys.exit(0)

def PARENTAL_CONTROLS_OFF():

	try:
		os.remove(PARENTAL_FILE)
		dialog.ok(AddonTitle,'Parental controls have been disabled.')
		xbmc.executebuiltin("Container.Refresh")
	except:
		dialog.ok(AddonTitle,'There was an error disabling the parental controls.')
		xbmc.executebuiltin("Container.Refresh")

def GET_LUCKY():

	import random
	lucky = random.randrange(10)
	
	dp = xbmcgui.DialogProgress()
	
	if lucky == 1:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]We are getting the moisturiser.[/B][/COLOR]','[B][COLOR azure]Do you have the wipes ready?[/B][/COLOR]' )
	elif lucky == 2:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]I am just taking off my pants.[/B][/COLOR]','[B][COLOR azure]Darn belt![/B][/COLOR]' )
	elif lucky == 3:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Are the curtains closed?[/B][/COLOR]','[B][COLOR azure]Oh baby its cold outside![/B][/COLOR]' )
	elif lucky == 4:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]This is my fifth time today.[/B][/COLOR]','[B][COLOR azure]How about you?[/B][/COLOR]' )
	elif lucky == 5:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Please no buffer, please no buffer![/B][/COLOR]')
	elif lucky == 6:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]I think I am going blind :-/[/B][/COLOR]','[B][COLOR azure]Oh no, just something in my eye.[/B][/COLOR]' )
	elif lucky == 7:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Did I turn the oven off?[/B][/COLOR]','[B][COLOR azure]It can wait![/B][/COLOR]' )
	elif lucky == 8:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Your video is coming. Are you?[/B][/COLOR]','[B][COLOR azure]Do you get it?[/B][/COLOR]' )
	elif lucky == 9:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Kodi does not save your browsing history :-D[/B][/COLOR]','[B][COLOR azure]Thats lucky isnt it :-)[/B][/COLOR]' )
	else:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]There are more XXX addons by ECHO.[/B][/COLOR]','[B][COLOR azure]Just so you know.[/B][/COLOR]' )

	return dp

def TextBoxes(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('XNXX.com - Story') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                               
        return param

def addItem(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

params=get_params(); url=None; name=None; mode=None; site=None; description=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: mode=int(params["mode"])
except: pass
try: description=urllib.quote_plus(params["description"])
except: pass

if mode==None or url==None or len(url)<1: MAIN_MENU()
elif mode==1: GET_CONTENT(url)
elif mode==2: SEARCH()
elif mode==3: PLAY_URL(name,url,iconimage)
elif mode==11: PARENTAL_CONTROLS()
elif mode==12: PARENTAL_CONTROLS_PIN()
elif mode==13: PARENTAL_CONTROLS_OFF()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
