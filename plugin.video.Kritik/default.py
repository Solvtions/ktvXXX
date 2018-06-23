import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,datetime,os,json,base64,plugintools,xbmc,socket
from datetime import datetime as dtdeep
import GoDev
import common,xbmcvfs,zipfile,downloader,extract
import xml.etree.ElementTree as ElementTree
import unicodedata
import time
import string
reload(sys)
dialog       =  xbmcgui.Dialog()
sys.setdefaultencoding('utf8')
SKIN_VIEW_FOR_MOVIES="515"
addonDir = plugintools.get_runtime_path()
global kontroll
global EPGColour
addon_id = "plugin.video.Kritik"
background = "YmFja2dyb3VuZC5wbmc=" 
defaultlogo = "ZGVmYXVsdGxvZ28ucG5n" 
hometheater = "aG9tZXRoZWF0ZXIuanBn"
noposter = "bm9wb3N0ZXIuanBn"
theater = "dGhlYXRlci5qcGc="
addonxml = "YWRkb24ueG1s"
addonpy = "ZGVmYXVsdC5weQ=="
icon = "aWNvbi5wbmc="
fanart = "ZmFuYXJ0LmpwZw=="
supplier = "RmFiIElQVFY="
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png')) 
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg')) 
APKS = base64.b64decode("aHR0cDovL2ZhYmlwdHYuY29tL2Fwa3MvbmV3YXBrcy50eHQ=")
HOME =  xbmc.translatePath('special://home/')
lehekylg= base64.b64decode("aHR0cDovL3RoZXBrLmNv")
pordinumber="2086"
message = "VU5BVVRIT1JJWkVEIEVESVQgT0YgQURET04h"
kasutajanimi=plugintools.get_setting("Username")
salasona=plugintools.get_setting("Password")
F1ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'F1.png'))
BASEURL = base64.b64decode("bmFkYQ==")
LOAD_LIVEchan = os.path.join( plugintools.get_runtime_path() , "resources" , "art/arch" )
loginurl   = base64.b64decode("JXM6JXMvZ2V0LnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcyZ0eXBlPW0zdV9wbHVzJm91dHB1dD10cw==")%(lehekylg,pordinumber,kasutajanimi,salasona)

def run():
    global pnimi
    global televisioonilink
    global LiveCats
    global PlayerAPI
    global filmilink
    global andmelink
    global uuenduslink
    global lehekylg
    global LOAD_LIVE
    global uuendused
    global vanemalukk
    global version
    global showxxx
    version = int(get_live("MQ=="))
    kasutajanimi=plugintools.get_setting("Username")
    salasona=plugintools.get_setting("Password")
    if not kasutajanimi:
        kasutajanimi = "NONE"
        salasona="NONE"
	
    uuendused=plugintools.get_setting(sync_data("dXVlbmR1c2Vk"))
    vanemalukk=plugintools.get_setting(sync_data("dmFuZW1hbHVraw=="))
    showxxx=plugintools.get_setting("showxxx")
    pnimi = get_live("T25lIFZpZXcg")
    LOAD_LIVE = os.path.join( plugintools.get_runtime_path() , "resources" , "art" )
    plugintools.log(pnimi+get_live("U3RhcnRpbmcgdXA="))
    televisioonilink = get_live("JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfbGl2ZV9jYXRlZ29yaWVz")%(lehekylg,pordinumber,kasutajanimi,salasona)
    LiveCats = get_live("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9saXZlX2NhdGVnb3JpZXM=")%(lehekylg,pordinumber,kasutajanimi,salasona)
    PlayerAPI = get_live("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXM=")%(lehekylg,pordinumber,kasutajanimi,salasona)
    filmilink = vod_channels("JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfdm9kX2NhdGVnb3JpZXM=")%(lehekylg,pordinumber,kasutajanimi,salasona)
    andmelink = vod_channels("JXM6JXMvcGFuZWxfYXBpLnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcw==")%(lehekylg,pordinumber,kasutajanimi,salasona)
    params = plugintools.get_params()

    if params.get("action") is None:
        peamenyy(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    plugintools.close_item_list()

def peamenyy(params):
    plugintools.log(pnimi+vod_channels("TWFpbiBNZW51")+repr(params))
    load_channels()
    if not lehekylg:
        plugintools.open_settings_dialog()

    channels = kontroll()
    if channels == 1 and GoDev.mode != 5 and GoDev.mode != 1:
        plugintools.log(pnimi+vod_channels("TG9naW4gU3VjY2Vzcw=="))
        plugintools.add_item( action=vod_channels("c2VjdXJpdHlfY2hlY2s="),  title="[COLOR gold][B][I]Live TV Channels[/I][/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")) , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
        plugintools.add_item( action=vod_channels("ZGV0ZWN0X21vZGlmaWNhdGlvbg=="),   title="[COLOR gold][B]VOD/TV SHOWS[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("dm9kLnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
        plugintools.add_item( action=vod_channels("VGhlRGV2"),   title="[COLOR gold][B]CATCHUP TV[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("dm9kLnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=True )
        #plugintools.add_item( action=vod_channels("TGlzdGluZ3M="),   title="Listings" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("aWNvbi5wbmc=")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
        #plugintools.add_item( action=vod_channels("R29EZXYuRmFiU3BvcnRz"),   title="Replays" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("c3BvcnRzLnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=False )
        #plugintools.add_item( action=vod_channels("R29EZXYuTUxCUGFzcw=="),   title="MLB" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("TUxCLnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=False )
        plugintools.add_item( action=vod_channels("bWFpbnRNZW51"),   title="[COLOR white][B]Maintenance Tools[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("aWNvbi5wbmc=")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
        plugintools.add_item( action=vod_channels("VG9vbHM="),   title="[COLOR white][B]Tools & Settings[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("aWNvbi5wbmc=")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
        if not xbmc.getCondVisibility('Pvr.HasTVChannels'):
            plugintools.add_item( action=vod_channels("R29EZXYuY29ycmVjdFBWUg=="),   title="[COLOR orange][B]Setup Full PVR[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=False )
            plugintools.add_item( action=vod_channels("R29EZXYuUFZSYmV0YQ=="),   title="[COLOR yellow][B]Setup PVR without VoD[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=False )
        else:
            plugintools.addItem('[COLOR redorange][B]Launch PVR[/B][/COLOR]','speed',11,GoDev.Images + 'logo.png',GoDev.Images + 'background.png')
            plugintools.add_item( action=vod_channels("R29EZXYuZGlzYWJsZVBWUg=="),   title="[COLOR redorange][B]Disable PVR[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bGl2ZXR2LnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=False )
    elif channels != 1 and GoDev.mode != 1:
        plugintools.add_item( action=vod_channels("bGljZW5zZV9jaGVjaw=="), title="[COLOR gold][B]Step 1. Insert Login Credentials[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("aWNvbi5wbmc=")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")), folder=False )	
        plugintools.add_item( action=vod_channels("bGljZW5zZV9jaGVjazI="), title="[COLOR gold][B]Step 2. Click Once Login Is Input[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("aWNvbi5wbmc=")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")), folder=False )	


def Tools(params):
	plugintools.add_item( action=vod_channels("ZXhlY3V0ZV9haW5mbw=="),   title="[COLOR red][B]Account Information[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
	plugintools.addItem('[COLOR red][B]Run Speedtest[/B][/COLOR]','speed',9,GoDev.Images + 'speed.png',GoDev.Images + 'background.png')
	plugintools.add_item( action=vod_channels("R29EZXYuREN0ZXN0"),   title="[COLOR red][B]Datacentre Speedtest[/B][/COLOR]" , thumbnail=GoDev.Images + 'speed.png', fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
	plugintools.add_item( action=vod_channels("bGljZW5zZV9jaGVjaw=="), title="[COLOR white][B]Addon Settings[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("aWNvbi5wbmc=")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=False )


def TheDev(params):
    tvaAPI = base64.b64decode("JXM6JXMvcGFuZWxfYXBpLnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcw==")%(lehekylg,pordinumber,kasutajanimi,salasona)
    link=open_url(tvaAPI)
    archivecheck = re.compile('"num":.+?,"name":"(.+?)".+?"stream_id":"(.+?)","stream_icon":"(.+?)".+?"tv_archive":(.+?).+?"tv_archive_duration":(.+?)}').findall(link)
    for kanalinimi,streamid,streamicon,tvarchive,archdays in archivecheck:
        if tvarchive == '1':
            streamicon = streamicon.replace('\/','/')
            archdays = archdays.replace('"','')
            plugintools.add_item( action=sync_data("dHZhcmNoaXZl"), title='[COLOR white]'+kanalinimi+'[/COLOR]' , thumbnail=streamicon, extra=streamid, page=archdays, fanart=os.path.join(LOAD_LIVE,sync_data("aG9tZXRoZWF0ZXIuanBn")), isPlayable=False, folder=True )
            plugintools.set_view( plugintools.LIST )

def tvarchive(extra):
    plugintools.set_view( plugintools.EPISODES )
    extra = str(extra)
    extra = extra.replace(',','')
    days = re.compile("'page': '(.+?)'").findall(extra)
    days = str(days)
    days = days.replace("['","").replace("']","")
    days = int(days)
    streamid = re.compile("'extra': '(.+?)'").findall(extra)
    streamicon = re.compile("'thumbnail': '(.+?)'").findall(extra)
    streamid = str(streamid)
    streamid = streamid.replace("['","").replace("']","")
    streamicon = str(streamicon)
    streamicon = streamicon.replace("['","").replace("']","")
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    date3 = datetime.datetime.now() - datetime.timedelta(days)
    date = str(date3)
    date = str(date).replace('-','').replace(':','').replace(' ','')
    APIv2 = base64.b64decode("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9zaW1wbGVfZGF0YV90YWJsZSZzdHJlYW1faWQ9JXM=")%(lehekylg,pordinumber,kasutajanimi,salasona,streamid)
    link=open_url(APIv2)
    match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
    for ShowTitle,start,end,DesC in match:
        ShowTitle = base64.b64decode(ShowTitle)
        DesC = base64.b64decode(DesC)
        format = '%Y-%m-%d %H:%M:%S'
        try:
            modend = dtdeep.strptime(end, format)
            modstart = dtdeep.strptime(start, format)
        except:
            modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
            modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
        StreamDuration = modend - modstart
        modend_ts = time.mktime(modend.timetuple())
        modstart_ts = time.mktime(modstart.timetuple())
        Duration=plugintools.get_setting("FinalDuration")
        if not Duration == 'Off':
            FinalDuration = Duration
        else:
            FinalDuration = int(modend_ts-modstart_ts) / 60
        strstart = start
        Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
        start2 = start[:-3]
        editstart = start2
        start2 = str(start2).replace(' ',' - ')
        t = float(modstart_ts)
        Prefix =  time.strftime("%a %d %H:%M", time.gmtime(t))
        start = str(editstart).replace(' ',':')
        Editstart = start[:13] + '-' + start[13:]
        Finalstart = Editstart.replace('-:','-')
        if Realstart > date:
            if Realstart < now:
                catchupURL = base64.b64decode("JXM6JXMvc3RyZWFtaW5nL3RpbWVzaGlmdC5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmc3RyZWFtPSVzJnN0YXJ0PQ==")%(lehekylg,pordinumber,kasutajanimi,salasona,streamid)
                ResultURL = catchupURL + str(Finalstart) + "&duration=%s"%(FinalDuration)
                kanalinimi = str('[COLOR white]'+Prefix+'[/COLOR]')+ " - " + '[COLOR gold]'+ShowTitle+'[/COLOR]'
                plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=kanalinimi , url=ResultURL, thumbnail=streamicon , plot=DesC, fanart=os.path.join(LOAD_LIVE,sync_data("aG9tZXRoZWF0ZXIuanBn")) , extra="", isPlayable=True, folder=False )

def license_check(params):
    plugintools.log(pnimi+get_live("U2V0dGluZ3MgbWVudQ==")+repr(params))
    plugintools.open_settings_dialog()

def license_check2(params):
	d = urllib.urlopen(loginurl)
	FileInfo = d.info()['Content-Type']
	if not 'application/octet-stream' in FileInfo:
		dialog.ok('[COLOR white]Invalid Login[/COLOR]','[COLOR white]Incorrect login details found![/COLOR]','[COLOR white]Please check your spelling and case sensitivity[/COLOR]','[COLOR white]Check your password with the team otherwise[/COLOR]')
		plugintools.open_settings_dialog()
	else:
		xbmc.executebuiltin('Container.Refresh')

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def convertSize(size):
   import math
   if (size == 0):
       return '[COLOR lime]0 MB[/COLOR]'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name == "B" or "KB":
        return '[COLOR lime]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name == "GB" or "TB" or "PB" or "EB" or "ZB" or "YB":
        return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 100:
        return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s < 50:
        return '[COLOR lime]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 50:
        if i < 100:
            return '[COLOR orange]%s %s' % (s,size_name[i]) + '[/COLOR]'

def maintMenu(params):

	CACHE      =  xbmc.translatePath(os.path.join('special://home/cache',''))
	PACKAGES   =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
	THUMBS     =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))

	if not os.path.exists(CACHE):
		CACHE     =  xbmc.translatePath(os.path.join('special://home/temp',''))
	if not os.path.exists(PACKAGES):
		os.makedirs(PACKAGES)

	CACHE_SIZE_BYTE    = get_size(CACHE)
	PACKAGES_SIZE_BYTE = get_size(PACKAGES)
	THUMB_SIZE_BYTE    = get_size(THUMBS)
	
	CACHE_SIZE    = convertSize(CACHE_SIZE_BYTE)
	PACKAGES_SIZE = convertSize(PACKAGES_SIZE_BYTE)
	THUMB_SIZE    = convertSize(THUMB_SIZE_BYTE)

	startup_clean = plugintools.get_setting("acstartup")
	weekly_clean = plugintools.get_setting("clearday")

	if startup_clean == "false":
		startup_onoff = "[COLOR red]OFF[/COLOR]"
	else:
		startup_onoff = "[COLOR lime]ON[/COLOR]"
	if weekly_clean == "0":
		weekly_onoff = "[COLOR red]OFF[/COLOR]"
	else:
		weekly_onoff = "[COLOR lime]ON[/COLOR]"

	common.addItem('[COLOR white][B]Auto Clean Device[/B][/COLOR]','url',19,ICON,FANART,'')
	common.addItem("[COLOR white][B]Clear Cache[/B][/COLOR] - Current Size: " + str(CACHE_SIZE),BASEURL,20,ICON,FANART,'')
	common.addItem("[COLOR white][B]Delete Thumbnails [/B][/COLOR] - Current Size: " + str(THUMB_SIZE),BASEURL,22,ICON,FANART,'')
	common.addItem("[COLOR white][B]Purge Packages [/B][/COLOR] - Current Size: " + str(PACKAGES_SIZE),BASEURL,23,ICON,FANART,'')
	common.addItem('[COLOR white][B]Update Addons & Repos[/B][/COLOR]',BASEURL,26,ICON,FANART,'')

def security_check(params):
	plugintools.add_item( action=vod_channels("VFZzZWFyY2g="),   title="[COLOR red][B]Search Shows on Now[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("U2VhcmNoLWljb24ucG5n")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
	plugintools.log(pnimi+sync_data("TGl2ZSBNZW51")+repr(params))
	request = urllib2.Request(televisioonilink, headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
		kanalinimi = channel.find(get_live("dGl0bGU=")).text
		kanalinimi = base64.b64decode(kanalinimi)
		kategoorialink = channel.find(vod_channels("cGxheWxpc3RfdXJs")).text
		CatID = channel.find(get_live("Y2F0ZWdvcnlfaWQ=")).text
		ICON = os.path.join(LOAD_LIVE,sync_data("aWNvbi5wbmc="))
		if 'NHL' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("TkhMLnBuZw=="))
		if 'MLB' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("TUxCLnBuZw=="))
		if 'SPORTS' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("c3BvcnRzLnBuZw=="))
		if 'USA' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("VVNBLnBuZw=="))
		if 'RADIO' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("VGhlX0xpdmVfUmFkaW9fTG9nby5wbmc="))
		if 'CANADIAN' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("RmxhZ19NYXBfb2ZfdGhlX1VuaXRlZF9TdGF0ZXNfKENhbmFkYSkucG5n"))
		if 'LATINO' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("c3BhbmlzaC5wbmc="))
		if 'PAY PER VIEW' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("UFBWLUxvZ28tRmluYWwucG5n"))
		if '24/7' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("MjQ3LnBuZw=="))
		if 'LOCAL NEWS' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("TkVXUy5wbmc="))
		if 'ALL' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("YWxsY2hhbm5lbHMucG5n"))
		if 'MUSIC' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("TXVzaWMtaWNvbi5wbmc="))
		if 'NFL' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("TkZMVVMucG5n"))
		if 'NBA' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("TkJBVFYucG5n"))
		if 'ADULT' in kanalinimi.upper():
			ICON=os.path.join(LOAD_LIVE,sync_data("UE9STi5wbmc="))



		plugintools.add_item( action=get_live("c3RyZWFtX3ZpZGVv"), title=kanalinimi , url=CatID , thumbnail=ICON , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) ,info_labels=kanalinimi, folder=True )

	plugintools.set_view( plugintools.LIST )
	


def stream_video(params):
    EPGColour=plugintools.get_setting("EPGColour")
    kasutajanimi=plugintools.get_setting("Username")
    salasona=plugintools.get_setting("Password")
    CatID = params.get(get_live("dXJs")) #description
    url = get_live("JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfbGl2ZV9zdHJlYW1zJmNhdF9pZD0lcw==")%(lehekylg,pordinumber,kasutajanimi,salasona,CatID)
    request = urllib2.Request(url, headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")): #channel
        kanalinimi = channel.find(get_live("dGl0bGU=")).text #title
        kanalinimi = base64.b64decode(kanalinimi)
        kanalinimi = kanalinimi.partition("[")
        striimilink = channel.find(get_live("c3RyZWFtX3VybA==")).text #stream_url
        pony = striimilink
        if ("%s:%s/enigma2.php")%(lehekylg,pordinumber)  in striimilink: 
            pony = striimilink.split(kasutajanimi,1)[1]
            pony = pony.split(salasona,1)[1]
            pony = pony.split("/",1)[1]            
        pilt = channel.find(vod_channels("ZGVzY19pbWFnZQ==")).text #desc_image
        kava = kanalinimi[1]+kanalinimi[2]
        kava = kava.partition("]")
        kava = kava[2]
        kava = kava.partition("   ")
        kava = kava[2]
        shou = get_live("W0NPTE9SIHdoaXRlXSVzWy9DT0xPUl0gW0NPTE9SICVzXSVzIFsvQ09MT1Jd")%(kanalinimi[0],EPGColour,kava)
        kirjeldus = channel.find(sync_data("ZGVzY3JpcHRpb24=")).text #description
        if kirjeldus:
           kirjeldus = base64.b64decode(kirjeldus)
           nyyd = kirjeldus.partition("(")
           nyyd = sync_data("Tm93OiA=") +nyyd[0]
           jargmine = kirjeldus.partition(")\n")
           jargmine = jargmine[2].partition("(")
           jargmine = sync_data("TmV4dDog") +jargmine[0] #shou
           kokku = nyyd+jargmine
        else:
           kokku = ""
        if pilt:
           plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=pony, thumbnail=pilt, plot=kokku, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")), extra="", isPlayable=True, folder=False )
        else:
           plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=pony, thumbnail=os.path.join(LOAD_LIVE,vod_channels("YWxsY2hhbm5lbHMucG5n")) , plot=kokku, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )
    plugintools.set_view( plugintools.EPISODES )

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

def detect_modification(params):
    plugintools.add_item( action=vod_channels("Vk9Ec2VhcmNo"),   title="[COLOR red][B]Search for VOD/TV SHOWS[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("U2VhcmNoLWljb24ucG5n")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
    plugintools.add_item( action=vod_channels("UmVjZW50bHlBZGRlZA=="),   title="Recently Added" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("dm9kLnBuZw==")), fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) ,  folder=True )
    plugintools.log(pnimi+vod_channels("Vk9EIE1lbnUg")+repr(params))
    request = urllib2.Request(filmilink, headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
        filminimi = channel.find(get_live("dGl0bGU=")).text
        filminimi = base64.b64decode(filminimi)
        kategoorialink = channel.find(vod_channels("cGxheWxpc3RfdXJs")).text
        plugintools.add_item( action=vod_channels("Z2V0X215YWNjb3VudA=="), title=filminimi , url=kategoorialink , thumbnail=os.path.join(LOAD_LIVE,sync_data("dm9kLnBuZw==")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=True )
	
    plugintools.set_view( plugintools.LIST )

def open_url(url):
    try:
        req = urllib2.Request(url,headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except:quit()

def RecentlyAdded(params):
	plugintools.set_view( plugintools.MOVIES )
	Recent = base64.b64decode(b'JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF92b2Rfc3RyZWFtcw==')%(lehekylg,pordinumber,kasutajanimi,salasona)
	Load = json.load(urllib2.urlopen(Recent))
	now = datetime.datetime.now()
	diff = datetime.timedelta(days=7)
	future = now - diff
	Past = future.strftime("%Y-%m-%d %H:%M:%S")
	for x in Load:
		DateAdded = x['added']
		pealkiri = x['name']
		Icon = x['stream_icon']
		StreamID = x['stream_id']
		Ext = x['container_extension']
		Normal = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(DateAdded)))
		if Normal > Past:
			if StreamID:
				striimilink = vod_channels('JXM6JXMvbW92aWUvJXMvJXMvJXMuJXM=')%(lehekylg,pordinumber,kasutajanimi,salasona,StreamID,Ext)
				URL = vod_channels('JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF92b2RfaW5mbyZ2b2RfaWQ9JXM=')%(lehekylg,pordinumber,kasutajanimi,salasona,StreamID)
				Meta = json.load(urllib2.urlopen(URL))
				try:
					Plot = Meta['info']['plot']
				except:
					Plot = 'No plot Available'
				try:
					Genre = Meta['info']['genre']
				except:
					Genre = 'Unknown Genre'
				try:
					Director = Meta['info']['director']
				except:
					Director = 'No Director Specified'
				try:
					ReleaseDate = Meta['info']['releasedate']
				except:
					ReleaseDate = 'Release Date Not Found'
				try:
					Duration = Meta['info']['duration']
				except:
					Duration = 'Duration Not Found'
				kirjeldus = Duration+'\n'+Plot.encode("utf-8")+'\n'+Director.encode("utf-8")+'\n'+Genre.encode("utf-8")+'\n'+ReleaseDate
				if Icon:
					plugintools.add_item( action="restart_service", title=pealkiri.encode("utf-8") , url=striimilink, thumbnail=Icon, plot=kirjeldus.encode("utf-8"), fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )
				else:
					plugintools.add_item( action="restart_service", title=pealkiri.encode("utf-8") , url=striimilink, thumbnail=os.path.join(LOAD_LIVE,sync_data("dm9kLnBuZw==")), plot=kirjeldus.encode("utf-8"), fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )

def VODsearch(params):
	SEARCH_LIST = base64.b64decode(b'JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfdm9kX3N0cmVhbXMmY2F0X2lkPTA=')%(lehekylg,pordinumber,kasutajanimi,salasona)
	keyb = xbmc.Keyboard('', '[COLOR white]Search[/COLOR]')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm=keyb.getText()
		searchterm=string.capwords(searchterm)
	else:quit()
	link=open_url(SEARCH_LIST) 
	match = re.compile('<title>(.+?)</title><desc_image><!\[CDATA\[(.+?)\]\]></desc_image><description>(.+?)</description>.+?<stream_url><!\[CDATA\[(.+?)\]\]></stream_url>').findall(link)
	for pealkiri,pilt,kirjeldus,striimilink in match:
		pealkiri = base64.b64decode(pealkiri)
		pealkiri = pealkiri.encode("utf-8")
		if kirjeldus:
			kirjeldus = base64.b64decode(kirjeldus)
		if searchterm in pealkiri:
			if pilt:
				plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=pilt, plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )
			else:
				plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=os.path.join("dm9kLnBuZw=="), plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )

def TVsearch(params):
	EPGColour=plugintools.get_setting("EPGColour")
	SEARCH_LIST = base64.b64decode(b'JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfbGl2ZV9zdHJlYW1zJmNhdF9pZD0w')%(lehekylg,pordinumber,kasutajanimi,salasona)
	keyb = xbmc.Keyboard('', '[COLOR white]Search[/COLOR]')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm=keyb.getText()
		searchterm=string.capwords(searchterm)
	else:quit()
	request = urllib2.Request(SEARCH_LIST, headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall(sync_data("Y2hhbm5lbA==")): #channel
		kanalinimi = channel.find(get_live("dGl0bGU=")).text #title
		kanalinimi = base64.b64decode(kanalinimi)
		kanalinimi = kanalinimi.partition("[")
		striimilink = channel.find(get_live("c3RyZWFtX3VybA==")).text #stream_url
		pony = striimilink
		if ("%s:%s/enigma2.php")%(lehekylg,pordinumber) in striimilink:
			pony = striimilink.split(kasutajanimi,1)[1]
			pony = pony.split(salasona,1)[1]
			pony = pony.split("/",1)[1]			
		pilt = channel.find(vod_channels("ZGVzY19pbWFnZQ==")).text #desc_image
		kava = kanalinimi[1]+kanalinimi[2]
		kava = kava.partition("]")
		kava = kava[2]
		kava = kava.partition("   ")
		kava = kava[2]
		shou = get_live("W0NPTE9SIHdoaXRlXSVzWy9DT0xPUl0gW0NPTE9SICVzXSVzIFsvQ09MT1Jd")%(kanalinimi[0],EPGColour,kava)
		kirjeldus = channel.find(sync_data("ZGVzY3JpcHRpb24=")).text #description
		if kirjeldus:
			kirjeldus = base64.b64decode(kirjeldus)
			nyyd = kirjeldus.partition("(")
			nyyd = sync_data("Tm93OiA=") +nyyd[0]
			jargmine = kirjeldus.partition(")\n")
			jargmine = jargmine[2].partition("(")
			jargmine = sync_data("TmV4dDog") +jargmine[0] #shou
			kokku = nyyd+jargmine
		else:
			kokku = ""
		if searchterm in kava:
			if pilt:
				plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=pony, thumbnail=pilt, plot=kokku, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")), extra="", isPlayable=True, folder=False )
			else:
				plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=pony, thumbnail=os.path.join(LOAD_LIVE,vod_channels("YWxsY2hhbm5lbHMucG5n")) , plot=kokku, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )

def get_myaccount(params):
    if vanemalukk == "true":
       pealkiri = params.get("title")
       vanema_lukk(pealkiri)
    purl = params.get("url")
    request = urllib2.Request(purl, headers={"Accept" : "application/xml","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall("channel"):
        try:
            pealkiri = channel.find("title").text
            pealkiri = base64.b64decode(pealkiri)
            pealkiri = pealkiri.encode("utf-8")
            striimilink = channel.find("stream_url").text
            pilt = channel.find("desc_image").text
            kirjeldus = channel.find("description").text
            if kirjeldus:
               kirjeldus = base64.b64decode(kirjeldus)
            if pilt:
               plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=pilt, plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )
            else:
               plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=os.path.join("dm9kLnBuZw=="), plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , extra="", isPlayable=True, folder=False )
        except:
            kanalinimi = channel.find("title").text
            kanalinimi = base64.b64decode(kanalinimi)
            kategoorialink = channel.find("playlist_url").text
            CatID = channel.find("category_id").text
            plugintools.add_item( action=get_live("Z2V0X215YWNjb3VudA=="), title=kanalinimi , url=kategoorialink , thumbnail=os.path.join(LOAD_LIVE,sync_data("dm9kLnBuZw==")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) ,info_labels=kanalinimi, folder=True )

    plugintools.set_view( plugintools.EPISODES )

def run_cronjob(params):
    kasutajanimi=plugintools.get_setting("Username")
    salasona=plugintools.get_setting("Password")
    lopplink = params.get("url")
    if "http://"  not in lopplink: 
        lopplink = get_live("aHR0cDovLyVzOiVzL2VuaWdtYS5waHAvbGl2ZS8lcy8lcy8lcw==")%(lehekylg,pordinumber,kasutajanimi,salasona,lopplink)
        lopplink = lopplink[:-2]
        lopplink = lopplink + "ts"
    listitem = xbmcgui.ListItem(path=lopplink)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def sync_data(channel):
    video = base64.b64decode(channel)
    return video

def restart_service(params):
    lopplink = params.get(vod_channels("dXJs"))
    plugintools.play_resolved_url( lopplink )

def grab_epg():
	req = urllib2.Request(andmelink)
	req.add_header(sync_data("VXNlci1BZ2VudA==") , vod_channels("S29kaSBwbHVnaW4gYnkgTWlra00="))
	response = urllib2.urlopen(req)
	link=response.read()
	try:
		jdata = json.loads(link.decode('utf8'))
		response.close()
		if jdata:
			plugintools.log(pnimi+sync_data("amRhdGEgbG9hZGVk"))
			return jdata
	except ValueError, e:
		return False

def kontroll():
	try:
		randomstring = grab_epg()
		kasutajainfo = randomstring[sync_data("dXNlcl9pbmZv")]
		kontroll = kasutajainfo[get_live("YXV0aA==")]
		return kontroll
	except:
		return None
def get_live(channel):
    video = base64.b64decode(channel)
    return video
def execute_ainfo(params):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		localip = s.getsockname()[0]
	except:
		localip = None
	try:
		f = urllib.urlopen("http://ip.42.pl/raw")
		html_doc = f.read()
		f.close()
	except:
		html_doc = None
	try:
		h = urllib.urlopen("https://myhostname.net")
		host_doc = h.read()
		h.close()
		hostname = re.compile('span id="curHostname" class="notranslate">(.+?)</span>').findall(host_doc)
		for i in hostname:
			host = i
	except:
		host = None
	data = json.load(urllib2.urlopen(PlayerAPI))
	today = datetime.date.today()
	x=data['user_info']
	Username = x['username']
	Status = x['status']
	Creation = x['created_at']
	Created = datetime.datetime.fromtimestamp(int(Creation)).strftime('%H:%M %d/%m/%Y')
	Current = x['active_cons']
	Max = x['max_connections']
	Expiry = x['exp_date']
	if Expiry == None:
		Expired = 'Never'
	else:
		Expired = datetime.datetime.fromtimestamp(int(Expiry)).strftime('%H:%M %d/%m/%Y')
	plugintools.add_item( action="",   title="[COLOR white][B]User: "+Username+"[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	plugintools.add_item( action="",   title="[COLOR white][B]Status: "+Status+"[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	plugintools.add_item( action="",   title="[COLOR white][B]Created: "+Created+"[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	plugintools.add_item( action="",   title="[COLOR white][B]Expires: "+Expired+"[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	plugintools.add_item( action="",   title="[COLOR white][B]Max connections: "+Max+"[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	plugintools.add_item( action="",   title="[COLOR white][B]Active connections: "+Current+"[/B][/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	if localip:
		plugintools.add_item( action="",   title="[COLOR white]Local IP: "+localip+"[/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	if html_doc:
		plugintools.add_item( action="",   title="[COLOR white]External IP: "+html_doc+"[/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )
	if host:
		plugintools.add_item( action="",   title="[COLOR white]Hostname: "+host+"[/COLOR]", thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,sync_data("dGhlYXRlci5qcGc=")) , folder=False )

	plugintools.set_view( plugintools.LIST )
def vanema_lukk(name):
        plugintools.log(pnimi+sync_data("UGFyZW50YWwgbG9jayA="))
        a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx'
        if any(s in name for s in a):
           xbmc.executebuiltin((u'XBMC.Notification("Parental Lock", "Channels may contain adult content", 2000)'))
           text = plugintools.keyboard_input(default_text="", title=get_live("UGFyZW50YWwgbG9jaw=="))
           if text==plugintools.get_setting(sync_data("dmFuZW1ha29vZA==")):
              return
           else:
              exit()
        else:
           name = ""
def check_user():
    plugintools.message(get_live("RVJST1I="),vod_channels("VU5BVVRIT1JJWkVEIEVESVQgT0YgQURET04h"))
    sys.exit()
def load_channels():
    statinfo = os.stat(LOAD_LIVE+"/"+get_live("YmFja2dyb3VuZC5wbmc="))

def vod_channels(channel):
    video = base64.b64decode(channel)
    return video

run()