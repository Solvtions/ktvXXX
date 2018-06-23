import xbmc,xbmcplugin,xbmcgui,re,os,xbmcaddon,sys,base64,time,urllib2,string,logging,array,news,shutil
AddonID = 'plugin.video.Kritik'
FabAddon = xbmcaddon.Addon('plugin.video.Kritik')
Username = FabAddon.getSetting("Username")
Password = FabAddon.getSetting("Password")
PVRon = FabAddon.getSetting("PVRUpdater")
lehekylg = base64.b64decode("aHR0cDovL21lb3d5YXBtZW93LmNvbQ==")
pordinumber = base64.b64decode("ODA4MA==")
EPGurl = base64.b64decode("JXM6JXMveG1sdHYucGhwP3VzZXJuYW1lPSVzJnBhc3N3b3JkPSVz")%(lehekylg,pordinumber,Username,Password)
NewPVR = xbmc.translatePath('special://home/userdata/addon_data/pvr.iptvsimple/players.m3u8')
iVueRepo = xbmc.translatePath('special://home/addons/xbmc.repo.ivueguide')
dialog = xbmcgui.Dialog()
Duration=FabAddon.getSetting("FinalDuration")
if Duration == '':
	FabAddon.setSetting(id='FinalDuration', value='Off')

if os.path.exists(iVueRepo):
	shutil.rmtree(iVueRepo)

def Check():
	if PVRon == 'true':
		time.sleep(20)
		if os.path.exists(NewPVR):
			os.remove(NewPVR)
		time.sleep(1)
		try:
			f = open(NewPVR, 'a')
			UserList = base64.b64decode("JXM6JXMvZ2V0LnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcyZ0eXBlPW0zdV9wbHVzJm91dHB1dD10cw==")%(lehekylg,pordinumber,Username,Password)
			link = open_url(UserList).replace('\n','').replace('\r','&split&')
			a,b = newlink = link.split('&split&#EXTINF:-1 tvg-id="" tvg-name="Absolute 80')
			OutpuT = a.replace("&split&","\n").replace("#EXTM3U","#EXTM3U\n")
			f = open(NewPVR, 'a')
			f.write(OutpuT)
			if PVRon == 'false':
				FabAddon.setSetting(id='PVRUpdater', value='true')
			xbmc.executebuiltin('Notification(PVR Updated,[COLOR white]PVR Playlist Updated[/COLOR],3000,special://home/addons/'+AddonID+'/icon.png)')
		except:
			if PVRon == 'true':
				FabAddon.setSetting(id='PVRUpdater', value='false')
				xbmc.executebuiltin('Notification(PVR Update Failed,[COLOR white]PVR failed - now turned off[/COLOR],3000,special://home/addons/'+AddonID+'/icon.png)')

def open_url(url):
    try:
        req = urllib2.Request(url,headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except:quit()

TypeOfMessage="t"; (NewImage,NewMessage)=news.FetchNews();
news.CheckNews(TypeOfMessage,NewImage,NewMessage,True);
Check()