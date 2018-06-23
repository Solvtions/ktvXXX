import threading,xbmc,xbmcplugin,xbmcgui,re,os,xbmcaddon,sys
import shutil,plugintools,installer
import zipfile
import urlparse
import urllib,urllib2,json
import common,xbmcvfs,downloader,extract
import datetime
import base64, time
import unicodedata
from datetime import datetime
from datetime import timedelta
import maintenance
AddonID = 'plugin.video.Kritik'
AddonTitle = 'Kritik Live TV'
Images=xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources/art/'));
fanart = Images+'fanart.jpg'
icon = Images+'icon.png'
FabAddon = xbmcaddon.Addon('plugin.video.Kritik')
ADDON=xbmcaddon.Addon(id='plugin.video.Kritik')
dialog       =  xbmcgui.Dialog()
dialogprocess =  xbmcgui.DialogProgress()
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata/',''))
FabData      =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.Kritik/',''))
HOME         =  xbmc.translatePath('special://home/')
Username=plugintools.get_setting("Username")
Password=plugintools.get_setting("Password")
PVRon = plugintools.get_setting("PVRUpdater")
lehekylg= base64.b64decode("aHR0cDovL3RoZXBrLmNv") #####
pordinumber="2086"
BASEURL = base64.b64decode("bmFkYQ==")
AddonRes = xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources'))
loginurl   = base64.b64decode("JXM6JXMvZ2V0LnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcyZ0eXBlPW0zdV9wbHVzJm91dHB1dD10cw==")%(lehekylg,pordinumber,Username,Password)
THE_DATE = time.strftime("%Y%m%d")
now = datetime.now()
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)

##################################################################################


def Print(OuT):
	HOME = xbmc.translatePath('special://home')
	if "Users\\" in HOME:
		Name,Appdata = str(HOME).split("Roaming")
		Desktop = Name.replace('AppData','Desktop')
	ResultFile = Desktop + 'test.txt'
	if os.path.exists(ResultFile):
		os.remove(ResultFile)
		time.sleep(3)
	f = open(ResultFile, 'a')
	f.write(OuT)

def PVRbeta(self):
	PVRSimple = xbmc.translatePath('special://home/userdata/addon_data/pvr.iptvsimple/')
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	if os.path.exists(PVRSimple):
		shutil.rmtree(PVRSimple)
	nullPVR   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}'
	nullLiveTV = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":false},"id":1}'
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	EPGurl   = base64.b64decode("JXM6JXMveG1sdHYucGhwP3VzZXJuYW1lPSVzJnBhc3N3b3JkPSVz")%(lehekylg,pordinumber,Username,Password)
	
	xbmc.executeJSONRPC(nullLiveTV)
	xbmc.executeJSONRPC(nulldemo)
	xbmc.executeJSONRPC(nullPVR)
	time.sleep(2)
	
	if not os.path.exists(PVRSimple):
		os.makedirs(PVRSimple)
	shutil.copyfile(AddonRes+'/PVRset.xml', PVRSimple+'settings.xml')
	BetaPVR = PVRSimple+'players.m3u8'
	time.sleep(1)

	f = open(BetaPVR, 'a')

	UserList = base64.b64decode("JXM6JXMvZ2V0LnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcyZ0eXBlPW0zdV9wbHVzJm91dHB1dD10cw==")%(lehekylg,pordinumber,Username,Password)
	link = open_url(UserList).replace('\n','').replace('\r','&split&')
	a,b = link.split('&split&#EXTINF:-1 tvg-id="" tvg-name="Absolute 80')
	OutpuT = a.replace("&split&","\n").replace("#EXTM3U","#EXTM3U\n")
	f = open(BetaPVR, 'a')
	f.write(OutpuT)

	time.sleep(1)
	xbmc.executeJSONRPC(IPTVon)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uPath', value='special://home/userdata/addon_data/pvr.iptvsimple/Fab.m3u8')
	time.sleep(3)
	xbmc.executeJSONRPC(jsonSetPVR)
	time.sleep(3)
	xbmc.executeJSONRPC(IPTVon)
	if PVRon == 'false':
		FabAddon.setSetting(id='PVRUpdater', value='true')
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	xbmc.executebuiltin('Notification(PVR Setup,[COLOR white]PVR is now setup allow loading to finish[/COLOR],3000,special://home/addons/'+AddonID+'/icon.png)')
	time.sleep(5)
	xbmc.executebuiltin("Container.Refresh")

def correctPVR(self):

	try:
		connection = urllib2.urlopen(loginurl)
		print connection.getcode()
		connection.close()
		#playlist found, user active & login correct, proceed to addon
		pass
		
	except urllib2.HTTPError, e:
		print e.getcode()
		dialog.ok("[COLOR white]Error[/COLOR]",'[COLOR white]This process will not run as your account has expired[/COLOR]',' ','[COLOR white]Please check your account information[/COLOR]')
		sys.exit(1)
		xbmc.executebuiltin("Dialog.Close(busydialog)")
		

	RAM = int(xbmc.getInfoLabel("System.Memory(total)")[:-2])
	RAMM = xbmc.getInfoLabel("System.Memory(total)")
	
	if RAM < 1999:
		choice = xbmcgui.Dialog().yesno('[COLOR white]Low Power Device [COLOR lime]RAM: ' + RAMM + '[/COLOR][/COLOR]', '[COLOR white]Your device has been detected as a low end device[/COLOR]', '[COLOR white]We recommend avoiding PVR usage for this reason[/COLOR]', '[COLOR white]We cannnot support low end devices for PVR[/COLOR]', nolabel='[COLOR lime]OK, Cancel this[/COLOR]',yeslabel='[COLOR red]I know, proceed[/COLOR]')
		if choice == 0:
			sys.exit(1)
		elif choice == 1:
			pass
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	nullPVR   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}'
	nullLiveTV = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":false},"id":1}'
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	EPGurl   = base64.b64decode("JXM6JXMveG1sdHYucGhwP3VzZXJuYW1lPSVzJnBhc3N3b3JkPSVz")%(lehekylg,pordinumber,Username,Password)

	xbmc.executeJSONRPC(nullPVR)
	xbmc.executeJSONRPC(nullLiveTV)
	time.sleep(10)
	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	time.sleep(25)
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	dialog.ok("[COLOR white]" + AddonTitle + "[/COLOR]",'[COLOR white]We\'ve copied your logins to the PVR Guide[/COLOR]',' ','[COLOR white]You [B]MUST[/B] allow time to load the EPG to avoid issues.[/COLOR]')
	xbmc.executebuiltin("Container.Refresh")

def disablePVR(self):
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	nullPVR   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}'
	nullLiveTV = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":false},"id":1}'
	PVRdata   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/','pvr.iptvsimple'))
	if PVRon == 'false':
		FabAddon.setSetting(id='PVRUpdater', value='true')
	xbmc.executeJSONRPC(nullLiveTV)
	time.sleep(2)
	xbmc.executeJSONRPC(nullPVR)
	shutil.rmtree(PVRdata)
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	xbmc.executebuiltin('Notification(PVR Disabled,[COLOR white]PVR Guide is now disabled[/COLOR],2000,special://home/addons/'+AddonID+'/icon.png)')
	xbmc.executebuiltin("Container.Refresh")

def SpeedChoice():
	choice = dialog.select("[COLOR white]" + AddonTitle + " Speedtest[/COLOR]", ['[COLOR white]Ookla Speedtest[/COLOR]','[COLOR white]Fast.com Speedtest by Netflix[/COLOR]'])
	if choice == 0:
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.Kritik/speedtest.py")')
	if choice == 1:
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.Kritik/fastload.py")')

##########################################################################

AMS10 = "http://ams.download.10gbps.io/10mb.bin"
AMS100 = "http://ams.download.10gbps.io/100mb.bin"
CHI10 = "http://chi.download.10gbps.io/10mb.bin"
CHI100 = "http://chi.download.10gbps.io/100mb.bin"
LA10 = "http://lax.download.10gbps.io/10mb.bin"
LA100 = "http://lax.download.10gbps.io/100mb.bin"
FRA10 = "http://rbx.proof.ovh.net/files/10Mio.dat"
FRA100 = "http://rbx.proof.ovh.net/files/100Mio.dat"
CA10 = "http://bhs.proof.ovh.net/files/10Mio.dat"
CA100 = "http://bhs.proof.ovh.net/files/100Mio.dat"
LON10 = "http://lon.download.10gbps.io/10mb.bin"
LON100 = "http://lon.download.10gbps.io/100mb.bin"
NY10 = "http://nyc.download.10gbps.io/10mb.bin"
NY100 = "http://nyc.download.10gbps.io/100mb.bin"
SYD10 = "http://speedtest.syd01.softlayer.com/downloads/test10.zip"
SYD100 = "http://speedtest.syd01.softlayer.com/downloads/test100.zip"

##########################################################################

def DCtest(params):
	addItem('[COLOR white]Canada[/COLOR]','',101,icon,fanart,'')
	addItem('[COLOR white]Chicago[/COLOR]','',102,icon,fanart,'')
	addItem('[COLOR white]France[/COLOR]','',103,icon,fanart,'')
	addItem('[COLOR white]LA[/COLOR]','',104,icon,fanart,'')
	addItem('[COLOR white]London[/COLOR]','',105,icon,fanart,'')
	addItem('[COLOR white]Netherlands[/COLOR]','',106,icon,fanart,'')
	addItem('[COLOR white]New York[/COLOR]','',107,icon,fanart,'')
	addItem('[COLOR white]Sydney[/COLOR]','',108,icon,fanart,'')
	addItem('[COLOR white]------------------------------[/COLOR]','',99999,icon,fanart,'')
	addItem('[COLOR white]**Disclaimer**[/COLOR]','',109,icon,fanart,'')

def Disclaimer():
	common.TxtBox('\n\nPlease note these speedtest files are not hosted by us or our servers, they are hosted in common global datacenters which should provide a guide on your best server location\n\nWe advise you test these thoroughly to ensure you have an accurate result in these tests, the results can be provided to the Fab team to assist with connection issues\n\nWe will update this feature soon once we see the results from our users, this is currently just a rough guide')

def CAN():
	choice = dialog.select("[COLOR white]Canada[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(CA10)
	if choice == 1:
		runtest(CA100)

def CHI():
	choice = dialog.select("[COLOR white]Chicago[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(CHI10)
	if choice == 1:
		runtest(CHI100)

def FRA():
	choice = dialog.select("[COLOR white]France[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(FRA10)
	if choice == 1:
		runtest(FRA100)

def LA():
	choice = dialog.select("[COLOR white]LA[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(LA10)
	if choice == 1:
		runtest(LA100)

def LON():
	choice = dialog.select("[COLOR white]London[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(LON10)
	if choice == 1:
		runtest(LON100)

def AMS():
	choice = dialog.select("[COLOR white]Netherlands[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(AMS10)
	if choice == 1:
		runtest(AMS100)

def NY():
	choice = dialog.select("[COLOR white]New York[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(NY10)
	if choice == 1:
		runtest(NY100)

def SYD():
	choice = dialog.select("[COLOR white]Sydney[/COLOR]", ['[COLOR white]10Mb Test[/COLOR]','[COLOR white]100Mb Test[/COLOR]'])
	if choice == 0:
		runtest(SYD10)
	if choice == 1:
		runtest(SYD100)

max_Bps = 0.0
currently_downloaded_bytes = 0.0

#-----------------------------------------------------------------------------------------------------------------
def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle,"Connecting to server",'[COLOR lime][I]Testing your internet speed...[/I][/COLOR]', 'Please wait...')
    dp.update(0)
    start_time=time.time()
    try:
        urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
    except:
        pass    
    return ( time.time() - start_time )
#-----------------------------------------------------------------------------------------------------------------
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        global max_Bps
        global currently_downloaded_bytes
        
        try:
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded_bytes = float(numblocks) * blocksize
            currently_downloaded = currently_downloaded_bytes / (1024 * 1024) 
            Bps_speed = currently_downloaded_bytes / (time.time() - start_time) 
            if Bps_speed > 0:                                                 
                eta = (filesize - numblocks * blocksize) / Bps_speed 
                if Bps_speed > max_Bps: max_Bps = Bps_speed
            else: 
                eta = 0 
            kbps_speed = Bps_speed * 8 / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            dp.update(percent)
        except: 
            currently_downloaded_bytes = float(filesize)
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise Exception("Cancelled")
#-----------------------------------------------------------------------------------------------------------------
def make_dir(mypath, dirname):
    import xbmcvfs
    
    if not xbmcvfs.exists(mypath): 
        try:
            xbmcvfs.mkdirs(mypath)
        except:
            xbmcvfs.mkdir(mypath)
    
    subpath = os.path.join(mypath, dirname)
    
    if not xbmcvfs.exists(subpath): 
        try:
            xbmcvfs.mkdirs(subpath)
        except:
            xbmcvfs.mkdir(subpath)
            
    return subpath
#-----------------------------------------------------------------------------------------------------------------
def GetEpochStr():
    time_now  = datetime.now()
    epoch     = time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
    epoch_str = str('%f' % epoch)
    epoch_str = epoch_str.replace('.','')
    epoch_str = epoch_str[:-3]
    return epoch_str
#-----------------------------------------------------------------------------------------------------------------
def runtest(url):
    addon_profile_path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    speed_test_files_dir = make_dir(addon_profile_path, 'speedtestfiles')
    speed_test_download_file = os.path.join(speed_test_files_dir, GetEpochStr() + '.speedtest')
    timetaken = download(url, speed_test_download_file)
    os.remove(speed_test_download_file)
    avgspeed = ((currently_downloaded_bytes / timetaken) * 8 / ( 1024 * 1024 ))
    maxspeed = (max_Bps * 8/(1024*1024))
    if avgspeed < 2:
        livestreams = 'Not likely to play at all'
        onlinevids = 'Expect HEAVY buffering'
        rating = '[COLOR white][B] Verdict: Very Poor   | Score: [COLOR white]1/10[/B][/COLOR]'
    elif avgspeed < 5:
        livestreams = 'You might be ok for SD content.'
        onlinevids = 'SD/DVD quality should be ok, HD probably not.'
        rating = '[COLOR white][B]Poor   | Score: [COLOR white]2/10[/B][/COLOR]'
    elif avgspeed < 10:
        livestreams = 'Some HD streams may struggle, SD should be fine.'
        onlinevids = '720 should be fine but some 1080 may struggle.'
        rating = '[COLOR white][B]OK   | Score: [COLOR white]4/10[/B][/COLOR]'
    elif avgspeed < 15:
        livestreams = 'All streams including HD should stream fine.'
        onlinevids = '720 & 1080 should stream fine'
        rating = '[COLOR white][B]Good   | Score: [COLOR white]6/10[/B][/COLOR]'
    elif avgspeed < 20:
        livestreams = 'All streams should play fine'
        onlinevids = 'All VoD should play fine'
        rating = '[COLOR white][B][I]Very good[/I]   | Score: [COLOR white]8/10[/B][/COLOR]'
    else:
        livestreams = 'All streams should play smooth'
        onlinevids = 'All VoD should play smooth'
        rating = '[COLOR white][B]Excellent   | Score: [COLOR white]10/10[/B][/COLOR]'
    print "Average Speed: " + str(avgspeed)
    print "Max. Speed: " + str(maxspeed)
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(
    '[COLOR white][B]Your Result:[/COLOR][/B] ' + rating,
    #'[COLOR blue]Duration:[/COLOR] %.02f secs' % timetaken,
    '[COLOR white][B]Live Streams:[/COLOR][/B] ' + livestreams,
    '[COLOR white][B]Movie Streams:[/COLOR][/B] ' + onlinevids,
	'[COLOR white][B]Duration:[/COLOR][/B] %.02f secs ' % timetaken + '[COLOR white][B]Average Speed:[/B][/COLOR] %.02f Mb/s ' % avgspeed + '[COLOR white][B]Max Speed:[/B][/COLOR] %.02f Mb/s ' % maxspeed,
	#'[COLOR blue]Maximum Speed:[/COLOR] %.02f Mb/s ' % maxspeed,
	)

def install(name,url):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create(AddonTitle,"Installing...",'', 'Please Wait')
    lib=os.path.join(path, 'content.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
    time.sleep(3)
    dp = xbmcgui.DialogProgress()
    dp.create(AddonTitle,"Installing...",'', 'Please Wait')
    dp.update(0,"", "Installing... Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    unzip(lib,addonfolder,dp)

def unzip(_in, _out, dp):
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'Process was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True	

def AddDir(name, url, mode, iconimage, description="", isFolder=True, background=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    a=sys.argv[0]+"?url=None&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+a
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def AddDir2(name, url, mode, iconimage, description="", isFolder=True, background=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    a=sys.argv[0]+"?url=None&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def addItem(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addItem2(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==9099 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addXMLMenu(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def open_url(url):
    try:
        req = urllib2.Request(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except:quit()

def OPEN_URL_NORMAL(url):

	if "https://" in url:
		url = url.replace("https://","http://")
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')
	response = urllib2.Request(req)
	link=response.read()
	response.close()
	return link

def Buildlist(url):
    list = common.m3u2list(url)
    for channel in list:
        name = common.GetEncodeString(channel["display_name"])
        AddDir(name ,channel["url"], 3, iconimage, isFolder=False)
		
def PlayUrl(name, url, iconimage=None):
        _NAME_=name
        list = common.m3u2list(loginurl)
        for channel in list:
            name = common.GetEncodeString(channel["display_name"])
            stream=channel["url"]
            if _NAME_ in name:
                listitem = xbmcgui.ListItem(path=stream, thumbnailImage=iconimage)
                listitem.setInfo(type="Video", infoLabels={ "Title": name })
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)				

def Get_Params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?','')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0].lower()] = splitparams[1]
    return param
	
params=Get_Params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url = urllib.unquote_plus(params["url"])
except:pass
try:name = urllib.unquote_plus(params["name"])
except:pass
try:iconimage = urllib.unquote_plus(params["iconimage"])
except:pass
try:mode = int(params["mode"])
except:pass
try:description = urllib.unquote_plus(params["description"])
except:pass

if mode == 7:
	quit
elif mode == 8:
	iVuemenu()
elif mode == 12:
	PVRmenu()
elif mode == 1:
	Buildlist(url)
elif mode == 3:
    PlayUrl(name, url, iconimage)
elif mode == 9:
	SpeedChoice()
elif mode == 10:
	correctPVR()
elif mode == 11:
	xbmc.executebuiltin('ActivateWindow(TVGuide)')
elif mode == 15:
	installer.INSTALLAPK(name,url,description)
elif mode == 16:
	PVRbeta()
elif mode == 17:
	disablePVR()
elif mode==18:
        maintenance.viewLogFile()
elif mode==19:
		maintenance.autocleannow()
elif mode==20:
		maintenance.clearCache()
elif mode==21:
		maintenance.DeleteCrashLogs()
elif mode==22:
		maintenance.deleteThumbnails()
elif mode==23:
		maintenance.purgePackages()
elif mode==24:
		maintenance.view_LastError()
elif mode==25:
		maintenance.viewErrors()
elif mode==26:
		maintenance.CheckUpdates()
elif mode == 100:
		DCtest()
elif mode == 101:
		CAN()
elif mode == 102:
		CHI()
elif mode == 103:
		FRA()
elif mode == 104:
		LA()
elif mode == 105:
		LON()
elif mode == 106:
		AMS()
elif mode == 107:
		NY()
elif mode == 108:
		SYD()
elif mode == 109:
		Disclaimer()